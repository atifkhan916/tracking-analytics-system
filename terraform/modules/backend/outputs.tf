output "alb_dns_name" {
  description = "DNS name of the Application Load Balancer"
  value       = aws_lb.main.dns_name
}

output "ecr_repository_app_url" {
  value = data.aws_ecr_repository.app.repository_url
}

output "service_url" {
  description = "Service Discovery URL for the application"
  value       = aws_service_discovery_service.app.name
}
