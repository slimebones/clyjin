from typing import List
from clyjin.core.ModuleSpec import ModuleSpec
from clyjin.modules import api, boot

BUILTIN_MODULE_SPECS: List[ModuleSpec] = [
    ModuleSpec("boot", boot.main),
    ModuleSpec("api", api.main)
] 