from dotenv import load_dotenv

load_dotenv()

import boto3
import os


class S3Client:
    def __init__(self):
        self.client = boto3.client(
            's3',
            endpoint_url='https://atlas-seal-cloud.cern.ch:443',
            verify=False,
            aws_access_key_id=os.getenv('aws_access_key_id'),
            aws_secret_access_key=os.getenv('aws_secret_access_key'),
            aws_session_token=None,
            config=boto3.session.Config(signature_version='s3v4'),
        )

    def upload_file(self, bucket, file_path, key):
        self.client.upload_file(file_path, bucket, key)

    def download_file(self, bucket, key, file_path):
        self.client.download_file(bucket, key, file_path)

    def list_objects(self, bucket):
        return self.client.list_objects(Bucket=bucket)

    def delete_object(self, bucket, key):
        self.client.delete_object(Bucket=bucket, Key=key)

    def delete_objects(self, bucket, keys):
        self.client.delete_objects(
            Bucket=bucket,
            Delete={
                'Objects': [{'Key': key} for key in keys]
            }
        )

    def create_bucket(self, bucket):
        self.client.create_bucket(Bucket=bucket)

    def delete_bucket(self, bucket):
        self.client.delete_bucket(Bucket=bucket)


if __name__ == '__main__':
    s3_client = S3Client()
    print(s3_client.list_objects('rucio_dev'))

    s3_client.download_file('rucio_dev', 'reporting/manifest/20220101-20220801/entries.csv', 'consistency_checks/data/seal/entries.csv')
    s3_client.download_file('rucio_dev', 'reporting/manifest/20220101-20220801/errors.csv', 'consistency_checks/data/seal/errors.csv')
