from typing import Annotated

from fastapi import Depends

from app.api.deps.settings import SettingsDep
from app.infrastructure.storage.factory import create_object_storage
from app.infrastructure.storage.protocol import ObjectStorage


def get_object_storage(settings: SettingsDep) -> ObjectStorage:
    return create_object_storage(settings)


ObjectStorageDep = Annotated[
    ObjectStorage,
    Depends(get_object_storage),
]
