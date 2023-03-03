import importlib
import importlib.util
import os
import sys
from pathlib import Path

import typer

from sundew import test
from sundew.config import config

app = typer.Typer()


@app.command()
def run(
    module: Path,
    function: str = typer.Option(  # noqa: B008
        "",
        "--function",
        "-f",
        help="Run all tests for this function.",
    ),
    auto_test_writer: bool = typer.Option(  # noqa: B008, FBT001
        False,  # noqa: FBT003
        "--auto-test-writer",
        "-a",
        help="Enable the automatic test writer.",
    ),
) -> None:
    config.modules = {"module.name"}

    if module.is_dir():
        for dirpath, _, fnames in os.walk(module):
            for f in fnames:
                if f.endswith(".py"):
                    if spec := importlib.util.spec_from_file_location(
                        "module.name",
                        Path(dirpath) / f,
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

    test.run(function_name=function, enable_auto_test_writer=auto_test_writer)


if __name__ == "__main__":
    app()
