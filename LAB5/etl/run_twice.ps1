$ErrorActionPreference = "Stop"

Set-Location (Split-Path $PSScriptRoot -Parent)
py -3.13 etl/load_and_check.py
py -3.13 etl/load_and_check.py
