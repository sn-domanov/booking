from typing import Annotated

from fastapi import Depends

from app.api.deps.settings import SettingsDep
from app.infrastructure.storage.protocol import ObjectStorage
from app.infrastructure.storage.s3 import S3ObjectStorage


def get_object_storage(settings: SettingsDep) -> ObjectStorage:
    return S3ObjectStorage(
        settings=settings.s3,
    )


ObjectStorageDep = Annotated[
    ObjectStorage,
    Depends(get_object_storage),
]
