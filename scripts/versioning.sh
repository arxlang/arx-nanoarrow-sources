#!/usr/bin/env bash
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && cd .. && pwd )"

set -e

if [ "$1" == "" ]; then
  echo "Version parameter is required."
  exit 1
fi

PYPROJECT_PATH="${PROJECT_DIR}/pyproject.toml"
VERSION_MODULE_PATH="${PROJECT_DIR}/src/arx_nanoarrow_sources/_version.py"

sed -i \
  "s/version = \"[0-9]*\.[0-9]*\.[0-9]*\"  # bundled nanoarrow version/version = \"$1\"  # bundled nanoarrow version/" \
  "${PYPROJECT_PATH}"

sed -i \
  "s/BUNDLED_NANOARROW_VERSION = \"[0-9]*\.[0-9]*\.[0-9]*\"/BUNDLED_NANOARROW_VERSION = \"$1\"/" \
  "${VERSION_MODULE_PATH}"
