variable "regions" {
  type        = list(string)
  default     = ["us-east-1", "us-west-2"]
}

variable "bucket_name_prefix" {
  type        = string
  default     = "julia-multi-region-bucket"
}