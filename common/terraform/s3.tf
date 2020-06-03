#=========================================================================
# S3 Bucket
#=========================================================================

# Create private s3 bucket for templates, bucket will be presented (read-only) via cloudfront
# Content bucket (data, blogs etc)

resource "aws_s3_bucket" "site_bucket" {
  bucket = local.site_bucket_name
  acl = "private"
  force_destroy = true
  tags = local.tags
}

resource "aws_ssm_parameter" "site_bucket" {
  name = local.ssm_site_bucket
  type = "String"
  value = aws_s3_bucket.site_bucket.id
  tags = local.tags
}

data "aws_iam_policy_document" "site_policy_doc" {
  statement {
    effect = "Allow"
    actions = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.site_bucket.arn}/*"]
    principals {
      identifiers = [
        aws_cloudfront_origin_access_identity.origin_access_identity.iam_arn
      ]
      type = "AWS"
    }
  }
}

resource "aws_s3_bucket_policy" "site_bucket_policy" {
  bucket = aws_s3_bucket.site_bucket.id
  policy = data.aws_iam_policy_document.site_policy_doc.json
}
