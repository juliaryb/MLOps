resource "aws_s3_bucket" "this" {
   bucket = "${var.bucket_name_prefix}-${var.region}-${var.random_suffix}"
}

resource "aws_s3_bucket_versioning" "this" {
   bucket = aws_s3_bucket.this.id

   versioning_configuration {
      status = "Enabled"
   }
}

resource "aws_s3_bucket_lifecycle_configuration" "this" {
   bucket = aws_s3_bucket.this.id

   rule {
      id     = "transition-to-glacier"
      status = "Enabled"

      filter {}
      
      transition {
         days          = var.lifecycle_days
         storage_class = var.lifecycle_storage_class
      }
   }
}