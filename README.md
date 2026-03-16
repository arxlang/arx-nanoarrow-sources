# arx-nanoarrow-sources

`arx-nanoarrow-sources` packages the generated nanoarrow C bundle for the Arx
ecosystem.

It does not ship compiled binaries. Instead, it ships:

- generated `nanoarrow.h` and `nanoarrow.hpp`
- generated `nanoarrow.c`
- upstream bundle metadata and license files
- Python helper functions to locate those files from build systems

The package also depends on the Python `nanoarrow` package so projects can use
the runtime Python bindings and the bundled C sources together.

## Usage

```python
from arx_nanoarrow_sources import (
    bundled_nanoarrow_version,
    get_header_files,
    get_include_dir,
    get_source_files,
)

print(bundled_nanoarrow_version())
print(get_include_dir())
print(get_header_files())
print(get_source_files())
```

## Build behavior

Run `python scripts/build_bundle.py` before `poetry build`. The bundle script
downloads the pinned upstream nanoarrow source release, runs the official
upstream bundler, and stores the generated output under
`src/arx_nanoarrow_sources/vendor/`.

## Development

```bash
python scripts/build_bundle.py
pytest -q
ruff check .
mypy src tests
```
