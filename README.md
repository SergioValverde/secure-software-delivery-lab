# Secure Software Delivery Lab

A practical lab for building and validating secure software delivery controls.

This repository demonstrates how software changes can be evaluated before they reach the default branch. The current milestone implements an enforced pull-request quality gate using GitHub Actions, Python tests, and a GitHub branch ruleset.

## Current milestone: enforced pull-request quality gate

The repository now requires pull requests into `main` to pass automated Python tests before merge.

The control flow is:

```text
developer change
→ pull request
→ GitHub Actions workflow
→ Python test execution
→ required status check
→ branch ruleset enforcement
→ merge allowed only if checks pass
