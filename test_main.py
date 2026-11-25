"""Tests for main.py — The Absurd Clause Contest entry.

The program writes one original English sentence (<= 200 chars) to
/output/entry.txt: a deadpan terms-of-service clause that quietly turns absurd.
"""

import os
import subprocess
import sys
import tempfile
import unittest

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_PY = os.path.join(REPO_DIR, "main.py")

EXPECTED_LINE = (
    "Any user who reads this clause hereby owes the company one (1) goat, "
    "payable within thirty (30) days, no exceptions."
)


def run_main(output_path, extra_env=None):
    env = dict(os.environ)
    env["ENTRY_OUTPUT"] = output_path
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        [sys.executable, MAIN_PY],
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )


class TestEntryOutput(unittest.TestCase):
    def test_writes_exact_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "entry.txt")
            result = run_main(out)
            self.assertEqual(result.returncode, 0, result.stderr)
            with open(out, "rb") as f:
                raw = f.read()
            self.assertEqual(raw.decode("utf-8"), EXPECTED_LINE)

    def test_length_within_gate(self):
        self.assertGreaterEqual(len(EXPECTED_LINE), 1)
        self.assertLessEqual(len(EXPECTED_LINE), 200)

    def test_single_line_no_newline(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "entry.txt")
            run_main(out)
            with open(out, "rb") as f:
                raw = f.read()
            self.assertNotIn(b"\n", raw)
            self.assertNotIn(b"\r", raw)

    def test_no_leading_trailing_whitespace(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "entry.txt")
            run_main(out)
            text = open(out, encoding="utf-8").read()
            self.assertEqual(text, text.strip())
            self.assertTrue(text.strip(), "entry must not be only whitespace")

    def test_deterministic_across_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            out1 = os.path.join(tmp, "a.txt")
            out2 = os.path.join(tmp, "b.txt")
            run_main(out1)
            run_main(out2)
            self.assertEqual(open(out1, "rb").read(), open(out2, "rb").read())

    def test_creates_missing_output_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "deep", "nested", "entry.txt")
            result = run_main(out)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(os.path.exists(out))

    def test_one_sentence(self):
        self.assertEqual(EXPECTED_LINE.count("."), 1)
        self.assertTrue(EXPECTED_LINE.endswith("."))

    def test_ascii_only(self):
        EXPECTED_LINE.encode("ascii")

    def test_default_output_path(self):
        # Default is /output/entry.txt when ENTRY_OUTPUT is unset.
        import main

        self.assertEqual(main.DEFAULT_OUTPUT, "/output/entry.txt")

    def test_unwritable_location_fails_gracefully(self):
        # Writing into a path that is a directory must exit non-zero
        # with a message, not an unhandled traceback.
        with tempfile.TemporaryDirectory() as tmp:
            result = run_main(tmp)  # tmp is a directory, not a file
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn("Traceback", result.stderr, "must not leak a traceback")
            self.assertTrue(result.stderr.strip())


class TestSourceConstraints(unittest.TestCase):
    def test_stdlib_only_imports(self):
        import ast

        tree = ast.parse(open(MAIN_PY, encoding="utf-8").read())
        allowed = {"os", "sys"}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.assertIn(alias.name.split(".")[0], allowed)
            elif isinstance(node, ast.ImportFrom):
                self.assertIn((node.module or "").split(".")[0], allowed)

    def test_no_network_calls(self):
        source = open(MAIN_PY, encoding="utf-8").read()
        for banned in ("socket", "urllib", "requests", "http.client", "urlopen"):
            self.assertNotIn(banned, source)


if __name__ == "__main__":
    unittest.main()
