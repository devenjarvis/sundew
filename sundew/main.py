import glob
import importlib
import importlib.util
import os
import sys
from importlib.machinery import ModuleSpec
from pathlib import Path
from typing import Optional

import typer

from sundew import test_runner
from sundew.config import config

app = typer.Typer()


@app.command()
def run(  # noqa: C901
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
        def find_spec(
            cls, name: str, path, target=None  # noqa: all
        ) -> Optional[ModuleSpec]:
            module_path = module
            # Back up until we get to the root of the project directory
            while "tests" in str(module_path):
                module_path = module_path.parent

            # If we're testing a module
            module_init = module_path / name / "__init__.py"
            if module_init.exists():
                spec = importlib.util.spec_from_file_location(name, module_init)
                # If there is an __init__.py
                if spec:
                    return spec

            # If we're testing a script, look around for it
            if possible_import := glob.glob(
                f"{module_path}/**/{name}*py", recursive=True
            ):
                spec = importlib.util.spec_from_file_location(
                    name, Path(possible_import[0])
                )
                if spec:
                    return spec

            return None

    # Import user's code from tests
    sys.meta_path.append(ModuleFinder)

    # Load test files in provided path
    if module.is_dir():
        for dirpath, _, fnames in os.walk(module):
            for f in fnames:
                if f.endswith(".py"):
                    if spec := importlib.util.spec_from_file_location(
                        f[:-3],
                        Path(dirpath) / f,
                    ):
                        imported_module = importlib.util.module_from_spec(spec)
                        sys.modules[f[:-3]] = imported_module
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

    test_runner.run(function_name=function, enable_auto_test_writer=auto_test_writer)
