from typing import List

from pydantic import BaseModel


class VolumeRes(BaseModel):
    kind: str
    id: str
    etag: str
    selfLink: str
    volumeInfo: dict


class Volumes(BaseModel):
    volumes: List[VolumeRes]
