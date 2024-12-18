
output "db_host" {
  description = "Database host address"
  value       = aws_service_discovery_service.db.
}

output "efs_id" {
  description = "ID of the EFS file system"
  value       = aws_efs_file_system.postgres_data.id
}

output "ecr_repository_url" {
  description = "URL of the database ECR repository"
  value       = aws_ecr_repository.db.repository_url
}