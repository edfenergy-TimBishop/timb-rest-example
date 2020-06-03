#-------------------------------------------------------------------------
# Cloudfront
#-------------------------------------------------------------------------

resource "aws_cloudfront_origin_access_identity" "origin_access_identity" {
  comment = "OAI for ${local.domain}"
}

resource "aws_cloudfront_distribution" "cloudfront_distribution" {
    # UI is default
    default_cache_behavior {
        target_origin_id = "${local.app_name}-ui-${terraform.workspace}"
        
        allowed_methods = ["GET", "HEAD", "OPTIONS"]
        cached_methods = ["GET", "HEAD", "OPTIONS"]
        forwarded_values {
            query_string = true
            cookies {
                forward = "none"
            }
        }
        min_ttl = 0
        default_ttl = 0
        max_ttl = 0
        compress = true
        viewer_protocol_policy = "redirect-to-https"
    }
      
    # API
    ordered_cache_behavior {
        path_pattern = "/api/*"
        allowed_methods = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
        cached_methods = ["HEAD", "GET", "OPTIONS"]
        target_origin_id = "${local.app_name}-api-${terraform.workspace}"

        forwarded_values {
            query_string = true
            headers = [
                "Access-Control-Request-Headers",
                "Access-Control-Request-Method",
                "Origin",
                "Authorization",
                "Accept",
                "Content-Type",
                "Referer",
                "x-api-key"
            ]
            cookies {
                forward = "none"
            }
        }

        min_ttl = 0
        default_ttl = 0
        max_ttl = 0
        compress = true
        viewer_protocol_policy = "https-only"
    }

    # UI Origin 
    origin {
        domain_name = aws_s3_bucket.site_bucket.bucket_regional_domain_name
        origin_id = "${local.app_name}-ui-${terraform.workspace}"

        s3_origin_config {
            origin_access_identity = aws_cloudfront_origin_access_identity.origin_access_identity.cloudfront_access_identity_path
        }
    }

    # API Orgin
    origin {
        domain_name = "${aws_api_gateway_rest_api.api.id}.execute-api.${local.region}.amazonaws.com"
        origin_id = "${local.app_name}-api-${terraform.workspace}"
        origin_path = "/${terraform.workspace}"
        custom_origin_config {
            origin_protocol_policy = "https-only"
            origin_ssl_protocols = ["SSLv3"]
            https_port = 443
            http_port = 80
        }
    }

    default_root_object = "index.html"
    enabled = true

    #aliases = [ local.website_domain ]

    # Distributes content to US and Europe
    price_class = "PriceClass_100"

    # Restricts who is able to access this content
    restrictions {
        geo_restriction {
            # type of restriction, blacklist, whitelist or none
            restriction_type = "none"
        }
    }

    # SSL certificate for the service.
    viewer_certificate {
        #acm_certificate_arn = aws_acm_certificate.cert.arn
        #ssl_support_method = "sni-only"
        cloudfront_default_certificate = true
    }

    custom_error_response {
        error_code = 403
        response_code = 403
        response_page_path = "/index.html"
    }

    custom_error_response {
        error_code = 404
        response_code = 404
        response_page_path = "/index.html"
    }

    tags = local.tags
}

resource "aws_ssm_parameter" "cf_distro" {
  name = local.ssm_cf_distro
  type = "String"
  value = aws_cloudfront_distribution.cloudfront_distribution.id
  tags = local.tags
}
