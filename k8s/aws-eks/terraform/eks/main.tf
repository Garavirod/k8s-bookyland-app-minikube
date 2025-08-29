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

variable vpc_id {
  description = "The VPC ID to use for the project"
  type = string
}

variable subnet_ids {
  description = "The subnet IDs to use for the project"
  type = list(string)
}



module "eks" {
    source = "terraform-aws-modules/eks/aws"
    version = "~> 19.0"

    cluster_name = "${var.project_name}-${var.environment}-eks"
    cluster_version = "1.27"

    vpc_id = var.vpc_id
    subnet_ids = var.subnet_ids

    cluster_endpoint_public_access = true # Ideally set this as false for production, this will allow public access to the cluster
    cluster_endpoint_private_access = true # Ideally set this as false for production, this will allow private access to the cluster

    cluster_addons = {
        kube-proxy = {
            resolve_conflicts = "OVERWRITE" // useful for PODs communication each other
        }
        coredns = {
            // Resolves service names to IP addresses, This is an internal DNS resolution
            // Pods needs to find other services by name
            resolve_conflicts = "OVERWRITE" 
        }
        vpc-cni = {
            // Handles security groups and NACLs
            // This manage Container Network Interface (CNI)
            // Native VPC networking for PODS
            resolve_conflicts = "OVERWRITE" 
        }
        csi = {
            // Manages volume provisioning and attachment
            // Enables persistent storage for pods
            // Storage driver for AWS EBS volumes
            // Pods need persistent storage (databases, file storage)
            // Enables PersistentVolumeClaims (PVCs)
            resolve_conflicts = "OVERWRITE"
        }
        aws-load-balancer-controller = {
          resolve_conflicts = "OVERWRITE"
        }
    }

    eks_managed_node_groups = {
        green = {
            desired_capacity = 1
            max_capacity = 2
            min_capacity = 1
            instance_types = ["t2.medium"]
            tags = {
                Name = "${var.project_name}-eks-green-node-group"
            }
        }
    }
}
