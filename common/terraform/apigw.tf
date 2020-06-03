resource "aws_api_gateway_rest_api" "api" {
  name = "${local.app_name}-${terraform.workspace}"
  description = "API's for ${local.app_name}-${terraform.workspace}"
  endpoint_configuration {
    types = ["REGIONAL"]
  }
  tags = local.tags
}

resource "aws_api_gateway_resource" "base_resource" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id = aws_api_gateway_rest_api.api.root_resource_id
  path_part = "api"
}

resource "aws_ssm_parameter" "api_id" {
  name = local.ssm_api_id
  type = "String"
  value = aws_api_gateway_rest_api.api.id
  tags = local.tags
}

resource "aws_ssm_parameter" "api_base" {
  name = local.ssm_api_base
  type = "String"
  value = aws_api_gateway_resource.base_resource.id
  tags = local.tags
}