output "cluster_id" {
  description = "ECS Cluster ID"
  value       = aws_ecs_cluster.main.id
}

output "cluster_name" {
  description = "ECS Cluster Name"
  value       = aws_ecs_cluster.main.name
}

output "execution_role_arn" {
  description = "ECS Execution Role ARN"
  value       = aws_iam_role.execution_role.arn
}

output "execution_role_id" {
  description = "ECS Execution Role ID"
  value       = aws_iam_role.execution_role.id
}

output "task_role_arn" {
  description = "ECS Task Role ARN"
  value       = aws_iam_role.task_role.arn
}

output "task_role_id" {
  description = "ECS Task Role ID"
  value       = aws_iam_role.task_role.id
}

output "service_discovery_namespace_id" {
  description = "Service Discovery Namespace ID"
  value       = aws_service_discovery_private_dns_namespace.main.id
}
