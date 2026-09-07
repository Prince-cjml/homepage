#!/usr/bin/env bash
set -euo pipefail
repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
export DOTNET_CLI_HOME="$repo_root/.dotnet-home"
export NUGET_PACKAGES="$repo_root/.nuget/packages"
export DOTNET_CLI_TELEMETRY_OPTOUT=1
cd "$repo_root"
exec dotnet "$@"
