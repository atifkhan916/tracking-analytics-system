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

output "alb_dns_name" {
  description = "DNS name of the Application Load Balancer"
  value       = module.backend.alb_dns_name
}

output "ecr_repository_db_url" {
  description = "URL of the ECR repository for the database"
  value       = module.database.ecr_repository_url
}

# Database outputs
output "db_host" {
  description = "Hostname of the database"
  value       = module.database.db_host
}

output "efs_file_system_id" {
  description = "ID of the EFS file system"
  value       = module.database.efs_id
}