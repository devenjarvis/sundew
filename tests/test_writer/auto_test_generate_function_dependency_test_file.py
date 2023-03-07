from pathlib import PosixPath
from sundew.test import test
from sundew.test_writer import (
    build_file_path,
    build_import_string,
    build_test_strings,
    generate_function_dependency_test_file,
)

test(build_file_path)(
    kwargs={"fn": generate_function_dependency_test_file},
    returns=PosixPath(
        "/Users/devenjarvis/Code/sundew/tests/test_writer/auto_test_generate_function_dependency_test_file.py"
    ),
)
test(build_import_string)(
    kwargs={"generated_test_file_imports": set()},
    returns="from sundew.test import test\n\n",
)
test(build_test_strings)(
    kwargs={"fn_tests": set()},
)
