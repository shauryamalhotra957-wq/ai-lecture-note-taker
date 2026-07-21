# Contributing

Thanks for improving AI Lecture Note Taker.

## Development setup

1. Fork or clone the repository.
2. Create a focused branch from `main`.
3. Create and activate a Python 3.11 virtual environment.
4. Install the project with `python -m pip install -e .`.

## Quality checks

Run `python -m pytest` before opening a pull request. Add tests for transcription, summarization, parsing, and failure handling. Use synthetic or consented sample media only.

## Pull requests

Describe the problem, implementation, and validation. Never commit credentials, private recordings, model caches, or generated notes.
