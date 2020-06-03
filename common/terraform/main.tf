#=========================================================================
# Main
#=========================================================================

locals {
  region = "eu-west-1"
  domain = "XXX"
  website_domain = "${terraform.workspace}.${local.domain}"
  app_name = "smec-example"
  site_bucket_name = "${local.app_name}-site-${terraform.workspace}"
  content_bucket_name = "${local.app_name}-content-${terraform.workspace}.test"
  ssm_site_bucket = "/${local.app_name}/site-bucket/${terraform.workspace}"
  ssm_cf_distro = "/${local.app_name}/cf_distro/${terraform.workspace}"
  ssm_api_id = "/${local.app_name}/api_id/${terraform.workspace}"
  ssm_api_base = "/${local.app_name}/api_base/${terraform.workspace}"
  tags = {
    PRODUCT = local.app_name
    STAGE = terraform.workspace
  }
}

data "aws_caller_identity" "current" {}
