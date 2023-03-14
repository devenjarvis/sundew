<h1 align="center"> sundew :sunny: </h1>
<p align="center"> Function-Based Testing for Python. </p>

## About
Sundew is a testing framework for Python, implementing a new approach to testing that I call "function-based testing". This approach takes the overlap of functional programming concepts, and the best practices for writing tests that we already know, and enforces them to enable some really powerful features that make testing easier and more effective. 

Sundew is still very new, and we've just scratched the surface of function-based testing, but some features implemented already include:
- Smart test ordering, improving our odds to fail fast
- Detection of functions without any tests
- Automatic writing of regression tests, without any cost to your test suite run time 

Beyond these unique features, Sundew also less tangible but just-as-impactful ergonomic benefits like:
- Enforcing good test practices like the Single Responsibility Principle, and test isolation
- Eliminating many case where typical tests can "silently pass" when they shouldn't
- An opinionated syntax that makes it dead simple to understand what is being tested

If you'd like to learn more about function-based testing and Sundew, checkout our launch blog post [here]().

## Installation

Sundew is both a module for writing tests, and a CLI for running them. Once you're ready to get started you can easily install sundew by adding it to your pyproject.toml and/or by running:

```pip
pip install sundew
```
or
```poetry
poetry add sundew --group dev
```

Now you're ready to start using sundew :tada:

> **Warning:**
> Sundew is still pre-1.0, and likely will be for some time. I believe the foundation is fairly set, but make no guarantees yet on breaking changes. If you'd like to pin to a specific version, you can check the GitHub Releases tab or PyPi to find the latest. 