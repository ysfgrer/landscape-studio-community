#!/bin/sh
cd "$(dirname "$0")" || exit 1
if [ ! -x .venv/bin/python ]; then
  python3 setup.py || exit 1
fi
exec .venv/bin/python launcher.py
