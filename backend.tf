terraform {
  backend "s3" {
    bucket       = "payday-tf-state-13052026"
    key          = "eks/terraform.tfstate"
    use_lockfile = true   # ⭐ enables native state locking
  }
}