variable "regions" {
  description = "AWS regions where buckets will be created (order matters)"
  type        = list(string)
  default     = ["us-east-1", "us-west-2"]
}

variable "bucket_name_prefix" {
  description = "Prefix for S3 bucket names (must be DNS-compatible: lowercase, digits, hyphens)"
  type        = string
  default     = "julia-multi-region-bucket"
}