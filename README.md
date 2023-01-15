# sundew ☀️
A new kind of testing framework for Python.

> **Warning**
> This projct is barely even a proof-of-concept still and is not close to being ready for production use. This warning will be updated/removed when that has changed!
  
## To-do

Major things that still need to be done before making public (in rough order):  

- [x] Handle test output failures  
- [x] Handle test errors
- [ ] Handle test side-effect failures (in progress - working basically)
- [x] Basic enforcing of test isolation (Isolate inputs)
- [x] Simplify writing multiple tests for a function
- [ ] Look into a better side_effect signature
- [ ] Fixtures (in progress - implemented for inputs)
- [ ] Write tests for sundew 🤭 (Almost there...)
- [ ] Figure out test naming
- [ ] Basic test selection support
- [x] Asyncio support/examples (basic implementation)
- [ ] Documentation
- [ ] Implement smart test runner
- [ ] Implement automatic sub-function test cases
- [ ] Implement untested sub-function detection
- [ ] Parallel test runner support
- [ ] Add code of conduct
- [ ] Add contribution guidelines
- [x] Setup Github Actions to run CI on PR
- [x] Setup Github Actions to release new versions to PyPi
- [ ] Release version 0.1.0 to PyPi

Future items to look into:

- [ ] Hypothesis integration?
- [ ] Test-case generation for runtime exceptions?