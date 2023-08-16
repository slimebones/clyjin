from clyjin.core.modules.base import CoreModule
from clyjin.core.modules.configurator.configurator import (
    ConfiguratorCoreModule,
)

CORE_MODULE_CLASSES: list[type[CoreModule]] = [
    ConfiguratorCoreModule,
]
