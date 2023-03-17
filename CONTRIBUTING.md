# Contributing to Sundew

We're glad you're here, and really appreciate your consideration to contribute to Sundew! :tada: 

Right now Sundew is maintained by one person (:wave:) and is in _very_ stages where vision and opinions have not been stabilized. For these reasons I ask for an abundance of patience with any contributions made. I'll make best effort to reply to issues and PRs as quickly as I am able within the contraints of my other obligations. 

## Quick Links to Important Resources
- [Docs](https://sundew-testing.gitbook.io/docs/)
- [Issues](https://github.com/devenjarvis/sundew/issues)
- This project and everyone participating in it is governed by the [Sundew Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Do I Submit A Change?
All change contributions, whether for an enhancement or to fix a bug, are don through the standard GitHub Pull Request process. When you're changes are ready (with tests!) to be contributed back please:

1. Open a new PR in the Sundew repo. Provide a clear title, description, and link to any related issues to the PR.
2. Submit your PR in draft mode while the automated CI runs. (Don't worry, we prioritize keeping this step quick)
3. If the CI fails, troubleshoot the issue and push the necessary changes.
4. Once the CI passes, publish your PR for review!
5. A project maintainer will review your PR as soon as they can, provide a review approving or requesting changes, and then will merge your PR once approved :tada:


## How Do I Report A Bug?

Bugs are tracked as GitHub issues, to submit one please create an issue on this repository and provide the following information:

- Use a clear and descriptive title for the issue to identify the problem.
- Describe the exact steps which reproduce the problem in as many details as possible.
- Explain which behavior you expected to see instead and why.


## How Do I Submit An Enhancement Suggestion?

Enhancement suggestions are tracked as GitHub issues, to submit one please create an issue on this repository and provide the following information:

- Use a clear and descriptive title for the issue to identify the suggestion.
- Provide a step-by-step description of the suggested enhancement in as many details as possible.
- Describe the current behavior and explain which behavior you expected to see instead and why.

## Testing
Sundew is a testing framework, and we want our users to be able to rely on it confidently. For that reason high quality tests and significant test coverage is expected for any changes to the codebase. That said, we dog-food Sundew and sometimes testing the core funtionality of the testing framework with itself is hard :grimace:. When necessary, adding tests to the `examples` as proxy tests for the newly introduced functionality or corrected bug is an acceptable way to build confidence that the change will not break in the future.

## Style Guide / Coding conventions 
Sundew zealously and automatically relies on `black`, `mypy`, and `ruff` modules to enforce coding convetions and style. By default we enable _all_ `ruff` linting rules, and selectively disable rules that we find to be universally restrictive. Occasionally ignoring a linting or typing rule within the code can be necessary, and is totally acceptable when needed. Beyond the strong opinions these tools enforce, Sundew has no specific style guide or coding conventions that we expect contributors to adhere to.

## Thank You!
Just wanted to end this doc with one more "Thank you!". I think Sundew has the potential to be impactful across a wide subset of Python developers, but I expect I won't get there without partnership and contribution from the community. So thank you for your bug report, enhancement suggestion, or (especially!) your PR to make one of those things a reality! I'm grateful for your help in making Sundew better :sunny: