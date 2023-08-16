from typing import TypeVar

from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound="Model")
class Model(BaseModel):
    pass
