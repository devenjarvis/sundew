# sundew ☀️
A new kind of testing framework for Python.

> **Warning**
> This project is a proof-of-concept still and is not close to being ready for production use. This warning will be updated/removed when that has changed!

## Installation
Sundew is both a module for writing tests, and a CLI for running them. You can easily install sundew by adding it to your pyproject.toml or by running:

```
pip install sundew
```

If you'd like to pin to a specific version, you can check the GitHub Releases tab or PyPi.
  
## To-do

Major things that still need to be done before making public (in rough order):  

- [x] Handle test output failures  
- [x] Handle test errors
- [x] Handle basic test side-effects
- [x] Basic enforcing of test isolation (Isolate inputs)
- [x] Simplify writing multiple tests for a function
- [x] Look into a better side_effect signature
- [x] Fixtures (Basics implemented)
- [x] Write initial tests for sundew
- [x] ~Figure out test naming~ (Decided this isn't necessary for now)
- [x] Basic test selection support (Can select tests by function name with --function option)
- [x] Asyncio support/examples (basic implementation)
- [x] Implement smart test runner
- [x] Implement untested sub-function detection
- [x] Implement automatic sub-function test writing
- [x] Setup Github Actions to run CI on PR
- [x] Add code of conduct
- [x] Add contribution guidelines
- [x] Cache auto regression tests so they have no performance impact
- [x] Documentation
- [x] Expand Python version compatibility (Now supports Python 3.9 -> 3.11)
- [ ] Improve sundew test coverage
- [ ] Handle more advanced test side-effects (<=, >=, in, etc)
- [ ] Setup Github Actions to release new versions to PyPi
- [ ] Add "Here be dragons" disclaimers to docs
- [ ] Upate README and move to do list into GH issues
- [ ] Release version 0.1.0 to PyPi
- [ ] Write first blog post, introducing sundew

## Future
- [ ] Add more complex examples (~0.2.0)
- [ ] Improve error handling/reporting (right now we throw a lot of exceptions) (~0.2.0)
- [ ] Improve test failure messages, `warp` is a good example to strive for. (~0.2.0)
- [ ] Parallel test runner support (~0.2.0)
- [ ] testmon-like functionality (~0.3.0)
- [ ] Mutation testing/coverage reporting (~0.4.0)
- [ ] Hypothesis integration (maybe?)
- [ ] Test-case generation for runtime exceptions (maybe?)