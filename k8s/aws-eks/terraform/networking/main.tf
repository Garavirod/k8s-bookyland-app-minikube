variable project_name {
  description = "The name of the project"
  type = string
}

variable environment {
  description = "The environment to use for the project"
  type = string
}

variable aws_region {
  description = "The AWS region to use for the project"
  type = string
}

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"
  name = "${var.project_name}-${var.environment}-vpc"
  cidr = "10.0.0.0/16"
  azs = ["${var.aws_region}a", "${var.aws_region}b", "${var.aws_region}c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets = ["10.0.4.0/24", "10.0.5.0/24", "10.0.6.0/24"]
  create_igw = true
  enable_nat_gateway = true 
  single_nat_gateway = true # with False, it will create a NAT gateway for each subnet (ideally for production)
  tags = {
    Name = "${var.project_name}-${var.environment}-vpc"
  }
}
