# uses default provider configuration
resource "aws_s3_bucket" "my_bucket" {
  bucket = "aliases-east-1-bucket" # replace with your own unique name
  tags = {
    Name = "my-bucket-east-1"
  }
}

# alias provider specified, it will use its configuration
resource "aws_s3_bucket" "my_bucket_us_west_2" {
  bucket   = "aliases-west-2-bucket" # replace with your own unique name
  provider = aws.us_west_2
  tags = {
    Name = "my-bucket-west-2"
  }
}