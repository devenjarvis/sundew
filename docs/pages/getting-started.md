<h1 align="center"> sundew :sunny: </h1>
<p align="center"> Making Python testing easy, enjoyable, and effective </p>

## About
Sundew is a testing framework for Python, implementing a new approach to testing. One that combines functional programming concepts and the general best practices for writing tests that we already know, and enforces them in a way that enables some really powerful features that make testing easier, enjoyable, and more effective.

Sundew is still very new and we've just scratched the surface of what it can unlock, but some features implemented already include:
- Smart test ordering, improving our odds to fail fast
- Detection of functions without any tests
- Automatic writing of regression tests, without any cost to your test suite run time 

Using Sundew also has other, less tangible, benefits like:
- Enforcing good test practices like the Single Responsibility Principle and test isolation
- Eliminating many cases where typical tests can "silently pass" when they shouldn't
- An opinionated syntax that makes it dead simple for others to understand what exactly is being tested

If you'd like to learn more about Sundew and it's unique approach to testing, which I call "function-based testing", checkout out the [About section](about.md).


## Here Be Dragons 🐉
**Warning:** Not only does this project attempt a new approach to testing, it is also in _very_ early stages and still has alot of sharp edges that need smoothing. While sundew introduces a set of new and unique features, it is not yet at a place where it has the stability or feature parity of more mature existing framworks like `pytest`. Early adopters are encouraged to try out sundew and report any issues or critical missing functionality in the form of a GitHub Issue. 

This project is currenty maintained by a single part-time individual (:wave:), so there is **no guarantee** on how quickly raised issues will be addressed, however bug fixes and missing critical functionailty will be significantly prioritizd over expanded functionailty at this stage of the project. PRs are also welcome for those who are willing and interested in [contributing](CONTRIBUTING.md).

If you are excited about trying something brand new and are willing to except the edges, please continue! However if you or your project is not ready to take on this amount of risk, I recommend keeping an eye on this project and waiting a bit before diving in. I'll update this section as the project matures.

## Installation

Sundew is both a module for writing tests, and a CLI for running them. Once you're ready to get started you can easily install sundew by adding it to your pyproject.toml and/or by running:

```pip
pip install -U sundew
```
or
```poetry
poetry add sundew --group dev
```

Now you're ready to start using sundew :tada:

> **Warning:**
> Sundew follows semantic versioning, is still pre-1.0, and likely will be for some time. At this time I can make no guarantees on breaking changes. If you'd like to pin to a specific version, you can check the GitHub Releases tab or PyPi to find the latest. 