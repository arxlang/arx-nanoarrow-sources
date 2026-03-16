"""
Locate the bundled nanoarrow source artifacts shipped by this package.
"""

from arx_nanoarrow_sources._bundle import (
    bundle_root,
    bundled_nanoarrow_tag,
    bundled_nanoarrow_version,
    get_header_files,
    get_include_dir,
    get_license_files,
    get_source_dir,
    get_source_files,
    package_root,
)
from arx_nanoarrow_sources._version import __version__

__all__ = [
    "__version__",
    "bundle_root",
    "bundled_nanoarrow_tag",
    "bundled_nanoarrow_version",
    "get_header_files",
    "get_include_dir",
    "get_license_files",
    "get_source_dir",
    "get_source_files",
    "package_root",
]
