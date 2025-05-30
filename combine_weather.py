import os
import boto3
from datetime import datetime, timezone

s3 = boto3.client("s3")

def handler(event, context):
    bucket        = os.environ["BUCKET"]
    nyc_prefix    = os.environ.get("NYC_PREFIX", "raw/nyc")
    la_prefix     = os.environ.get("LA_PREFIX",  "raw/la")
    out_prefix    = os.environ.get("OUT_PREFIX", "raw/combined")

    # Use UTC now so it matches your hourly schedule
    now     = datetime.now(timezone.utc)
    date    = now.strftime("%Y-%m-%d")
    hour    = now.strftime("%H")

    nyc_key     = f"{nyc_prefix}/{date}/{hour}.csv"
    la_key      = f"{la_prefix}/{date}/{hour}.csv"
    combined_key= f"{out_prefix}/{date}/{hour}.csv"

    # fetch each single-row CSV
    nyc_obj = s3.get_object(Bucket=bucket, Key=nyc_key)["Body"].read().decode()
    la_obj  = s3.get_object(Bucket=bucket, Key=la_key )["Body"].read().decode()

    # combine into two lines
    combined = "\n".join([nyc_obj.strip(), la_obj.strip()]) + "\n"

    # write back to S3
    s3.put_object(
        Bucket=bucket,
        Key=combined_key,
        Body=combined.encode(),
        ContentType="text/csv"
    )

    return {
        "statusCode": 200,
        "body": f"wrote {combined_key}"
    }
