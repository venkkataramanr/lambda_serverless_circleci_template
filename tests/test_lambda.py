import boto3
import os
from moto import mock_s3
from common.utils import s3_put_event_factory, read_s3_file, get_all_keys
from lambda.handler import lambda_handler

THIS_DIR = os.path.dirname(__file__)
FIXTURES_DIR = os.path.join(THIS_DIR, 'fixtures')


class TestLambda:

    def setup(self):
        self.mocked_s3 = mock_s3()
        self.mocked_s3.start()

        s3 = boto3.resource('s3')
        input_bucket = s3.Bucket("venkkat-test")
        output_bucket = s3.Bucket("venkkat-output")
        output_bucket.create()
        input_bucket.create()
        input_bucket.upload_file(os.path.join(FIXTURES_DIR, "input.csv"), "input.csv")

    def test_handler(self):
        event_bucket = "venkkat-test"
        event_key = "input.csv"
        output_bucket = "venkkat-output"
        output_key = "output.csv"
        event = s3_put_event_factory(event_bucket, event_key)

        # Execution
        lambda_handler(event, {})

        input_file = read_s3_file(event_bucket, event_key).split('\n')
        bucket_files = get_all_keys(output_bucket, prefix=output_key)
        output_file = read_s3_file(output_bucket, bucket_files[0]).split('\n')

        assert len(bucket_files) == 1
        assert len(input_file) == len(output_file)

    def teardown(self):
        self.mocked_s3.stop()
