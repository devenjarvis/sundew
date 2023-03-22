import glob
import importlib
import importlib.util
import os
import sys
from pathlib import Path

import typer

from sundew import test
from sundew.config import config

app = typer.Typer()

import sys


class DebugFinder:
    @classmethod
    def find_spec(cls, name, path, target=None):
        print(f"Importing {name!r}")
        return None


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

    class ModuleFinder:
        @classmethod
        def find_spec(cls, name, path, target=None):
            module_path = module
            # Back up until we get to the root of the project directory
            while "tests" in str(module_path):
                module_path = module_path.parent

            # If we're testing a module
            module_init = module_path / name / "__init__.py"
            if module_init.exists():
                # If there is an __init__.py
                if spec := importlib.util.spec_from_file_location(name, module_init):
                    return spec

            # If we're testing a script, look around for it
            if possible_import := glob.glob(
                f"{module_path}/**/{name}*py", recursive=True
            ):
                # If there is an __init__.py
                if spec := importlib.util.spec_from_file_location(
                    name, Path(possible_import[0])
                ):
                    return spec

            return None

    # Import user's code from tests
    sys.meta_path.append(ModuleFinder)

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
    elif spec := importlib.util.spec_from_file_location("module.name", module):
        imported_module = importlib.util.module_from_spec(spec)
        sys.modules["module.name"] = imported_module
        if spec.loader:
            spec.loader.exec_module(imported_module)
        else:
            ...
    else:
        ...

    test.run(function_name=function, enable_auto_test_writer=auto_test_writer)
