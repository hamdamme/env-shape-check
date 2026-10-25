
# env-shape-check

Check that a local `.env` file has the same variable names as `.env.example`.

The checker reports variable names only. It does not print, compare, modify, or upload values.

## Why use it?

An application can fail when a required environment variable is missing, or when an old variable remains after a configuration change. This small command checks the shape of the files before you run the application.

## Requirements

- Python 3.10 or newer
- No third-party runtime dependencies

## Install from a checkout

From this directory:

```sh
python -m pip install .
```

## Use

From the directory containing `.env.example` and `.env`:

```sh
env-shape-check
```

Choose different paths when needed:

```sh
env-shape-check --example config/env.example --env config/.env
```

Example output:

```text
Missing from .env: API_TOKEN
Extra in .env: OLD_FLAG
```

Exit codes:

- `0`: the files contain the same variable names
- `1`: one or more names are missing or extra
- `2`: a file cannot be read or has a malformed assignment

You can use the exit code in a shell script or CI job. The command never prints values, and it does not change either file.

## Supported file shape

The parser accepts one `NAME=value` assignment per line, blank lines, comments beginning with `#`, and an optional `export ` prefix. Names must use letters, digits, and underscores, and cannot begin with a digit. Values are ignored after the first `=`; quoting, interpolation, multiline values, and shell evaluation are not interpreted. `.env` conventions differ between tools, so check your framework's format if it uses additional syntax.

Example:

```dotenv
# Local service settings
API_TOKEN=
export DATABASE_URL=
FEATURE_FLAG=false
```

## Safety and scope

- Keep `.env` out of version control; commit a value-free `.env.example` instead.
- This tool checks names only. It does not verify that values exist, are valid, or are safe.
- Avoid sharing terminal output if your variable names themselves reveal sensitive information.
- This is a small convenience checker, not a secret scanner or security review.

## License

MIT. See [LICENSE](LICENSE).

## References

- [Python Packaging User Guide: Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [Python `argparse` documentation](https://docs.python.org/3/library/argparse.html)
- [Python `pathlib` documentation](https://docs.python.org/3/library/pathlib.html)
