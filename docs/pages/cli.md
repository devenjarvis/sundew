# Using the CLI

Running tests with sundew can be done easily with the CLI, which is automatically downloaded as a part of the package when you `pip install sundew`. This document details how to use the CLI and the options and features available to you. If you need a quick reference you can also always run:

```bash
sundew --help
```

## Running Tests
The minimal use of the CLI runs all tests in provided directory, and is invoked simply with:

```bash
sundew ./tests
```

In thie case we assume you are in the root of your project and want to run all tests in the `tests` directory. However, you can set the directory to anything you like by providing it as an argument at the end of your CLI command. 

You can set it to a directory:
```bash
sundew ./tests/examples
```

Or a specific test file:
```bash
sundew ./tests/examples/test_async_examples.py
```

Sundew will automatically check all python files within the provided path, recursively, and run all tests defined with sundew's `test()` function. Sundew does not care about the name of your test files and will check all python files.

## Run Tests For a Specific Function

Sundew does not have a concept of test naming, and instead relies on the names of the functions-under-test to narrow down which tests you want to run. Sundew accepts an optional flag, `--function` or `-f`, to run only tests for the provided function name. When used, sundew will still search all python files in the directory provided for sundew tests, but will only run ones for the requested function. In practice this looks like this:

```bash
sundew ./tests -f get_source
```

When you run this you'll see an output similar to `Selected 3/48 tests` indicating that only a subset of the tests identified are being run.

## Automatic Test Writer

A cool feature that is unlocked by the way sundew does testing, is the ability to automatically write regression tests for the sub-functions of a function-under-test. Sundew is able to detect all the other functions that your function-under-test calls, mock those functions, and then use those mocks to capture the `kwargs` and `returns` of each called function. Sundew can then use that information to automatically write tests for those other functions in new test files. Furthermore, sundew will cache those functions and automatically sort them to be called before your original test, meaning the automatically written tests also come with zero cost to your test suite run time. 

To use this functionality you simply add the `--auto-test-writer` or `-a` flag when running the sundew CLI. For example:

```bash
sundew ./tests -a
```