terraform {
  required_providers {
    aws = {
      source  = "registry.terraform.io/hashicorp/aws"
      version = "~> 6.10.0"
    }
  }
  backend "s3" {
    // Backend configuration for S3 and DynamoDB is defined and managed by into CI/CD pipeline
  }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      ProjectName        = "${var.project_name}"
      Environment = var.environment
      ManagedBy   = "Terraform/Setup - EKS Bookyland Project"
    }
  }
}

