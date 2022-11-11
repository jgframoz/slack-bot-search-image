import os

import boto3

from services.util import UtilService


class AwsService:

    @staticmethod
    def get_s3_client():
        region = os.environ.get('AWS_REGION')
        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        return boto3.client(
            's3',
            region_name=region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

    @staticmethod
    def normalize_bucket_name(bucket_name: str):
        """
        Hack: there can't be two buckets in the WORLD with the same name
        This shou prevent this from happening
        """
        return f'sib-{bucket_name.lower()}'

    @staticmethod
    def create_s3_bucket(bucket_name: str):
        region = os.environ.get('AWS_REGION')
        s3_client = AwsService.get_s3_client()
        location = {'LocationConstraint': region}
        
        # bucket name cant contain upper case letters
        bucket_name_normalized = AwsService.normalize_bucket_name(bucket_name)

        s3_client.create_bucket(Bucket=bucket_name_normalized, CreateBucketConfiguration=location)


    @staticmethod
    def upload_image(bucket_name: str, folder: str, path: str):
        s3_client = AwsService.get_s3_client()

        env = os.environ.get('ENV')
        file_id = UtilService.create_random_string(20)
        file_extention = path.split('.')[-1]
        remote_file_name = f'{folder}/{env}_{file_id}.{file_extention}'
        bucket_name_normalized = AwsService.normalize_bucket_name(bucket_name)

        try:
            s3_client.upload_file(path, bucket_name_normalized, remote_file_name, ExtraArgs={'ACL':'public-read'})
        except Exception as e:
            print('Error uploading image to S3', str(e))

        return f'https://{bucket_name_normalized}.s3.eu-west-1.amazonaws.com/{remote_file_name}'
