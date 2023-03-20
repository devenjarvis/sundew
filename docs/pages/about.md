# About Sundew

As you peek around the docs, you might notice sundew looks a bit different from other testing frameworks. This isn't just an ergonomic preference, but rather the requirements of the unique way sundew approaches testing. The payoff for doing things differently is alot of powerful functionality that should both improve the effectiveness of your test suite, and your experience writing tests themselves. This page documents some of the underlying approach and invisible features of sundew, to better understand why it's different and what that unlocks.

## Function-Based Testing
The main philosphy behind how sundew works is, atleast from what I can tell, new. So until a better name arises I've choosen to call this approach "function-based testing". The name isn't to give you another dogmatic acronym to love or hate, just to name a concept that I believe can transcend Python and be useful in other languages as well.

The root philosphy behind sundew can be simply summarized as this:

> Every test has a strict relationship with a **single function** from your code.

To any software testing veteran this probably sounds a bit _obvious_. "Of course a good test should only test one thing at a time!", you might say - and you'd be right! Sundew takes this a step forward by enforcing it. If you read the very beginning of [Writing Tests](writing-tests.md) you'll see that every test in sundew is defined by passing a callable to the `sundew.test()` function. However, this isn't to be dogmatic to force good testing practices on you (although it is a good practice!). By doing this we unlock one key insight that sets us up for all the other cool things on this page:

> When each test has a strict relationship with a single function, our tests know **what** it is they are testing.

This is a simple but _powerful_ statement, because now our tests can do really smart things, automatically, without a terrible amount of complexity! Take a look at the next few sections to see what I'm talking about.

## Automatic Test Sorting
As we just explored, the main philosphy of function-based testing is that sundew knows exactly what function each test is running. Extending this idea into practice, we can also inspect those functions and see the  other functions they call as well (referred to as sub-functions throughout the rest of this doc). If those sub-functions have tests (and we hope they do, but we'll come back to that) then Sundew can build a dependency graph before it runs a single test. We can then take that dependency graph and apply [Kahn's Algorithm](https://en.wikipedia.org/wiki/Topological_sorting#Kahn's_algorithm) to topographically sort it. In our case, this sorts our tests from the ones for functions that have the least sub-functions (i.e. - zero) to the ones for functions that have the most number of dependent functions (ex: `function_a`, which calls `function_b` and `function_c`, both of which call `function_d`).

Now why is this interesting? Well if you've ever had a long running test suite not fail until it's 10 minutes in, then you might appreciate the value of a test suite that can **fail fast**. If we've got a failing test, we want to know as soon as possible so we don't waste precious developer flow waiting on all the successful tests before we find out. Now sundew is not deterministic in a way to _guarantee_ that the very last test you run doesn't have a bug in it, but we increase our odds of failing fast when we sort our tests like this in two ways:

1. Assume `function_a` calls `function_b`. `function_a` is guaranteed to take atleast as long as `function_b`. By topographically sorting our dependency graph we have approximately ordered our tests from fastest to slowest. This ordering is not guaranteed (no one says a function without any dependencies can't be extremely slow) but it's approximately the case for any reasonably complex codebase. This also implies we'll run more tests quicker, increasing our odds of finding the failing test earlier on.

2. Again, assume `function_a` calls `function_b`. If `function_a` has a bug in it `function_b` most likely does too. So once again, while this approach does not provide guarantees, we've increased our likelihood to find our bugs faster by testing the functions that others depend on first. For a sufficiently quality test suite, the inverse can also point to where your bugs are. If `function_a` is _not_ failing tests, but `function_b` is, it tells you a bit about where to look for your issue.

This happens automatically everytime you run sundew, and is just the start of the cool things function-based testing can unlock.

## Detection of Missing Tests

As we discussed in the last section, we now know what functions have tests and any sub-functions that those functions call. While we can use tests for those sub-functions to build our dependency graph, we can also detect and report when those sub-functions don't have tests! This is a great, high-level step toward assessing your test suite's code coverage. While it's often not worth it to ensure you've "tested" every line of code, I'd assert it's almost always beneficial to make sure you're at least testing every function of your code.

"But wait, that sounds like a lot of work. I already wrote good tests for a higher-level function; now I have to write tests for all the sub-functions it depends on?", I hear you say. Fear not, we've saved the best for last, because with Sundew you actually don't!

## Automatic Regression Tests (Cost Free!)

So at this point, Sundew knows:

1. Which functions have tests
2. What sub-functions are called by those functions
3. Which of those sub-functions don't have tests

If we combine all this knowledge we can do something _really_ cool. When Sundew runs the tests you have written, as long as they pass, it can patch the sub-functions without tests and **automatically write regression tests for them**. If we know `function_a` passes it's test, and while we ran that test `function_a` called `function_b` with the arguments `(a=123, b="456")` and `function_b` returned `"123456"` then we've got everything we need to write a basic Sundew test for `function_b`. This happens recursively and for all sub-function calls without an existing test.

What's even better is we `know` the test for `function_a` is going to run the same function with the same arguments as the automatic test we just wrote for `function_b`, ***and*** we know Sundew automatically orders our tests by function dependencies, so we can cache `function_b` so we don't waste time running the same function twice in our test suite. This means the run time for your test suite does not grow, even though the coverage of your test suite does :tada:.

Now, these auto written tests don't know what side-effects to test, nor are we running property tests to check other possible inputs that could fail, which is why I refer to them strictly as "regression tests". They take the tedium and cost out of writing tests to ensure that your changes in the future don't break what's working today.

## The Future
I believe sundew has only scratched the surface of the functionality function-based testing can offer, and there is certainly more work to be done to regain the expressiveness lost from traditional test functions. Some potential big wins tht I hope to explore with sundew in the future include:
- Detecting which functions have changes since your last commit, or test run, and only running tests for those functions
- I believe mutation testing is ready to have its time to shine in the Python world but is held back by the huge computational load of testing mutations across your code. I believe Sundew's function-based testing method can allow us to isolate mutation tsting to just single functions at a time, making it possible to slowly adopt and incorporate it into your test suite.
- I think there is more we can do with auto-generated tests, and I'd love to continue exploring making them more robust than just regression tests

In the meantime, I'm eager to see sundew get more real world use and hear back on the other ways sundew can improve your testing experience. If you hit a bug, or have other ideas about the potential of function-based testing please drop an [issue](https://github.com/devenjarvis/sundew/issues)