# One2N_S3

S3 Bucket Content Listing Application

**Overview**

This Flask-based application exposes a REST API endpoint to list the contents of an AWS S3 bucket. It provides both HTTP and HTTPS access for secure interactions. The application is designed for simplicity and scalability, ensuring seamless interaction with S3.

**Features**

List Bucket Contents: Retrieve the contents of a specified path in an S3 bucket.

Error Handling: Graceful handling of non-existent paths and bucket access issues.

HTTPS Support: Secure communication using a self-signed SSL certificate.

Environment Variables: Configuration is managed through a .env file for security.

**Design Decisions**

1. Boto3 with Flask Framework

Reason: Lightweight and easy to set up for RESTful APIs. I already had some knowledge on python and boto3.


2. HTTPS with Self-Signed Certificate

Reason: Adds a layer of encryption to secure data transmission during testing and development. To keep it simple using a self signed certificate.

Future Consideration: Can be replaced with certificates from Let's Encrypt or AWS Certificate Manager for production.

3. AWS S3 Integration Using Boto3

Reason: Boto3 is the official AWS SDK for Python, offering reliable and feature-rich S3 integration.

4. Environment Variable Management

Reason: Credentials and configuration are stored securely in a .env file to avoid hardcoding sensitive data.

Tools: python-dotenv library for loading environment variables.

## Assumptions

### Bucket Structure:

The bucket contains files and folders organized hierarchically.

### AWS Configuration:

Valid AWS credentials are available in the .env file.

The IAM user or role has sufficient permissions (e.g., s3:ListBucket, s3:GetObject).

### Deployment:

The application is deployed on an EC2 instance with proper security groups configured.

Port 5000 (Flask) and 443 (HTTPS) are open for incoming traffic.

### Self-Signed Certificate:

Browsers will show a warning for the self-signed certificate, which can be bypassed for testing purposes.

## Installation and Setup

1. Clone the Repository

git clone https://github.com/your-repo/s3-bucket-service.git
cd s3-bucket-service

2. Create the .env File

Add the following configuration:

AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-bucket-name

3. Install Dependencies

pip install -r requirements.txt

4. Generate SSL Certificates

openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=localhost"

5. Run the Application

python3 app.py

## Provision Infrastructure with Terraform

Navigate to the Terraform Directory:

cd terraform

Initialize Terraform:

terraform init

Apply Terraform Configuration:

terraform apply -var-file="terraform.tfvars"

Ensure to have a terraform.tfvars file with the necessary AWS credentials and configuration.

aws_access_key = "your-access-key"
aws_secret_key = "your-secret-access-key"
key_pair_name  = "your-keypair"
aws_region       = "your-region"

Access the Application:

Use the public IP provided by Terraform to access the application via HTTPS.

### API Usage

Endpoint:

GET /list-bucket-content/<path>

Examples:

List Top-Level Folders:

curl -k https://<public-ip>:5000/list-bucket-content

List Contents of a Specific Folder:

curl -k https://<public-ip>:5000/list-bucket-content/dir1

Future Enhancements

Replace Self-Signed Certificates: AWS Certificate Manager for trusted HTTPS.

Deployment Optimization:

Utilize Docker containers for portability.

Implement CI/CD pipelines.

Error Logging and Monitoring:

Integrate tools like AWS CloudWatch or Splunk for better observability.

Scalability:

Add support for large buckets with pagination.

Deploy behind a Load Balancer for high availability.

## Troubleshooting

### Cannot Access HTTPS:

Ensure the security group allows inbound traffic on port 443.

Verify the Flask app is bound to 0.0.0.0.

### Bucket Access Denied:

Check the IAM role or user permissions for the bucket.

Check for the correct bucket name.

Verify the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in the .env file.

### Self-Signed Certificate Warnings:

This is expected. Proceed with "Advanced → Proceed to site" in your browser.
