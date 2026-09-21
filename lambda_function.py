import json
import boto3
import os
from PIL import Image
from io import BytesIO

s3_client = boto3.client("s3")

INPUT_BUCKET = "bucket-for-lamda-resizer-1"
OUTPUT_BUCKET = "bucket-for-image-r-outout"

sizes = {
    "small": (200, 200),
    "medium": (500, 500),
    "large": (1000, 1000)
}


def lambda_handler(event, context):

    try:
        record = event["Records"][0]

        input_bucket = record["s3"]["bucket"]["name"]
        input_key = record["s3"]["object"]["key"]

        print("Input bucket:", input_bucket)
        print("Input file:", input_key)

        # Download original image from S3
        response = s3_client.get_object(
            Bucket=input_bucket,
            Key=input_key
        )

        image_data = response["Body"].read()

        # Open image using Pillow
        image = Image.open(BytesIO(image_data))
        image.load()

        print("Original image:", image.size)

        # Create multiple image sizes
        for size_name, size in sizes.items():

            print("Creating", size_name, size)

            resized_image = image.copy()

            # Maintain aspect ratio
            resized_image.thumbnail(size)

            output_buffer = BytesIO()

            # Convert to RGB for JPEG compatibility
            if resized_image.mode in ("RGBA", "P"):
                resized_image = resized_image.convert("RGB")

            # Save resized image as JPEG
            resized_image.save(
                output_buffer,
                format="JPEG",
                quality=90
            )

            output_buffer.seek(0)

            # Create output filename
            original_name = os.path.splitext(input_key)[0]
            output_key = f"{original_name}_{size_name}.jpg"

            print("Uploading to:", OUTPUT_BUCKET)
            print("Output file:", output_key)

            # Upload resized image to output S3 bucket
            s3_client.put_object(
                Bucket=OUTPUT_BUCKET,
                Key=output_key,
                Body=output_buffer.getvalue(),
                ContentType="image/jpeg"
            )

            print("UPLOAD SUCCESS:", output_key)

        return {
            "statusCode": 200,
            "body": json.dumps("Images resized successfully")
        }

    except Exception as e:

        print("ERROR:", str(e))

        return {
            "statusCode": 500,
            "body": json.dumps(str(e))
        }