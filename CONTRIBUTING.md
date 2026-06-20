# Contributing

Thanks for considering a contribution. This document covers how to report bugs,
submit pull requests, and set up a development environment.

## Reporting Bugs

- Check the existing [issues](https://github.com/B3122/PharmaLens/issues)
  to avoid duplicates.
- Open a new issue and include:
  - A short, clear title.
  - Steps to reproduce the problem.
  - Expected vs actual behavior.
  - Your OS, Python version, and any relevant terminal output.
- Use the **Bug Report** issue template if one exists.

## Pull Requests

### Branch strategy

This repo uses a single default branch model:

| Branch  | Purpose                         |
|---------|---------------------------------|
| `main`  | Active development, all commits |

- Target the `main` branch for all PRs.
- Keep PRs small and focused on one change.

### Commit style

- Write commits in English, present-tense imperative: `Add`, `Fix`, `Remove`.
- Keep the first line under 72 characters.
- Add a blank line before any body text.

### Before you open a PR

- [ ] Write or update tests for the changed behavior.
- [ ] Run `python -m pytest` and make sure all tests pass.
- [ ] Run any project linters or formatters already in use.
- [ ] Update the README if the change is user-visible.

## Development Setup

```bash
# Clone the repo
git clone https://github.com/B3122/PharmaLens.git
cd market-research

# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install jsonschema openpyxl
```

The project uses standard-library Python scripts under
`.pi/skills/product-market-research/scripts/`. JSON schemas live under
`.pi/skills/product-market-research/schemas/`.

## Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) for Python.
- Match the style of the file you are editing.
- Prefer readability over cleverness.

## Code of Conduct

All participants are expected to follow the
[Code of Conduct](CODE_OF_CONDUCT.md). Report concerns to the project
maintainers.
