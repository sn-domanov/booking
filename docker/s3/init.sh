#!/usr/bin/env sh

set -eu

echo "Initializing S3 bucket: $S3_BUCKET"

if ! aws s3api head-bucket \
    --bucket "$S3_BUCKET" \
    --endpoint-url "$S3_ENDPOINT_URL"
then
    aws s3api create-bucket \
        --bucket "$S3_BUCKET" \
        --endpoint-url "$S3_ENDPOINT_URL"
fi

echo "Configuring public read access"

cat >/tmp/public-read-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicRead",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::$S3_BUCKET/*"
    }
  ]
}
EOF

aws s3api put-bucket-policy \
    --bucket "$S3_BUCKET" \
    --endpoint-url "$S3_ENDPOINT_URL" \
    --policy file:///tmp/public-read-policy.json

echo "S3 bucket initialized: $S3_BUCKET"