from collections.abc import Sequence

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

    def get_url(
        self,
        *,
        storage_key: str,
    ) -> str:
        # TODO: consider virtual-hosted style http://{bucket}.localhost:9000/{key}
        return f"{self.public_base_url}/{self.bucket}/{storage_key}"

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

    async def delete_many(
        self,
        *,
        storage_keys: Sequence[str],
    ) -> None:
        if not storage_keys:
            return

        await run_in_threadpool(
            self.client.delete_objects,
            Bucket=self.bucket,
            Delete={
                "Objects": [{"Key": storage_key} for storage_key in storage_keys],
            },
        )

    async def clear(
        self,
        *,
        prefix: str | None = None,
    ) -> None:
        def _clear() -> None:
            paginator = self.client.get_paginator("list_objects_v2")

            for page in paginator.paginate(
                Bucket=self.bucket,
                **({"Prefix": prefix} if prefix else {}),
            ):
                keys = [obj["Key"] for obj in page.get("Contents", [])]

                if keys:
                    self.client.delete_objects(
                        Bucket=self.bucket,
                        Delete={
                            "Objects": [{"Key": key} for key in keys],
                        },
                    )

        await run_in_threadpool(_clear)
