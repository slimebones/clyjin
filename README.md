# Clyjin
System configuration toolbox

## Modules
Clyjin has set of builtin modules to work with, to call a module use:
```bash
python3 -m clyjin {module_name} {module_args}
```

### modules.API
Module deploying web server to display OpenAPI (A.K.A Swagger) specification UI
for set of paths to api entrypoints defined in given file.

Usage:
```bash
python3 -m clyjin api -f {path/to/file/with/api/paths.txt}
```

Structure of `paths.txt` might be something like:
```txt
/home/user/project1/api/main.yml
/home/user/project2/api/main.yml
/home/user/project3/api/main.yml
```

All paths defined in `paths.txt` are fetched, and if they hold correct OpenAPI
yaml spec, UI representation is built.

It is mandatory for now for API entrypoint to hold `info.title` info inside
according entrypoint spec. This is required to build route to this file.

For example, `main.yml`:
```yaml
openapi: '3.0.2'
info:
    title: MyProject
    version: package
...
```
will produce OpenAPI specification on route `/myproject` (or any cased route,
e.g. `/MyPrOjEcT` since lower casing is performed before api names matching).

> *⚠️ WARNING*<br>
>   Accessing raw yaml files for main entrypoint and related dependencies is
>   allowed across all filesystem of web-server's host (of course, where user
>   launched the web-server has an access). Although, the validation for
>   having exactly this api specified in `paths.txt` is done, this is not the
>   best practice to have, because validation is checking and "pinging"
>   requested target file.
>   <br>
>   <br>
>   Use on your own risk in public-faced servers.

#### Important notes
- Unfortunately, folder structure inside directory with entrypoint specified
is not allowed. This won't pass validation for referenced yaml files.
I plan to fix this in future releases

- And yes, only yaml formats supported for now

### modules.Boot
*[IN DEVELOPMENT]* Flexible system configurations from apps installation to own
settings applying.

