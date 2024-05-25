from prefect import task, flow
import os
import boto3
from botocore.exceptions import NoCredentialsError

@task
def upload_to_s3(directory, bucket_name):
    # Initialize the S3 client
    s3 = boto3.client('s3')

    # Iterate through the files in the specified directory
    for filename in os.listdir(directory):
        if filename.endswith(".parquet"):
            file_path = os.path.join(directory, filename)
            s3_key = f"parquet/{filename}/{filename}"
            try:
                s3.upload_file(file_path, bucket_name, s3_key)
                print(f"Successfully uploaded {filename} to s3://{bucket_name}/{s3_key}")
            except FileNotFoundError:
                print(f"The file {file_path} was not found")
            except NoCredentialsError:
                print("Credentials not available")


@flow
def upload():
    parquet_directory = "parquet"
    s3_bucket_name = "bucket-data-engeneering-project-nick"
    upload_to_s3(parquet_directory, s3_bucket_name)
