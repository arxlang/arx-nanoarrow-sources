"""
title: Helper functions for locating the packaged nanoarrow bundle.
"""

from __future__ import annotations

import json

from pathlib import Path
from typing import TypedDict, cast

from arx_nanoarrow_sources._version import (
    BUNDLED_NANOARROW_TAG,
    BUNDLED_NANOARROW_VERSION,
)


class BundleMetadata(TypedDict):
    bundled_tag: str
    bundled_version: str
    header_files: list[str]
    source_archive_url: str
    source_files: list[str]


def package_root() -> Path:
    """
    title: Return the root directory of the installed package.
    returns:
      type: Path
    """
    return Path(__file__).resolve().parent


def bundle_root() -> Path:
    """
    title: Return the root directory of the vendored nanoarrow bundle.
    returns:
      type: Path
    """
    root = package_root() / "vendor"
    if not root.exists():
        raise FileNotFoundError(
            "Bundled nanoarrow sources are missing. "
            "Run 'python scripts/build_bundle.py' before building/testing."
        )
    return root


def get_include_dir() -> Path:
    """
    title: Return the include directory containing nanoarrow headers.
    returns:
      type: Path
    """
    return bundle_root() / "include"


def get_source_dir() -> Path:
    """
    title: >-
      Return the directory containing the generated nanoarrow C source files.
    returns:
      type: Path
    """
    return bundle_root() / "src"


def get_header_files() -> tuple[Path, ...]:
    """
    title: Return the packaged nanoarrow header files.
    returns:
      type: tuple[Path, Ellipsis]
    """
    include_dir = get_include_dir()
    headers = sorted(include_dir.rglob("*.h")) + sorted(
        include_dir.rglob("*.hpp")
    )
    return tuple(headers)


def get_source_files() -> tuple[Path, ...]:
    """
    title: Return the packaged nanoarrow C source files.
    returns:
      type: tuple[Path, Ellipsis]
    """
    return tuple(sorted(get_source_dir().rglob("*.c")))


def get_license_files() -> tuple[Path, ...]:
    """
    title: Return the packaged license files shipped with the bundle.
    returns:
      type: tuple[Path, Ellipsis]
    """
    return tuple(sorted(bundle_root().glob("LICENSE*")))


def bundled_nanoarrow_version() -> str:
    """
    title: Return the upstream nanoarrow version bundled by this package.
    returns:
      type: str
    """
    return BUNDLED_NANOARROW_VERSION


def bundled_nanoarrow_tag() -> str:
    """
    title: Return the upstream nanoarrow tag bundled by this package.
    returns:
      type: str
    """
    return BUNDLED_NANOARROW_TAG


def read_bundle_metadata() -> BundleMetadata:
    """
    title: Return the stored metadata describing the generated bundle contents.
    returns:
      type: BundleMetadata
    """
    metadata_path = bundle_root() / "bundle-metadata.json"
    return cast(
        BundleMetadata,
        json.loads(metadata_path.read_text(encoding="utf8")),
    )
