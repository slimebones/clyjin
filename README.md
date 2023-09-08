# 🛠️ Clyjin

Provides a core for building plugins with CLI interfaces.

## 👩‍🏭 Installation

If you want to install some plugin, you probably need only one command:
```sh
pip install clyjin_someplugin
```

Additional steps might be required, consult with plugin's documentation for
details.

If you want to install Clyjin Core to develop own plugin, you might want to
start with:
```sh
pip install clyjin
```

Or, using [poetry](https://python-poetry.org/):
```sh
poetry add clyjin
```

## 📓 Getting Started

To get grasp of Clyjin's functionality we'll develop a new plugin called
`Hello`.

First, you need to create a new Python project which name starts with
`clyjin_`, e.g. `clyjin_hello`.

Structure of the project might look like:
```
.
├── .venv
├── clyjin_hello/
│   ├── __init__.py
│   └── _main.py
├── poetry.lock
└── pyproject.toml
```

Main class of your plugin-project is `Plugin`. Clyjin on initialization makes
imports of your defined plugin with statement like
`from clyjin_hello import MainPlugin`.

This means you need to define a variable called `MainPlugin` in your
`__init__.py` pointing to your plugin class:
```python
# clyjin_hello/__init__.py
from clyjin_hello._main import HelloPlugin

MainPlugin = HelloPlugin
```

That said, our plugin can be defined wherever we want, but we should reference
it to be importable from our root Python package via name `MainPlugin`.

The plugin itself in our example is defined within `_main.py`:
```python
# clyjin_hello/main.py
from clyjin.base import Plugin, PluginInitializeData

class HelloPlugin(Plugin):
    Name = "hello"
    ModuleClasses = [
        RootModule,
        GreetingsModule
    ]
    # retrieve version of our package dynamically
    Version = importlib.metadata.version("clyjin_hello")

    @classmethod
    async def initialize(
        clas,
        data: PluginInitializeData
    ) -> None:
        # our custom initialization logic
        ...
```

Let's do a quick overview of the things happened here:
- `Name = "hello"` - defines a callable name for our plugin. It will be used
    as a main entrypoint in CLI and in other references.
- `ModuleClasses = [...]` - list of module classes defined for your plugin.
- `Version = importlib.metadata.version("clyjin_hello")` - version of our
    plugin. In this case retrieved dynamically from package's data.
- `async def initialize(...)` - extra initialization logic for our plugin.

Our plugin's modules can be defined as follows:
```python
from clyjin.base import Module, ModuleData

class RootModule(Module[MyRootArgs, MyRootConfig]):
    Name = "$root"
    Description = "show count of hello words said"
    Args = MyRootArgs(
        output_dir=ModuleArg[str](
            names=["output_dir"],
            type=Path,
            help="where to write the result output"
        )
        is_world_only=ModuleArg[bool](
            names=["-w", "--world"],
            action="store_true",
            type=bool,
            argparse_type=type,
            help="whether should count only \"hello world\" messages"
        )
    )

    def __init__(
        self,
        module_data: ModuleData[MyRootArgs, MyRootConfig]
    ) -> None:
        super().__init__(module_data)

        # ... do whatever you want on your module's initialization
        # module data fields is available under self protected attributes,
        # e.g. self._args.output_dir or self._config as well as additional
        # helper variables, like self._rootdir

    async def execute(self) -> None:
        # ... called on module's execution
        # args values can be accessed like `self.args.output_dir.value`
        ...
```

- `class RootModule(Module[MyRootArgs, MyRootConfig])` - declares our module's
    class, inheriting it from generic module with setting as first argument
    our Args class and as second argument our Config class.
- `Name = "$root"` - special name for a module indicates that this module is a
    root module. Root modules are called directly under Plugin's namespace,
    e.g. `clyjin hello ...`, while other modules are called like
    `clyjin hello.module_name ...`.
- `Description = "..."` - description of the module, appeared at least in CLI
    help output
- `Args = MyRootArgs(...)` - initialization of our module's args class.
    Args class contains information about CLI arguments supported by our
    module. It's structure is mostly similar like arguments passed to
    argparse.add_argument.
- `def __init__(...)` - initialization method of our module accepting
    ModuleData object as first argument. ModuleData contains information about
    args, config and some extra helper fields, such as `rootdir`. Insider our
    Module super class all these fields are set to protected instance's
    variables, like `self._rootdir` making them available for further usage.
- `async def execute(self) -> None` - method called if Clyjin core decided to
    chose this module to execute next request. Typically, if you need to
    access CLI arguments passed within this method, you will need to use
    `this.args.your_cli_arg.value` statement.

You can define as many modules as you need in your `Plugin.ModuleClasses`
field, but you can have only one root module, i.e. module with name `$root`,
and other module names should be all unique.

To call your plugin anywhere, you need to install `clyjin` and `clyjin_hello`
(i.e. your plugin) and issue a CLI command:
```sh
clyjin <your_plugin_name>.<your_module_name> <...arguments>
```

For example for our imaginary GreetingsModule, which is part of HelloPlugin,
we might issue a command:
```sh
clyjin clyjin_hello.greetings --to world --from $USER
```

## 💪 Advanced

### 📁 System directories

[in process of writing, take some coffee ☕]

## 🔶 Official Plugins

- [📑 Clyjin Templates](https://github.com/ryzhovalex/clyjin_templates)
- [⚙️ Clyjin Make](https://github.com/ryzhovalex/clyjin_make)
