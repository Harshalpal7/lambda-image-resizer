# AWS Lambda Image Resizer

A serverless image-processing project using **AWS Lambda, Amazon S3, Python, and Pillow** to automatically create multiple resized versions of an uploaded image.

## Project Overview

This project automatically processes images uploaded to an Amazon S3 bucket.

When an image is uploaded to the input S3 bucket, an S3 event triggers the AWS Lambda function. The Lambda function downloads the image, processes it using Pillow, and generates three different image sizes:

| Size   | Maximum Dimensions |
| ------ | ------------------ |
| Small  | 200 × 200          |
| Medium | 500 × 500          |
| Large  | 1000 × 1000        |

The resized images are then uploaded to a separate S3 output bucket.

## Architecture

```text
                    Image Upload
                         |
                         v
              +---------------------+
              |      Amazon S3       |
              |    Input Bucket      |
              +----------+----------+
                         |
                         | S3 Event
                         v
              +---------------------+
              |      AWS Lambda      |
              |  Python + Pillow     |
              +----------+----------+
                         |
              +----------+----------+
              |          |           |
              v          v           v
           Small      Medium       Large
          200x200     500x500     1000x1000
              |          |           |
              +----------+-----------+
                         |
                         v
              +---------------------+
              |      Amazon S3       |
              |    Output Bucket     |
              +---------------------+
```

## Technologies Used

* **Python**
* **AWS Lambda**
* **Amazon S3**
* **AWS IAM**
* **Boto3**
* **Pillow (PIL)**
* **Git**
* **GitHub**

## AWS Services

### Amazon S3

Amazon S3 is used for:

* Storing the original uploaded image
* Triggering the Lambda function
* Storing the resized output images

### AWS Lambda

AWS Lambda executes the image-processing code automatically when a new image is uploaded to the input S3 bucket.

### AWS IAM

An IAM execution role provides Lambda with the required permissions to read images from the input S3 bucket and upload processed images to the output S3 bucket.

## How It Works

### 1. Upload Image

An image is uploaded to the input S3 bucket.

```text
Input S3 Bucket
        |
        └── image.jpg
```

### 2. S3 Event Trigger

The S3 bucket generates an event when the image is uploaded.

This event invokes the Lambda function.

### 3. Lambda Reads the Event

The Lambda function identifies:

* Input bucket
* Uploaded file name
* Object key

```python
record = event["Records"][0]

input_bucket = record["s3"]["bucket"]["name"]
input_key = record["s3"]["object"]["key"]
```

### 4. Download Image

The image is downloaded from S3 using Boto3.

```python
response = s3_client.get_object(
    Bucket=input_bucket,
    Key=input_key
)
```

### 5. Process Image

Pillow opens the image and loads it into memory.

```python
image = Image.open(BytesIO(image_data))
image.load()
```

### 6. Generate Multiple Sizes

The project creates three versions:

```python
sizes = {
    "small": (200, 200),
    "medium": (500, 500),
    "large": (1000, 1000)
}
```

The `thumbnail()` method maintains the image's aspect ratio.

### 7. Convert to JPEG

Images with RGBA or palette modes are converted to RGB so they can be saved as JPEG.

```python
if resized_image.mode in ("RGBA", "P"):
    resized_image = resized_image.convert("RGB")
```

### 8. Upload Results

The resized images are uploaded to the output S3 bucket.

Example:

```text
image_small.jpg
image_medium.jpg
image_large.jpg
```

## Example Workflow

Suppose the uploaded image is:

```text
product.jpg
```

Lambda generates:

```text
product_small.jpg
product_medium.jpg
product_large.jpg
```

with maximum dimensions:

```text
Small:   200 × 200
Medium:  500 × 500
Large:   1000 × 1000
```

## Project Structure

```text
lambda-image-resizer/
│
├── lambda_function.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── screenshots/
    ├── s3-buckets.png
    ├── lambda-function.png
    ├── lambda-trigger.png
    └── resized-images.png
```

## Lambda Function

The main application is contained in:

```text
lambda_function.py
```

The function:

1. Receives the S3 event.
2. Identifies the uploaded image.
3. Downloads the image from S3.
4. Opens the image using Pillow.
5. Creates three resized versions.
6. Converts the images to JPEG.
7. Uploads the processed images to the output S3 bucket.
8. Returns a success response.

## IAM Permissions

The Lambda execution role requires appropriate permissions for the S3 buckets.

The main permissions required are:

```text
s3:GetObject
s3:PutObject
```

For production environments, permissions should be restricted to the specific buckets and actions required by the application.

## Error Handling

The Lambda function uses exception handling:

```python
try:
    ...
except Exception as e:
    ...
```

Errors are printed to the Lambda logs and can be investigated using Amazon CloudWatch.

## Screenshots

### S3 Buckets

![S3 Buckets](screenshots/s3-buckets.png)

### Lambda Function

![Lambda Function](screenshots/lambda-function.png)

### S3 Trigger

![Lambda Trigger](screenshots/lambda-trigger.png)

### Resized Images

![Resized Images](screenshots/resized-images.png)

## Key Learning Outcomes

Through this project, I gained practical experience with:

* AWS Lambda
* Amazon S3
* Event-driven architecture
* AWS IAM
* Python
* Boto3
* Pillow image processing
* Serverless application development
* CloudWatch logging
* Git and GitHub
* S3 event triggers

## Future Improvements

Possible improvements include:

* Support for additional image formats
* Image compression
* WebP output
* Automatic deletion of original images
* CloudWatch alarms and monitoring
* Infrastructure deployment using Terraform
* CI/CD using GitHub Actions
* Processing multiple images concurrently
* Using Lambda Layers for Pillow dependencies

## Security

AWS credentials should never be stored in this repository.

Do not upload:

```text
AWS Access Keys
AWS Secret Keys
.env files
AWS credentials
Private keys
```

The Lambda function uses its IAM execution role to access AWS services.

## Author

**Harshal Pal**

Cloud Computing | AWS | DevOps

---

## License

This project is created for educational and portfolio purposes.
