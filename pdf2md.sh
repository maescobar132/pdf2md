#!/usr/bin/env bash
# Ubuntu wrapper (uv). Instalar: ln -s ~/tools/pdf2md/pdf2md.sh ~/bin/pdf2md
# uv lee las dependencias del encabezado de convert.py y las cachea pineadas.
set -euo pipefail
exec uv run --script "$(dirname "$(readlink -f "$0")")/convert.py" "$@"
