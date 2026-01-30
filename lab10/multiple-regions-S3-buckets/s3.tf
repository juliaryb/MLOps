resource "random_id" "bucket_suffix" {
  count       = length(var.regions)
  byte_length = 4
}

resource "aws_s3_bucket" "s3_us_east_1" {
  bucket = "${var.bucket_name_prefix}-${var.regions[0]}-${random_id.bucket_suffix[0].hex}"
}

resource "aws_s3_bucket_versioning" "s3_us_east_1" {
  bucket = aws_s3_bucket.s3_us_east_1.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "s3_us_east_1" {
  bucket = aws_s3_bucket.s3_us_east_1.id

  rule {
    id     = "transition-to-glacier"
    status = "Enabled"

    filter {}    # means to apply rules to all objects (prevents warning on terraform apply)

    transition {
      days          = 90
      storage_class = "GLACIER_IR"
    }
  }
}


# second bucket – same structure, different region and provider alias

resource "aws_s3_bucket" "s3_us_west_2" {
  provider = aws.us_west_2
  bucket   = "${var.bucket_name_prefix}-${var.regions[1]}-${random_id.bucket_suffix[1].hex}"
}

resource "aws_s3_bucket_versioning" "s3_us_west_2" {
  provider = aws.us_west_2
  bucket   = aws_s3_bucket.s3_us_west_2.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "s3_us_west_2" {
  provider = aws.us_west_2
  bucket   = aws_s3_bucket.s3_us_west_2.id

  rule {
    id     = "transition-to-glacier"
    status = "Enabled"

    filter {}

    transition {
      days          = 90
      storage_class = "GLACIER_IR"
    }
  }
}
