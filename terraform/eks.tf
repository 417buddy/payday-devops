module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "20.8.5"

  cluster_name    = var.cluster_name
  cluster_version = "1.29"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  cluster_endpoint_public_access = true

  eks_managed_node_groups = {
    default = {
      instance_types = ["t3a.medium"]
      capacity_type  = "SPOT"
      min_size     = 1
      max_size     = 3
      desired_size = 2
    }
  }

  tags = {
    Project = "payday"
  }
}
