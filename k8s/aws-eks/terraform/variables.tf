/* Input variables comes from CI/CD pipeline */

// Project name
// This variable is used to specify the name of the project for tagging resources
variable "project_name" {
  description = "The name of the project"
  type        = string
  default     = "eks-bookly-app"
}

// Environment
// This variable is used to specify the environment (e.g., dev, prod) for tagging resources
variable "environment" {
  description = "The environment to use for the project"
  type        = string
}

// AWS region
// This variable is used to specify the AWS region where resources will be created
variable "aws_region" {
  description = "The AWS region to use for the project"
  type        = string  
}
