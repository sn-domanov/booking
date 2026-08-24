from app.core.config import Settings
from app.infrastructure.storage.protocol import ObjectStorage
from app.infrastructure.storage.s3 import S3ObjectStorage


def create_object_storage(settings: Settings) -> ObjectStorage:
    return S3ObjectStorage(settings=settings.s3)
