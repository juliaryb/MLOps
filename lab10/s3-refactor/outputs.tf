output "bucket_arns" {
   value = {
      (var.regions[0]) = module.s3_us_east_1.bucket_arn,
      (var.regions[1]) = module.s3_us_west_2.bucket_arn,
   }
}

output "bucket_regions" {
  value = {
    "${module.s3_us_east_1.bucket_id}" = var.regions[0],
    "${module.s3_us_west_2.bucket_id}" = var.regions[1],
  }
}