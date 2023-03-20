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

...but that's not very useful is it? In these cases we're probably working with functions that have "side effect". These are actions taken on data and/or systems outside of the arguments that are passed to the function, which means we cannot test them by simply looking at our function's inputs and output, and we also may want to isolate our function from _actually_ causing those side effects. Sundew comes with simple but powerful ways to isolate and test side effects, and we'll lay the groundwork for doing so over the next few sections.

## Patches
`patches: dict[str, Any] | None = None`

We should first address how to apply patches to our functions. If you're unfamiliar, patches are a way to temporarily replace a function or class with an alternative function or class for the duration of your test. This alternative function or class usually is in place to both isolate our test from calling actual services, and to capture how that function or class is called or what it returns. Today, `patches` encompasses the bulk of mocking functionality in Sundew, and does so by extending the standard library [unittest patch function](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch). The `patches` parameter takes a dictionary of `[str, Any]` where the key is the module path to the target you want to patch, and the value is what you want to patch it with. Sundew then applies each key-value patch as a context manager when running your test to ensure all patches are applied and cleaned up before and after the function-under-test is run. 

For example, if we wanted to capture the output printed from our funtion-under-test, and not actually print it while testing, we might write a sundew test like this:

```python
test(my_app.print_hello)(
    kwargs={"name": "Dave"},
    patches={"sys.stdout": io.StringIO()}
)
```

In this example, we might expect our function to print `"Hello, {name}"`. By patching `stdout` with an `io.StringIO()` we prevent the output from actually being printed, and we've captured that output for us to test! However, that output isn't necessarily returned by our function so we can't just reach for the `returns` parameter, we need something else to test this value....

## Side Effects
`side_effects: list[Callable] | None = None`

Let's look how we can test the side effects of our function with the `side_effects` parameter. If you look at the last section, we introduced the `patches` parameter and used the following test to patch the output of `stdout` expecting to capture maybe a `"Hello, {name}"` being printed. We can extend the test in the last section with our `side_effects` parameter which accepts a list of `callables` - or more specifically a list of :sparkles: lambdas :sparkles:. We'll take a look at our test, and then explain what's going on.

```python
test(my_app.print_hello)(
    kwargs={"name": "Dave"},
    patches={"sys.stdout": io.StringIO()},
    side_effects=[
        lambda _: _.patches["sys.stdout"].getvalue() == "Hello, Dave\n",
    ],
)
```

Our `side_effects` _might_ look a bit ugly at first glance, but when designing sundew I've tried to bias design decisions for familiar-to-existing-devs, vs syntactically-pleasant-but-also-magic when I have to choose. The `lambda` is the only feasible construct within the Python language that let's us define an expression _now_ that we want to run _later_ (after your test is run). We pass this lambda single argument, endearingly named `_`, that has the following attributes:

- `_.patches: dict[str, Any]` which is the same dictionary you gave as the `patches` argument
- Dynamically generated attributes for each `kwarg` so in this case `_.name` which is set to whatever that parameter is equal to when your function is done running.

Now you may be wondering why we named the argument to the lambda `_`, and note **This is the required argument name**. Ultimately it came down to the shortest syntax that didn't feel _too much_ like magic, that your linter won't yell at you about. The keen observer will now be wondering why/how sundew enforces what you name this argument, it should be able to be anything... right? Well sundew does have a _bit_ of magic here, as we parse the AST of these lambdas and convert them into assertions so we're able to provide helpful failure messages when our test fails like:

```bash
FAILURE tests/examples/test_side_effects_example.py:34 - Side-effect '_.patches['sys.stdout'].getvalue() == 'Hello, Dabe\n'' failed because: _.patches['sys.stdout'].getvalue() == Hello, Dave, and Hello, Dave != Hello, Dabe
```

This error would occur if we incorrectly expected the patch to return `Hello, Dabe` in our side_effect à la 
```python
lambda _: _.patches["sys.stdout"].getvalue() == "Hello, Dabe\n",
```

> **Note:** Right now `side_effect` lambdas support all comparison types (`==`, `!=`, `<`, `>`, `<=`, `>=`, `is`, `is not`, `in`, and `not in`), but currently sundew only supports 1 comparison per lamdbda. You can break up lambdas with multiple comparisons into multiple `side_effect` lambdas with a single comparison each.

## Setup
`setup: set[Callable[[], _GeneratorContextManager[Any]]] | None = None`

Sometimes you want to make sure something happens before your function runs, usually to setup some other structure your function depends on. Sundew has basic support for this with the `setup` parameter which takes a list of **generator** functions. These functions must `yield` and provide an opportunity, although it is not enforced, for you to perform setup code with the standard `try, yield, finally` syntax. If you come from `pytest` you can think of these `setup` functions as yield fixtures, although they are not nearly to feature parity _yet_. I made the choice to only support generator functions because of how easy they make extra isolation, if you so choose to take it, to ensure cleanup happens for anything set up before your next test runs. 

You may define a setup function like this (taken from one of sundew's test_writer tests):
```python
from contextlib import contextmanager
from tests import fixtures

@contextmanager
def extend_config_with_dependent_functions() -> Iterator:
    try:
        new_graph = setup_test_graph_with_dependency()
        config.test_graph.extend(new_graph)

        yield new_graph
    finally:
        # remove the part of the graph we added
        for key in new_graph.functions:
            del config.test_graph.functions[key]
```

I usually store these in a separate file called `fixtures.py` within the `tests` directory, but sundew is not particular about how you structure this either. In this fixture we can see where we setup a new `Graph` called `new_graph` (original!) with dependencies we want to test, and extend our `config.test_graph` with it. We then `yield` that graph, although it isn't used anywhere. Once our test completes, wether it suceeds or fails, the `finally` block will be run and we will remove the keys from `new_graph` so as to not polute `config.test_graph` for any future test runs. The test that uses this generator function for `setup` looks like this:

```python
test(test_writer.mock_function_dependencies)(
    setup={fixtures.extend_config_with_dependent_functions},
    kwargs={"fn": fixtures.callee_func, "stack": ExitStack()},
    returns={
        "dependent_func": test_writer.DependentFunctionSpy(fixtures.dependent_func)
    },
)
```

## Cache
`cache: bool = False`

While, likely only useful for automatically generated tests, another parameter you can supply to your tests is the `cache` parameter, which specifies if sundew should cache this test's function run. This is primarily useful for speeding up your test suite when you want to test a function and then test another function which calls the first with the same arguments as your test. In this case you avoid the runtime penalty of running the same test twice, or even moreso if the first function is called many times in a loop (for some reason). 

`cache` is a boolean, which defaults to `False` and it can be used like:

```python
test(negative)(
    cache=True,
    kwargs={"a": -8},
    returns=8,
)
```

After this test is ran successfully, _any_ call to `negative(-8)` will immediately return `8` without actually running the logic. In this case our function is trivial, but you might see where this could be valuable for testing more compute intensive functions.