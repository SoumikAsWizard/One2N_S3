provider "aws" {
  region     = var.aws_region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

resource "aws_security_group" "instance_sg" {
  name   = "s3-service-sg"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "app_instance" {
  ami           = "ami-0c02fb55956c7d316"  # Amazon Linux 2 AMI
  instance_type = "t2.micro"
  key_name      = var.key_pair_name
  security_groups = [
    aws_security_group.instance_sg.name
  ]

  tags = {
    Name = "S3-Bucket-Service-Instance"
  }
}

output "instance_public_ip" {
  value = aws_instance.app_instance.public_ip
}
