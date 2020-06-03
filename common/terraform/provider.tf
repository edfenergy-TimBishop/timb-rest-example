provider "aws" {
  region = "eu-west-1"
  profile = "default"
}

# required for ACM / Cloudfront certs only
provider "aws" {
  region = "us-east-1"
  profile = "default"
  alias = "us-east-1"
}