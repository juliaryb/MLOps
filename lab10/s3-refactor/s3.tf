# s3
resource "random_id" "bucket_suffix" {
  count       = length(var.regions)
  keepers = {
    force_regenerate = timestamp()
  }
  byte_length = 6
}

# create us-east-1 bucket using the default provider
module "s3_us_east_1" {
  source             = "./modules/s3_bucket"
  bucket_name_prefix = var.bucket_name_prefix
  region             = var.regions[0]
  random_suffix      = random_id.bucket_suffix[0].hex
}

# create us-west-2 bucket using the eu_west_1 provider
module "s3_us_west_2" {
  source            = "./modules/s3_bucket"
  # notice how we pass provider alias to the module.
  providers = {
    aws = aws.us_west_2
  }
  bucket_name_prefix = var.bucket_name_prefix
  region            = var.regions[1]
  random_suffix     = random_id.bucket_suffix[1].hex
  lifecycle_days = 30
}
