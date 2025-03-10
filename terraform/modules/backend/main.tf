# ECR Repository
resource "aws_ecr_repository" "app" {
  name         = "${var.project}-${var.environment}-app"
  force_delete = true

  tags = {
    Name        = "${var.project}-${var.environment}-app"
    Environment = var.environment
    Project     = var.project
  }
}

# Policy for accessing Secrets Manager
resource "aws_iam_role_policy" "task_secrets_policy" {
  name = "${var.project}-${var.environment}-app-secrets-policy"
  role = var.ecs_task_role_arn

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue",
          "kms:Decrypt"
        ]
        Resource = [
          aws_secretsmanager_secret.db_password.arn
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy" "task_logs_policy" {
  name = "${var.project}-${var.environment}-app-logs-policy"
  role = var.ecs_task_role_arn

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "logs:DescribeLogStreams"
        ]
        Resource = [
          "arn:aws:logs:${var.aws_region}:${data.aws_caller_identity.current.account_id}:log-group:/ecs/${var.project}-${var.environment}*",
          "arn:aws:logs:${var.aws_region}:${data.aws_caller_identity.current.account_id}:log-group:/ecs/${var.project}-${var.environment}*:*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy" "execution_policy" {
  name = "${var.project}-${var.environment}-app-execution-policy"
  role = var.ecs_execution_role_arn

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ecr:GetAuthorizationToken",
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = [
          aws_secretsmanager_secret.db_password.arn
        ]
      }
    ]
  })
}

# Get current AWS account ID
data "aws_caller_identity" "current" {}

# Create CloudWatch Log Group
resource "aws_cloudwatch_log_group" "app" {
  name              = "/ecs/${var.project}-${var.environment}"
  retention_in_days = 30

  tags = {
    Name        = "${var.project}-${var.environment}-app-logs"
    Environment = var.environment
    Project     = var.project
  }
}

# Security Groups
resource "aws_security_group" "alb" {
  name        = "${var.project}-${var.environment}-alb-sg"
  description = "Security group for ALB"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.project}-${var.environment}-alb-sg"
    Environment = var.environment
    Project     = var.project
  }
}

resource "aws_security_group" "app" {
  name        = "${var.project}-${var.environment}-app-sg"
  description = "Security group for the application"
  vpc_id      = var.vpc_id

  ingress {
    from_port       = 8000
    to_port         = 8000
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.project}-${var.environment}-app-sg"
    Environment = var.environment
    Project     = var.project
  }
}

resource "aws_security_group" "db" {
  name        = "${var.project}-${var.environment}-db-sg"
  description = "Security group for PostgreSQL database"
  vpc_id      = var.vpc_id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.project}-${var.environment}-db-sg"
    Environment = var.environment
    Project     = var.project
  }
}

# ALB
resource "aws_lb" "main" {
  name               = "${var.project}-${var.environment}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets           = var.public_subnet_ids

  tags = {
    Name        = "${var.project}-${var.environment}-alb"
    Environment = var.environment
    Project     = var.project
  }
}

resource "aws_lb_target_group" "app" {
  name        = "${var.project}-${var.environment}-app-tg"
  port        = 8000
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 3
    timeout            = 5
    interval           = 30
    path               = "/health"
    matcher            = "200"
  }

  tags = {
    Name        = "${var.project}-${var.environment}-app-tg"
    Environment = var.environment
    Project     = var.project
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}

# ECS Task Definition
resource "aws_ecs_task_definition" "app" {
  family                   = "${var.project}-${var.environment}-app"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = var.ecs_execution_role_arn
  task_role_arn           = var.ecs_task_role_arn

  container_definitions = jsonencode([
    {
      name      = "app"
      image     = "${aws_ecr_repository.app.repository_url}:latest"
      essential = true
      
      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
          protocol      = "tcp"
        }
      ]
      
      environment = [
        {
          name  = "DB_HOST"
          value = var.db_host
        },
        {
          name  = "DB_NAME"
          value = var.db_name
        },
        {
          name  = "DB_USER"
          value = var.db_user
        }
      ]
      
      secrets = [
        {
          name      = "DB_PASSWORD"
          valueFrom = aws_secretsmanager_secret.db_password.arn
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
           "awslogs-group"         = aws_cloudwatch_log_group.app.name
           "awslogs-region"        = var.aws_region
           "awslogs-stream-prefix" = "app"
        }
      }
    }
  ])

  tags = {
    Name        = "${var.project}-${var.environment}-app-task"
    Environment = var.environment
    Project     = var.project
  }
}

# ECS Service
resource "aws_ecs_service" "app" {
  name            = "${var.project}-${var.environment}-app"
  cluster         = var.ecs_cluster_id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = 2
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [aws_security_group.app.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = "app"
    container_port   = 8000
  }

  service_registries {
    registry_arn = aws_service_discovery_service.app.arn
  }

  tags = {
    Name        = "${var.project}-${var.environment}-app-service"
    Environment = var.environment
    Project     = var.project
  }
}

# Service Discovery
resource "aws_service_discovery_service" "app" {
  name = "app"

  dns_config {
    namespace_id = var.service_discovery_namespace_id

    dns_records {
      ttl  = 10
      type = "A"
    }
  }

  health_check_custom_config {
    failure_threshold = 1
  }
}

# Secrets Manager for DB Password
resource "aws_secretsmanager_secret" "db_password" {
  name = "${var.project}-${var.environment}-app-db-password"
  
  tags = {
    Name        = "${var.project}-${var.environment}-app-db-password"
    Environment = var.environment
    Project     = var.project
  }
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id     = aws_secretsmanager_secret.db_password.id
  secret_string = jsonencode({
    username = var.db_user
    password = var.db_password
  })
}