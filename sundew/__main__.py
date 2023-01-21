import importlib
import importlib.util
import os
import sys

import typer

from sundew import test
from sundew.config import config

app = typer.Typer()


@app.command()
def run(
    module: str,
    function: str = typer.Option(  # noqa: B008
        "",
        help="Run all tests for this function.",
    ),
) -> None:
    config.modules = {"module.name"}

    if os.path.isdir(module):
        for dirpath, _, fnames in os.walk(module):
            for f in fnames:
                if f.endswith(".py"):
                    if spec := importlib.util.spec_from_file_location(
                        "module.name",
                        os.path.join(dirpath, f),
                    ):
                        imported_module = importlib.util.module_from_spec(spec)
                        sys.modules["module.name"] = imported_module
                        if spec.loader:
                            spec.loader.exec_module(imported_module)
                        else:
                            ...
                    else:
                        ...
    else:
        if spec := importlib.util.spec_from_file_location("module.name", module):
            imported_module = importlib.util.module_from_spec(spec)
            sys.modules["module.name"] = imported_module
            if spec.loader:
                spec.loader.exec_module(imported_module)
            else:
                ...
        else:
            ...

    test.run(function_name=function)


if __name__ == "__main__":
    app()
