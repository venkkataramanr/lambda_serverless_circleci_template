#!/usr/bin/env bash

export VIRTUAL_ENV="${CIRCLE_WORKING_DIRECTORY}/.venv"
export PATH="${PATH}:${VIRTUAL_ENV}/bin/"
export PYTHONPATH="${PYTHONPATH}:"

# Activates the virtual environment
if [ -f "${VIRTUAL_ENV}/bin/activate" ]; then
    source "${VIRTUAL_ENV}/bin/activate"
fi
