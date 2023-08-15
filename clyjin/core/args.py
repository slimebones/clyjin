from clyjin.base.moduleargs import ModuleArg, ModuleArgs
from clyjin.core.action import CoreAction


class CoreArgs(ModuleArgs):
    action: ModuleArg[CoreAction]
