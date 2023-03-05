from sundew.test import test
from sundew.test_writer import (
    build_import_string,
    build_test_strings,
    generate_naive_function_import,
    write_tests_to_file,
)

test(build_import_string)(
    kwargs={"generated_test_file_imports": {("sundew.test_writer", "write_tests_to_file"), ("sundew.test_writer", "build_test_strings"), ("sundew.test_writer", "generate_naive_function_import"), ("sundew.test_writer", "build_import_string")}},
    returns="from sundew.test import test\nfrom sundew.test_writer import (\n\tbuild_import_string,\n\tbuild_test_strings,\n\tgenerate_naive_function_import,\n\twrite_tests_to_file,\n)\n\n",
)
test(build_test_strings)(
    kwargs={"fn_tests": []},
)
test(generate_naive_function_import)(
    kwargs={"mock_name": "build_import_string"},
    returns=("sundew.test_writer", "build_import_string"),
)
test(generate_naive_function_import)(
    kwargs={"mock_name": "build_test_strings"},
    returns=("sundew.test_writer", "build_test_strings"),
)
test(generate_naive_function_import)(
    kwargs={"mock_name": "generate_naive_function_import"},
    returns=("sundew.test_writer", "generate_naive_function_import"),
)
test(generate_naive_function_import)(
    kwargs={"mock_name": "write_tests_to_file"},
    returns=("sundew.test_writer", "write_tests_to_file"),
)
