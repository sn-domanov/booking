from typing import Annotated

from fastapi import Depends

from app.api.deps.settings import SettingsDep
from app.infrastructure.storage.local import LocalObjectStorage
from app.infrastructure.storage.protocol import ObjectStorage


def get_object_storage(settings: SettingsDep) -> ObjectStorage:
    return LocalObjectStorage(
        settings=settings,
    )


ObjectStorageDep = Annotated[
    ObjectStorage,
    Depends(get_object_storage),
]
