"""
Build the bundled nanoarrow sources shipped by arx-nanoarrow-sources.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

from arx_nanoarrow_sources._version import (  # noqa: E402
    BUNDLED_NANOARROW_TAG,
    BUNDLED_NANOARROW_VERSION,
)

PACKAGE_DIR = SRC_DIR / "arx_nanoarrow_sources"
VENDOR_DIR = PACKAGE_DIR / "vendor"
UPSTREAM_ARCHIVE_URL = (
    "https://github.com/apache/arrow-nanoarrow/archive/refs/tags/"
    f"{BUNDLED_NANOARROW_TAG}.tar.gz"
)


def build_bundle() -> None:
    """
    Build and vendor the generated nanoarrow C bundle.
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        archive_path = tmp_path / f"{BUNDLED_NANOARROW_TAG}.tar.gz"
        extracted_root = tmp_path / "upstream"

        _download_archive(archive_path)
        _extract_archive(archive_path, extracted_root)

        upstream_root = _find_upstream_root(extracted_root)
        bundled_output = tmp_path / "bundled"
        _run_upstream_bundler(upstream_root, bundled_output)
        _sync_vendor_tree(upstream_root, bundled_output)


def _download_archive(target_path: Path) -> None:
    with urllib.request.urlopen(UPSTREAM_ARCHIVE_URL) as response:
        target_path.write_bytes(response.read())


def _extract_archive(archive_path: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive_path, "r:gz") as archive:
        for member in archive.getmembers():
            member_path = output_dir / member.name
            if not member_path.resolve().is_relative_to(output_dir.resolve()):
                raise ValueError("Archive contains an unsafe path")
            archive.extract(member, output_dir, filter="data")


def _find_upstream_root(output_dir: Path) -> Path:
    for child in output_dir.iterdir():
        bundle_script = child / "ci" / "scripts" / "bundle.py"
        if child.is_dir() and bundle_script.exists():
            return child

    raise FileNotFoundError("Unable to locate extracted nanoarrow source tree")


def _run_upstream_bundler(upstream_root: Path, output_dir: Path) -> None:
    subprocess.run(
        [
            sys.executable,
            str(upstream_root / "ci" / "scripts" / "bundle.py"),
            "--output-dir",
            str(output_dir),
        ],
        check=True,
        cwd=upstream_root,
    )


def _sync_vendor_tree(upstream_root: Path, bundled_output: Path) -> None:
    if VENDOR_DIR.exists():
        shutil.rmtree(VENDOR_DIR)

    shutil.copytree(bundled_output, VENDOR_DIR)

    license_path = _find_license_file(upstream_root)
    shutil.copy2(license_path, VENDOR_DIR / license_path.name)

    metadata = {
        "bundled_version": BUNDLED_NANOARROW_VERSION,
        "bundled_tag": BUNDLED_NANOARROW_TAG,
        "source_archive_url": UPSTREAM_ARCHIVE_URL,
        "header_files": [
            str(path.relative_to(VENDOR_DIR))
            for path in sorted((VENDOR_DIR / "include").rglob("*.h"))
        ]
        + [
            str(path.relative_to(VENDOR_DIR))
            for path in sorted((VENDOR_DIR / "include").rglob("*.hpp"))
        ],
        "source_files": [
            str(path.relative_to(VENDOR_DIR))
            for path in sorted((VENDOR_DIR / "src").rglob("*.c"))
        ],
    }

    (VENDOR_DIR / "bundle-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf8",
    )


def _find_license_file(upstream_root: Path) -> Path:
    for candidate in ("LICENSE.txt", "LICENSE"):
        path = upstream_root / candidate
        if path.exists():
            return path

    raise FileNotFoundError("Unable to locate upstream nanoarrow license file")


if __name__ == "__main__":
    build_bundle()
