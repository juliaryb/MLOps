variable "bucket_name_prefix" {
  type = string
}

variable "region" {
   type = string
}

variable "random_suffix" {
  type = string
}

variable "lifecycle_days" {
  type = number
  default = 90
}

variable "lifecycle_storage_class" {
  type = string
  default = "GLACIER"
}