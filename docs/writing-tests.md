# Writing Tests

## Directory Structure
Tests are typically written in python files within a `tests` directory at the root of your project. You can have many files within that directory and can use sub-directories to organize those files to your liking. Sundew is not very opinionated about subdirectories, or how the test files are named so feel free to structure this directory how you'd like. 


## Imports
All tests written in sundew follow a consistent format. Once you've created your first test file (ex: `tests/test_my_app.py`) you can begin writing your first tests. At the top of every test file you'll want an import statement that looks something like:

```python
from sundew import test
import my_app
```
This imports sundew's test function, and the application you want to test. You are welcome to import just a sub-module of your application if that works better for your organization.

## Basic Tests
Basic tests in sundew look like:

```python
test(my_app.my_function)(
    kwargs={"a": 123, "b": "456"},
    returns="123456"
)
```

In this test we specify 3 things.

1. The function we want to test by passing it within `test(...)`
2. The arguments we want to test our function with, passed as a dictionary to `kwargs`
3. The expected return from our function, defined as the argument to `returns`

### kwargs
`kwargs: dict[str, Any] | None = None`

This is a dictionary of paramater, argument pairs that you'd like passed into the function for this test. This follows the standard format for **kwargs and while the parameter names must be strings, the arguments provided can be any type. If an argument is not provided for `kwargs` it defaults to `None` and no arguments will be passed to the function under test.

### returns
`returns: Any | Exception | None = None`

The argument to `returns` can be any type, _including_ an Exception. If you expect your function will fail with an exception for this test, just set `returns` to the expected Exception and sundew will test for that. `returns` defaults to `None` if an argument is not provided. Note, if `returns` is `None` and the function does indeed return something, then the test will fail.

### The Most Basic Test
Some functions take no arguments and return nothing, so technically the simplest test you can write with sundew is:

```python
test(my_app.my_function)()
```

...but that's not very useful is it? In these cases we have other ways to test what's happening within these functions.

## Side Effects
Sometimes tests also, or only, perform "side effects". These are actions taken on data and/or systems outside of the arguments that are passed to the function. We'll discuss how to isolate external systems in the next two sections, but here we'll introduce how we can test the side effects of our function with the `side_effects` parameter. This parameter accepts a list of lambda functions and looks something like this:

```python
test(my_app.my_function)(
    kwargs={"a": 123, "b": "456"},
    returns="123456"
)
```

## Patches


## Setup


## Cache
