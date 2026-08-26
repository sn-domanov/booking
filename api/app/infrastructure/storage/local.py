from pathlib import Path

from app.core.config import Settings
from app.core.exceptions import InvalidStorageKeyError


class LocalObjectStorage:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def put(
        self,
        *,
        storage_key: str,
        content: bytes,
        content_type: str,
    ) -> None:
        filepath = self._path_for(storage_key)

        filepath.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        filepath.write_bytes(content)

    async def delete(
        self,
        *,
        storage_key: str,
    ) -> None:
        filepath = self._path_for(storage_key)

        filepath.unlink(
            missing_ok=True,
        )

    def get_url(
        self,
        *,
        storage_key: str,
    ) -> str:
        return f"{self.settings.local_storage.base_url}/{storage_key}"

    def _path_for(self, storage_key: str) -> Path:
        root = self.settings.local_storage.root.resolve()
        filepath = (root / storage_key).resolve()

        if not filepath.is_relative_to(root):
            raise InvalidStorageKeyError("Invalid storage key")

        return filepath
