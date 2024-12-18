# terraform/main.tf
module "networking" {
  source = "./modules/networking"
  
  project             = var.project
  environment         = var.environment
  vpc_cidr           = var.vpc_cidr
  public_subnet_cidrs = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
  availability_zones  = var.availability_zones
}

module "ecs" {
  source = "./modules/ecs"
  
  project            = var.project
  environment        = var.environment
  vpc_id             = module.networking.vpc_id
  private_subnet_ids = module.networking.private_subnet_ids
  public_subnet_ids  = module.networking.public_subnet_ids
}

module "database" {
  source = "./modules/database"

  project            = var.project
  environment        = var.environment
  vpc_id             = module.networking.vpc_id
  private_subnet_ids = module.networking.private_subnet_ids
  ecs_cluster_id     = module.ecs.cluster_id
  ecs_execution_role_arn = module.ecs.execution_role_arn
  ecs_task_role_arn     = module.ecs.task_role_arn
  service_discovery_namespace_id = module.ecs.service_discovery_namespace_id
  db_security_group_id  =  module.networking.db_security_group_id
  db_name            = var.db_name
  db_user            = var.db_user
  db_password        = var.db_password
}

module "backend" {
  source = "./modules/backend"
  
  project            = var.project
  environment        = var.environment
  vpc_id             = module.networking.vpc_id
  private_subnet_ids = module.networking.private_subnet_ids
  public_subnet_ids  = module.networking.public_subnet_ids
  ecs_cluster_id     = module.ecs.cluster_id
  ecs_execution_role_arn = module.ecs.execution_role_arn
  ecs_task_role_arn     = module.ecs.task_role_arn
  ecs_execution_role_name = module.ecs.execution_role_name
  ecs_task_role_name = module.ecs.task_role_name
  service_discovery_namespace_id = module.ecs.service_discovery_namespace_id
  app_security_group_id = module.networking.app_security_group_id
  alb_security_group_id = module.networking.alb_security_group_id
  db_host            = module.database.db_host
  db_name            = var.db_name
  db_user            = var.db_user
  db_password        = var.db_password
}