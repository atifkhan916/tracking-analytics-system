# ECR Repository for DB
resource "aws_ecr_repository" "db" {
  name         = "${var.project}-${var.environment}-db"
  force_delete = true

  tags = {
    Name        = "${var.project}-${var.environment}-db"
    Environment = var.environment
    Project     = var.project
  }
}

# EFS for PostgreSQL Data
resource "aws_efs_file_system" "postgres_data" {
  creation_token = "${var.project}-${var.environment}-postgres-data"
  encrypted      = true

  lifecycle_policy {
    transition_to_ia = "AFTER_30_DAYS"
  }

  tags = {
    Name        = "${var.project}-${var.environment}-postgres-data"
    Environment = var.environment
    Project     = var.project
  }
}

resource "aws_security_group" "efs" {
  name        = "${var.project}-${var.environment}-efs-sg"
  description = "Security group for EFS mount targets"
  vpc_id      = var.vpc_id

  ingress {
    from_port       = 2049
    to_port         = 2049
    protocol        = "tcp"
    security_groups = [var.db_security_group_id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.project}-${var.environment}-efs-sg"
    Environment = var.environment
    Project     = var.project
  }
}

resource "aws_efs_mount_target" "postgres_data" {
  count           = length(var.private_subnet_ids)
  file_system_id  = aws_efs_file_system.postgres_data.id
  subnet_id       = var.private_subnet_ids[count.index]
  security_groups = [aws_security_group.efs.id]
}

# Service Discovery for Database
resource "aws_service_discovery_service" "db" {
  name = "db"

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


# ECS Task Definition for Database
resource "aws_ecs_task_definition" "db" {
  family                   = "${var.project}-${var.environment}-db"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 512
  memory                   = 1024
  execution_role_arn       = var.ecs_execution_role_arn
  task_role_arn           = var.ecs_task_role_arn

  container_definitions = jsonencode([
    {
      name      = "db"
      image     = "postgres:14"
      essential = true
      
      portMappings = [
        {
          containerPort = 5432
          hostPort      = 5432
          protocol      = "tcp"
        }
      ]
      
      environment = [
        {
          name  = "POSTGRES_DB"
          value = var.db_name
        },
        {
          name  = "POSTGRES_USER"
          value = var.db_user
        }
      ]
      
      secrets = [
        {
          name      = "POSTGRES_PASSWORD"
          value = var.db_password
        }
      ]

      mountPoints = [
        {
          sourceVolume  = "postgres-data"
          containerPath = "/var/lib/postgresql/data"
          readOnly      = false
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/${var.project}-${var.environment}"
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "db"
        }
      }
    }
  ])

  volume {
    name = "postgres-data"
    efs_volume_configuration {
      file_system_id = aws_efs_file_system.postgres_data.id
      root_directory = "/"
    }
  }

  tags = {
    Name        = "${var.project}-${var.environment}-db-task"
    Environment = var.environment
    Project     = var.project
  }
}

# ECS Service for Database
resource "aws_ecs_service" "db" {
  name            = "${var.project}-${var.environment}-db"
  cluster         = var.ecs_cluster_id
  task_definition = aws_ecs_task_definition.db.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [var.db_security_group_id]
    assign_public_ip = false
  }

  service_registries {
    registry_arn = aws_service_discovery_service.db.arn
  }

  tags = {
    Name        = "${var.project}-${var.environment}-db-service"
    Environment = var.environment
    Project     = var.project
  }
}