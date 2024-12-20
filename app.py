from flask import Flask, jsonify, request
import boto3
import os
from botocore.exceptions import ClientError
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

# Load AWS credentials from environment variables
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

# Initialize S3 client
if AWS_ACCESS_KEY and AWS_SECRET_KEY:
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION,
    )
else:
    # Use IAM Role if no credentials are set in environment
    s3_client = boto3.client("s3", region_name=AWS_REGION)

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

def list_top_level_folders(bucket_name):
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Delimiter="/")
        if "CommonPrefixes" in response:
            folders = [prefix["Prefix"].rstrip("/") for prefix in response["CommonPrefixes"]]
            return folders
        else:
            return []
    except ClientError as e:
        return jsonify({"error": "No such bucket exists"}), 404

@app.route("/list-bucket-content", defaults={"path": ""}, methods=["GET"])
@app.route("/list-bucket-content/<path:path>", methods=["GET"])
def list_bucket_content(path):
    if not BUCKET_NAME:
        return jsonify({"error": "S3_BUCKET_NAME is not configured"}), 500

    try:
        prefix = path.rstrip("/") + "/" if path else ""
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix, Delimiter="/")

        if "Contents" not in response and "CommonPrefixes" not in response:
            return jsonify({"error": "No such directory"}), 404

        content = []

        if "CommonPrefixes" in response:
            content.extend([prefix["Prefix"].rstrip("/") for prefix in response["CommonPrefixes"]])

        if "Contents" in response:
            content.extend([obj["Key"].split("/")[-1] for obj in response["Contents"] if obj["Key"] != prefix])

        return jsonify({"content": content})

    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchBucket":
            return jsonify({"error": f"Bucket '{BUCKET_NAME}' does not exist"}), 404
        elif e.response["Error"]["Code"] == "AccessDenied":
            return jsonify({"error": "Access denied to the bucket"}), 403
        else:
            return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
  
