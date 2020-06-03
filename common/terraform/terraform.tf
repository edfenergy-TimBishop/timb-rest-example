terraform {
  backend "s3" {
    bucket = "smec-terraform-state-bucket" 
    key = "example"
    region = "eu-west-1"
  }
}
