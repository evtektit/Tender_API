# Bootstrap setup
$ErrorActionPreference = "Stop"
if (Test-Path .venv) { Remove-Item -Recurse -Force .venv }
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip setuptools wheel
pip install -r requirements.txt
python -m playwright install chromium
