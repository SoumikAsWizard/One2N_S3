variable "aws_access_key" {
  description = "AWS Access Key"
  type        = string
}

variable "aws_secret_key" {
  description = "AWS Secret Key"
  type        = string
}

variable "aws_region" {
  description = "The AWS region of the ec2"
  default     = "us-east-1" # Optional default value
}

variable "key_pair_name" {
  description = "Name of a existing AWS key pair"
  type        = string
}

