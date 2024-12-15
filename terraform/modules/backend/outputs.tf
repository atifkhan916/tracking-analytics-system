output "app_security_group_id" {
  description = "Security Group ID of the application"
  value       = aws_security_group.app.id
}

output "alb_dns_name" {
  description = "DNS name of the Application Load Balancer"
  value       = aws_lb.main.dns_name
}

output "ecr_repository_url" {
  description = "URL of the application ECR repository"
  value       = aws_ecr_repository.app.repository_url
}

output "app_secret_arn" {
  description = "ARN of the application secret"
  value       = aws_secretsmanager_secret.db_password.arn
}

output "service_url" {
  description = "Service Discovery URL for the application"
  value       = aws_service_discovery_service.app.name
}

output "db_security_group_id" {
  description = "Security Group ID of the database"
  value       = aws_security_group.db.id
}