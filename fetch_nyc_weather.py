import os
import requests
import boto3
from datetime import datetime

def handler(event, context):
    # pull config
    api_key = os.environ["OPENWEATHER_API_KEY"]
    lat     = os.environ["LAT"]
    lon     = os.environ["LON"]
    bucket  = os.environ["BUCKET"]

    # current weather
    url      = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&appid={api_key}&units=imperial"
    )
    resp     = requests.get(url)
    resp.raise_for_status()
    data     = resp.json()

    # timestamp
    now  = datetime.utcnow()
    date = now.strftime("%Y-%m-%d")
    hour = now.strftime("%H")

    # extract metrics
    main    = data.get("main", {})
    weather = data.get("weather", [{}])[0]
    wind    = data.get("wind", {})

    temp       = main.get("temp", "")
    feels_like = main.get("feels_like", "")
    humidity   = main.get("humidity", "")
    desc       = weather.get("description", "")
    wind_spd   = wind.get("speed", "")

    # CSV line
    line = f"{date},{hour},{temp},{feels_like},{humidity},{desc},{wind_spd}\n"

    # upload to S3 under raw/nyc/<date>/<hour>.csv
    key = f"raw/nyc/{date}/{hour}.csv"
    boto3.client("s3").put_object(
        Bucket=bucket,
        Key=key,
        Body=line.encode("utf-8")
    )

    return {
        "status": "ok",
        "uploaded_key": key
    }
