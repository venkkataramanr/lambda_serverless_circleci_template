try:
    import unzip_requirements  # NOQA
except ImportError:
    pass

import pandas as pd
from common.utils import S3Client


def lambda_handler(event, _context):

    s3_client = S3Client()
    event_bucket = event['Records'][0]['s3']['bucket']['name']
    event_key = event['Records'][0]['s3']['object']['key']
    output_bucket = "venkkat-output"

    with s3_client.object_as_io(event_bucket, event_key) as asn_obj:
        input_dataframe = pd.read_csv(asn_obj, sep="|")

    today_2_temp = input_dataframe["temperature_1"]
    today_1_temp = input_dataframe["temperature_2"]
    today_temp = input_dataframe["temperature_3"]

    input_dataframe["average_temperature"] = (today_1_temp + today_2_temp + today_temp) / 3

    s3_client.write_string(output_bucket, "output.csv", input_dataframe.to_csv(
            index=False, sep='|'
        ).encode())
