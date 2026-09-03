#!/bin/bash
set -e

# Run tests
PYTHONPATH=. ~/.pyenv/versions/3.12.13/bin/pytest tests/

echo "All checks passed successfully."
