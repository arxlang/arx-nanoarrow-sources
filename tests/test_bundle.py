"""
title: Tests for the packaged nanoarrow bundle helpers.
"""

from arx_nanoarrow_sources import (
    bundle_root,
    bundled_nanoarrow_tag,
    bundled_nanoarrow_version,
    get_header_files,
    get_include_dir,
    get_license_files,
    get_source_dir,
    get_source_files,
)
from arx_nanoarrow_sources._bundle import read_bundle_metadata


def test_bundle_paths_exist() -> None:
    """
    title: Assert that the generated bundle paths exist.
    """
    assert bundle_root().exists()
    assert get_include_dir().exists()
    assert get_source_dir().exists()
    assert get_header_files()
    assert get_source_files()
    assert get_license_files()


def test_bundle_metadata_matches_helper_api() -> None:
    """
    title: Assert that bundle metadata matches the helper API.
    """
    metadata = read_bundle_metadata()

    assert metadata["bundled_version"] == bundled_nanoarrow_version()
    assert metadata["bundled_tag"] == bundled_nanoarrow_tag()
    assert "include/nanoarrow/nanoarrow.h" in metadata["header_files"]
    assert "src/nanoarrow.c" in metadata["source_files"]
