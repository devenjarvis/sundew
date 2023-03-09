from pathlib import Path

from sundew.test import test
from sundew.test_writer import (
    build_file_path,
    build_import_string,
    build_test_strings,
    generate_function_dependency_test_file,
    generate_naive_function_import,
)
from sundew.types import FunctionTest

test(build_file_path)(
    kwargs={"fn": generate_function_dependency_test_file},
    returns=Path.home()
    / "Code/sundew/tests/test_writer/auto_test_generate_function_dependency_test_file.py",
)
test(build_import_string)(
    kwargs={"generated_test_file_imports": set()},
    returns="from sundew.test import test\n\n",
)
test(build_test_strings)(
    kwargs={"fn_tests": set()},
)
test(generate_naive_function_import)(
    kwargs={
        "mock_name": "build_file_path",
        "mock_test_functions": {
            FunctionTest(
                function=build_file_path,
                kwargs={"fn": generate_function_dependency_test_file},
                patches={},
                returns=Path.home()
                / "Code/sundew/tests/test_writer/auto_test_generate_function_dependency_test_file.py",  # noqa: E501
                setup=set(),
                side_effects=[],
            )
        },
    },
    returns=[
        ("sundew.test_writer", "build_file_path"),
        ("sundew.test_writer", "generate_function_dependency_test_file"),
        ("pathlib", "PosixPath"),
    ],
)
test(generate_naive_function_import)(
    kwargs={
        "mock_name": "generate_naive_function_import",
        "mock_test_functions": {
            FunctionTest(
                function=generate_naive_function_import,
                kwargs={
                    "mock_name": "build_import_string",
                    "mock_test_functions": {
                        FunctionTest(
                            function=build_import_string,
                            kwargs={
                                "generated_test_file_imports": {
                                    ("sundew.test_writer", "build_file_path"),
                                    ("sundew.test_writer", "build_import_string"),
                                    ("sundew.test_writer", "build_test_strings"),
                                    (
                                        "sundew.test_writer",
                                        "generate_function_dependency_test_file",
                                    ),
                                    ("sundew.types", "FunctionTest"),
                                    ("pathlib", "PosixPath"),
                                    (
                                        "sundew.test_writer",
                                        "generate_naive_function_import",
                                    ),
                                }
                            },
                            patches={},
                            returns="from pathlib import PosixPath\nfrom sundew.test import test\nfrom sundew.test_writer import (\n\tbuild_file_path,\n\tbuild_import_string,\n\tbuild_test_strings,\n\tgenerate_function_dependency_test_file,\n\tgenerate_naive_function_import,\n)\nfrom sundew.types import FunctionTest\n\n",  # noqa: E501
                            setup=set(),
                            side_effects=[],
                        ),
                        FunctionTest(
                            function=build_import_string,
                            kwargs={"generated_test_file_imports": set()},
                            patches={},
                            returns="from sundew.test import test\n\n",
                            setup=set(),
                            side_effects=[],
                        ),
                    },
                },
                patches={},
                returns=[("sundew.test_writer", "build_import_string")],
                setup=set(),
                side_effects=[],
            ),
            FunctionTest(
                function=generate_naive_function_import,
                kwargs={
                    "mock_name": "generate_naive_function_import",
                    "mock_test_functions": set(),
                },
                patches={},
                returns=[
                    ("sundew.test_writer", "generate_naive_function_import"),
                    ("sundew.types", "FunctionTest"),
                    ("sundew.types", "FunctionTest"),
                    ("sundew.types", "FunctionTest"),
                ],
                setup=set(),
                side_effects=[],
            ),
            FunctionTest(
                function=generate_naive_function_import,
                kwargs={
                    "mock_name": "build_file_path",
                    "mock_test_functions": {
                        FunctionTest(
                            function=build_file_path,
                            kwargs={"fn": generate_function_dependency_test_file},
                            patches={},
                            returns=Path.home()
                            / "Code/sundew/tests/test_writer/auto_test_generate_function_dependency_test_file.py",  # noqa: E501
                            setup=set(),
                            side_effects=[],
                        )
                    },
                },
                patches={},
                returns=[
                    ("sundew.test_writer", "build_file_path"),
                    ("sundew.test_writer", "generate_function_dependency_test_file"),
                    ("pathlib", "PosixPath"),
                ],
                setup=set(),
                side_effects=[],
            ),
            FunctionTest(
                function=generate_naive_function_import,
                kwargs={
                    "mock_name": "build_test_strings",
                    "mock_test_functions": {
                        FunctionTest(
                            function=build_test_strings,
                            kwargs={"fn_tests": set()},
                            patches={},
                            returns="",
                            setup=set(),
                            side_effects=[],
                        )
                    },
                },
                patches={},
                returns=[("sundew.test_writer", "build_test_strings")],
                setup=set(),
                side_effects=[],
            ),
        },
    },
    returns=[
        ("sundew.test_writer", "generate_naive_function_import"),
        ("sundew.types", "FunctionTest"),
        ("sundew.types", "FunctionTest"),
        ("sundew.types", "FunctionTest"),
        ("sundew.types", "FunctionTest"),
    ],
)
test(generate_naive_function_import)(
    kwargs={
        "mock_name": "build_import_string",
        "mock_test_functions": {
            FunctionTest(
                function=build_import_string,
                kwargs={
                    "generated_test_file_imports": {
                        ("sundew.test_writer", "build_file_path"),
                        ("sundew.test_writer", "build_import_string"),
                        ("sundew.test_writer", "build_test_strings"),
                        (
                            "sundew.test_writer",
                            "generate_function_dependency_test_file",
                        ),
                        ("sundew.types", "FunctionTest"),
                        ("pathlib", "PosixPath"),
                        ("sundew.test_writer", "generate_naive_function_import"),
                    }
                },
                patches={},
                returns="from pathlib import PosixPath\nfrom sundew.test import test\nfrom sundew.test_writer import (\n\tbuild_file_path,\n\tbuild_import_string,\n\tbuild_test_strings,\n\tgenerate_function_dependency_test_file,\n\tgenerate_naive_function_import,\n)\nfrom sundew.types import FunctionTest\n\n",  # noqa: E501
                setup=set(),
                side_effects=[],
            ),
            FunctionTest(
                function=build_import_string,
                kwargs={"generated_test_file_imports": set()},
                patches={},
                returns="from sundew.test import test\n\n",
                setup=set(),
                side_effects=[],
            ),
        },
    },
    returns=[("sundew.test_writer", "build_import_string")],
)
test(generate_naive_function_import)(
    kwargs={
        "mock_name": "build_test_strings",
        "mock_test_functions": {
            FunctionTest(
                function=build_test_strings,
                kwargs={"fn_tests": set()},
                patches={},
                returns="",
                setup=set(),
                side_effects=[],
            )
        },
    },
    returns=[("sundew.test_writer", "build_test_strings")],
)
