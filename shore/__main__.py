from shore.config import config
from shore import test

import typer
import importlib
import importlib.util
import sys
import os


app = typer.Typer()


@app.command()
def run(module: str):
    config.modules = {"module.name"}

    if os.path.isdir(module):
        for dirpath, dnames, fnames in os.walk(module):
            for f in fnames:
                if f.endswith(".py"):
                    spec = importlib.util.spec_from_file_location(
                        "module.name", os.path.join(dirpath, f)
                    )
                    imported_module = importlib.util.module_from_spec(spec)
                    sys.modules["module.name"] = imported_module
                    spec.loader.exec_module(imported_module)
    else:
        spec = importlib.util.spec_from_file_location("module.name", module)
        imported_module = importlib.util.module_from_spec(spec)
        sys.modules["module.name"] = imported_module
        spec.loader.exec_module(imported_module)

    test.run()


if __name__ == "__main__":
    app()
