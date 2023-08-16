from cv2.typing import MatLike
from pydantic import BaseModel, Field


class Image(BaseModel):
    objects: list[str] = Field(default_factory=list)
    img: MatLike
