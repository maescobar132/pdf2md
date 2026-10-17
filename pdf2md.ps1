# Windows wrapper (uv). En $PROFILE de PowerShell:
#   function pdf2md { uv run --script $HOME\tools\pdf2md\convert.py @args }
uv run --script "$PSScriptRoot\convert.py" @args
