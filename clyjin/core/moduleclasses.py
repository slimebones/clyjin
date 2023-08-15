from clyjin.core.modules.base import CoreModule
from clyjin.core.modules.register import RegisterCoreModule


CORE_MODULE_CLASSES: list[type[CoreModule]] = [
    RegisterCoreModule,
]
