# Development Guide

## Setting Up the Development Environment

[Instructions here]

## Running Tests

[Instructions here]

## Known Issues

### Hypothesis Tests on Lightning.ai

Currently, tests using the Hypothesis library may hang indefinitely when run on the Lightning.ai platform. This issue does not affect local development. 

**Workaround:** 

- All Hypothesis tests are skipped when running on Lightning.ai using a custom `@skip_on_lightning` decorator.
- For local development and CI, all tests (including Hypothesis tests) run normally.

**TODO:** 

- Investigate root cause of Hypothesis hanging on Lightning.ai
- Explore alternative property-based testing libraries that are compatible with Lightning.ai if necessary

## Contribution Guidelines

[Any guidelines for contributing to the project]