"""The Absurd Clause Contest — entry program.

Writes one original English sentence (116 characters) to /output/entry.txt:
a deadpan terms-of-service clause that quietly turns absurd.

Usage:
    python3 main.py

The output path defaults to /output/entry.txt and can be overridden with the
ENTRY_OUTPUT environment variable (used by the test suite). Standard library
only; deterministic; no network access.
"""

import os
import sys

DEFAULT_OUTPUT = "/output/entry.txt"

# One original English sentence, 116 characters: deadpan legal boilerplate
# ("hereby owes", "payable within thirty (30) days", "no exceptions") that
# quietly turns absurd at "one (1) goat" — and ambushes the reader, since
# reading the clause is itself the triggering act.
CLAUSE = (
    "Any user who reads this clause hereby owes the company one (1) goat, "
    "payable within thirty (30) days, no exceptions."
)


def resolve_output_path() -> str:
    """Return the output path: ENTRY_OUTPUT when set, else the default."""
    return os.environ.get("ENTRY_OUTPUT") or DEFAULT_OUTPUT


def validate(clause: str) -> None:
    """Enforce the gate: 1-200 characters, not only whitespace, one line.

    Also enforces the brief's shape: exactly one sentence (a single
    sentence-terminating period at the end), ASCII only, and no control
    characters, so a malformed clause can never reach the gate silently.
    """
    if not (1 <= len(clause) <= 200):
        raise ValueError(f"clause is {len(clause)} characters, must be 1-200")
    if not clause.strip():
        raise ValueError("clause must not be only whitespace")
    if "\n" in clause or "\r" in clause:
        raise ValueError("clause must be a single line")
    if any(ord(ch) < 0x20 for ch in clause):
        raise ValueError("clause must not contain control characters")
    try:
        clause.encode("ascii")
    except UnicodeEncodeError as exc:
        raise ValueError("clause must be plain ASCII") from exc
    if clause.count(".") != 1 or not clause.endswith("."):
        raise ValueError("clause must be exactly one sentence")


def main() -> int:
    try:
        validate(CLAUSE)
        path = resolve_output_path()
        parent = os.path.dirname(path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(CLAUSE)
        # Read-back verification: the file on disk must be byte-identical
        # to the clause, so a partial or mangled write is never silent.
        with open(path, "rb") as f:
            if f.read().decode("utf-8") != CLAUSE:
                raise OSError(f"read-back mismatch for {path}")
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {len(CLAUSE)} characters to {resolve_output_path()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
