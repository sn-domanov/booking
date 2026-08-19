import boto3
from fastapi.concurrency import run_in_threadpool

from app.core.config import S3Settings


class S3ObjectStorage:
    def __init__(
        self,
        *,
        settings: S3Settings,
    ) -> None:
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.endpoint_url,
            region_name=settings.region,
            aws_access_key_id=settings.access_key,
            aws_secret_access_key=settings.secret_key.get_secret_value(),
        )
        self.bucket = settings.bucket
        self.public_base_url = settings.public_base_url.rstrip("/")

    async def put(
        self,
        *,
        storage_key: str,
        content: bytes,
        content_type: str,
    ) -> None:
        await run_in_threadpool(
            self.client.put_object,
            Bucket=self.bucket,
            Key=storage_key,
            Body=content,
            ContentType=content_type,
        )

    async def delete(
        self,
        *,
        storage_key: str,
    ) -> None:
        await run_in_threadpool(
            self.client.delete_object,
            Bucket=self.bucket,
            Key=storage_key,
        )

    def get_url(
        self,
        *,
        storage_key: str,
    ) -> str:
        # TODO: consider virtual-hosted style http://{bucket}.localhost:9000/{key}
        return f"{self.public_base_url}/{self.bucket}/{storage_key}"
