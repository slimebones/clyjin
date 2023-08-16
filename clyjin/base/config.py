from typing import TypeVar

from clyjin.base.model import Model

ConfigType = TypeVar("ConfigType", bound="Config")


class Config(Model):
    pass
