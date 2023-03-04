from sundew.test import test
from sundew.test_writer import (
    build_import_string,
    build_test_strings,
    generate_naive_function_import,
    write_tests_to_file,
)

test(build_import_string)(
    kwargs={"generated_test_file_imports": {("sundew.test_writer", "write_tests_to_file"), ("sundew.test_writer", "build_test_strings"), ("sundew.test_writer", "build_import_string"), ("sundew.test_writer", "generate_naive_function_import")}},
    returns="from sundew.test import test\nfrom sundew.test_writer import (\n\tbuild_import_string,\n\tbuild_test_strings,\n\tgenerate_naive_function_import,\n\twrite_tests_to_file,\n)\n\n",
)
test(generate_naive_function_import)(
    kwargs={"mock_name": "write_tests_to_file"},
    returns=("sundew.test_writer", "write_tests_to_file"),
)
test(generate_naive_function_import)(
    kwargs={"mock_name": "build_import_string"},
    returns=("sundew.test_writer", "build_import_string"),
)
test(generate_naive_function_import)(
    kwargs={"mock_name": "generate_naive_function_import"},
    returns=("sundew.test_writer", "generate_naive_function_import"),
)
test(generate_naive_function_import)(
    kwargs={"mock_name": "build_test_strings"},
    returns=("sundew.test_writer", "build_test_strings"),
)
test(build_test_strings)(
    kwargs={"fn_tests": [FunctionTest(function=<function build_import_string at 0x10693fb00>, location="", kwargs={"generated_test_file_imports": {("sundew.test_writer", "write_tests_to_file"), ("sundew.test_writer", "build_test_strings"), ("sundew.test_writer", "build_import_string"), ("sundew.test_writer", "generate_naive_function_import")}}, patches={}, returns="from sundew.test import test\nfrom sundew.test_writer import (\n\tbuild_import_string,\n\tbuild_test_strings,\n\tgenerate_naive_function_import,\n\twrite_tests_to_file,\n)\n\n", setup=set(), side_effects=[])]},
    returns="test(build_import_string)(\n\tkwargs={\"generated_test_file_imports\": {(\"sundew.test_writer\", \"write_tests_to_file\"), (\"sundew.test_writer\", \"build_test_strings\"), (\"sundew.test_writer\", \"build_import_string\"), (\"sundew.test_writer\", \"generate_naive_function_import\")}},\n\treturns=\"from sundew.test import test\\nfrom sundew.test_writer import (\\n\\tbuild_import_string,\\n\\tbuild_test_strings,\\n\\tgenerate_naive_function_import,\\n\\twrite_tests_to_file,\\n)\\n\\n\",\n)\n",
)
test(build_test_strings)(
    kwargs={"fn_tests": []},
)
test(build_test_strings)(
    kwargs={"fn_tests": [FunctionTest(function=<function generate_naive_function_import at 0x1069c8220>, location="", kwargs={"mock_name": "generate_naive_function_import"}, patches={}, returns=("sundew.test_writer", "generate_naive_function_import"), setup=set(), side_effects=[]), FunctionTest(function=<function generate_naive_function_import at 0x1069c8220>, location="", kwargs={"mock_name": "build_test_strings"}, patches={}, returns=("sundew.test_writer", "build_test_strings"), setup=set(), side_effects=[]), FunctionTest(function=<function generate_naive_function_import at 0x1069c8220>, location="", kwargs={"mock_name": "build_import_string"}, patches={}, returns=("sundew.test_writer", "build_import_string"), setup=set(), side_effects=[]), FunctionTest(function=<function generate_naive_function_import at 0x1069c8220>, location="", kwargs={"mock_name": "write_tests_to_file"}, patches={}, returns=("sundew.test_writer", "write_tests_to_file"), setup=set(), side_effects=[]), FunctionTest(function=<function generate_naive_function_import at 0x1069c8220>, location="", kwargs={"mock_name": "write_tests_to_file"}, patches={}, returns=("sundew.test_writer", "write_tests_to_file"), setup=set(), side_effects=[]), FunctionTest(function=<function generate_naive_function_import at 0x1069c8220>, location="", kwargs={"mock_name": "build_import_string"}, patches={}, returns=("sundew.test_writer", "build_import_string"), setup=set(), side_effects=[]), FunctionTest(function=<function generate_naive_function_import at 0x1069c8220>, location="", kwargs={"mock_name": "generate_naive_function_import"}, patches={}, returns=("sundew.test_writer", "generate_naive_function_import"), setup=set(), side_effects=[]), FunctionTest(function=<function generate_naive_function_import at 0x1069c8220>, location="", kwargs={"mock_name": "build_test_strings"}, patches={}, returns=("sundew.test_writer", "build_test_strings"), setup=set(), side_effects=[])]},
    returns="test(generate_naive_function_import)(\n\tkwargs={\"mock_name\": \"write_tests_to_file\"},\n\treturns=(\"sundew.test_writer\", \"write_tests_to_file\"),\n)\ntest(generate_naive_function_import)(\n\tkwargs={\"mock_name\": \"build_import_string\"},\n\treturns=(\"sundew.test_writer\", \"build_import_string\"),\n)\ntest(generate_naive_function_import)(\n\tkwargs={\"mock_name\": \"generate_naive_function_import\"},\n\treturns=(\"sundew.test_writer\", \"generate_naive_function_import\"),\n)\ntest(generate_naive_function_import)(\n\tkwargs={\"mock_name\": \"build_test_strings\"},\n\treturns=(\"sundew.test_writer\", \"build_test_strings\"),\n)\n",
)
