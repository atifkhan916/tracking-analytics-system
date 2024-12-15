# Networking outputs
output "vpc_id" {
  description = "ID of the VPC"
  value       = module.networking.vpc_id
}

output "private_subnet_ids" {
  description = "IDs of the private subnets"
  value       = module.networking.private_subnet_ids
}

output "public_subnet_ids" {
  description = "IDs of the public subnets"
  value       = module.networking.public_subnet_ids
}

# ECS outputs
output "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  value       = module.ecs.ecs_cluster_name
}

output "alb_dns_name" {
  description = "DNS name of the Application Load Balancer"
  value       = module.ecs.alb_dns_name
}

output "ecr_repository_app_url" {
  description = "URL of the ECR repository for the application"
  value       = module.ecs.ecr_repository_app_url
}

output "ecr_repository_db_url" {
  description = "URL of the ECR repository for the database"
  value       = module.ecs.ecr_repository_db_url
}

# Database outputs
output "db_host" {
  description = "Hostname of the database"
  value       = module.database.db_host
}

output "efs_file_system_id" {
  description = "ID of the EFS file system"
  value       = module.database.efs_file_system_id
}