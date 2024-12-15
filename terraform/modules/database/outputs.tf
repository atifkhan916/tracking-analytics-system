output "db_security_group_id" {
  description = "Security Group ID of the database"
  value       = aws_security_group.db.id
}

output "db_host" {
  description = "Database host address"
  value       = aws_service_discovery_service.db.name
}

output "db_secret_arn" {
  description = "ARN of the database secret"
  value       = aws_secretsmanager_secret.db_password.arn
}

output "efs_id" {
  description = "ID of the EFS file system"
  value       = aws_efs_file_system.postgres_data.id
}

output "ecr_repository_url" {
  description = "URL of the database ECR repository"
  value       = aws_ecr_repository.db.repository_url
}