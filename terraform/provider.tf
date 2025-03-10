terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    # Will be configured via backend-config file
  }
}

provider "aws" {
  region = var.aws_region
}
