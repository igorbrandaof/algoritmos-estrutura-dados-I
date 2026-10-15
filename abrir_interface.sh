#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
exec python3 projeto_final/interface_grafica.py "$@"
