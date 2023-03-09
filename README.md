# sundew ☀️
A new kind of testing framework for Python.

> **Warning**
> This project is a proof-of-concept still and is not close to being ready for production use. This warning will be updated/removed when that has changed!
  
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
- [x] Setup Github Actions to release new versions to PyPi
- [ ] Improve sundew test coverage
- [ ] Handle more advanced test side-effects (<=, >=, in, etc)
- [ ] Documentation
- [ ] Add code of conduct
- [ ] Add contribution guidelines
- [ ] Release version 0.1.0 to PyPi
- [ ] Write first blog post, introducing sundew

## Future
- [ ] Improve error handling/reporting (right now we throw a lot of exceptions) (~0.2.0)
- [ ] Improve test failure messages, `warp` is a good example to strive for. (~0.2.0)
- [ ] Parallel test runner support (~0.2.0)
- [ ] testmon-like functionality (~0.3.0)
- [ ] Mutation testing/coverage reporting (~0.4.0)
- [ ] Hypothesis integration (maybe?)
- [ ] Test-case generation for runtime exceptions (maybe?)