import json
import os
from botocore.exceptions import ClientError
from io import BytesIO
import boto3

THIS_DIR = os.path.dirname(__file__)
FIXTURES_DIR = os.path.join(THIS_DIR, 'fixtures')


class S3Client:

    def __init__(self, **session_kwargs):
        self.boto_session = boto3.Session(**session_kwargs)
        self.s3_resource = self.boto_session.resource('s3')
        self.s3_client = self.boto_session.client('s3')

    def object_as_io(self, bucket, key):
        """
        Grab the given bucket/key from s3 as an io stream (File-like object)

        N.B: Use as a context manager

        :param bucket: the bucket
        :param key: the key you want
        :return: an io stream of data
        """
        bucket = self.s3_resource.Bucket(bucket)

        data = BytesIO()
        try:
            bucket.download_fileobj(key, data)
        except ClientError as exc:
            if exc.response['Error']['Code'] == '404':
                raise
            raise

        data.seek(0)
        return data

    def write_string(self, bucket, key, data, **upload_kwargs):
        """
        Write the given data to s3

        :param bucket: the bucket you want to write to
        :param key: the key you want to write at
        :param data: the data

        """
        bucket = self.s3_resource.Bucket(bucket)

        with BytesIO(data) as fp:
            bucket.upload_fileobj(fp, key, ExtraArgs=upload_kwargs)


def s3_put_event_factory(bucket, key):
    """
    Generate an s3 put event, with the given bucket and key

    :param bucket: the bucket that the event came from
    :param key: the key that has been put
    :return: an s3 event dict
    """

    with open(os.path.join('/Users/venkkataraman.r/workspace/tcs_ci_session/tests/fixtures/s3_put_event.json')) as f:
        event = json.loads(f.read())

    event['Records'][0]['s3']['bucket']['name'] = bucket
    event['Records'][0]['s3']['object']['key'] = key

    return event


def read_s3_file(bucket, key):
    s3 = boto3.client('s3')
    output = s3.get_object(Bucket=bucket, Key=key)
    contents = output['Body'].read()

    try:
        return contents.decode()
    except UnicodeDecodeError:
        return contents.decode('latin')


def get_all_keys(bucket, prefix='', suffix=''):
    s3 = boto3.resource('s3')
    Bucket = s3.Bucket(bucket)
    results = [x.key for x in Bucket.objects.all() if x.key.startswith(prefix)]
    if suffix:
        return [x for x in results if x.endswith(suffix)]
    return results
