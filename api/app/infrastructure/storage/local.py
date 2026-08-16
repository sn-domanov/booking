from pathlib import Path

from app.core.config import Settings


class LocalObjectStorage:
    def __init__(self, settings: Settings) -> None:
        self.root = Path(settings.media_root)
        self.base_url = settings.media_base_url

    async def put(
        self,
        *,
        storage_key: str,
        content: bytes,
        content_type: str,
    ) -> None:
        path = self._path(storage_key)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_bytes(content)

    async def delete(
        self,
        *,
        storage_key: str,
    ) -> None:
        self._path(storage_key).unlink(
            missing_ok=True,
        )

    def get_url(
        self,
        *,
        storage_key: str,
    ) -> str:
        return f"{self.base_url}/{storage_key}"

    def _path(self, storage_key: str) -> Path:
        return self.root / storage_key
