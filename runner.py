"""Runs a competitor's Python submission against a problem's test cases.

Each test case is executed as its own subprocess (isolated from the Flask
process and from other test cases) with a hard wall-clock timeout, so a
submission with an infinite loop or a crash can't hang or take down the
server. Grading is a "contains" check: the expected snippet must appear,
line-for-line (trailing whitespace ignored), somewhere in stdout. That
mirrors how you'd sanity-check a competition submission's output by eye,
without being brittle about incidental prompt text.
"""

import subprocess
import sys
import tempfile
import os

TIMEOUT_SECONDS = 8


def _normalize(text):
    lines = [ln.rstrip() for ln in text.replace("\r\n", "\n").splitlines()]
    while lines and lines[0] == "":
        lines.pop(0)
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def run_one(code, stdin_text, timeout=TIMEOUT_SECONDS):
    """Run `code` with `stdin_text` fed to stdin. Returns (stdout, stderr, timed_out)."""
    fd, path = tempfile.mkstemp(suffix=".py")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(code)
        try:
            proc = subprocess.run(
                [sys.executable, path],
                input=stdin_text,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            return proc.stdout, proc.stderr, False
        except subprocess.TimeoutExpired:
            return "", f"Timed out after {timeout}s (possible infinite loop).", True
    finally:
        try:
            os.remove(path)
        except OSError:
            pass


def grade_submission(code, test_cases):
    """Run every test case, return a results dict summarizing pass/fail."""
    results = []
    passed = 0
    for i, tc in enumerate(test_cases):
        stdout, stderr, timed_out = run_one(code, tc["stdin"])
        ok = (not timed_out) and (not stderr.strip()) and (
            _normalize(tc["expect"]) in _normalize(stdout)
        )
        if ok:
            passed += 1
        results.append({
            "index": i,
            "stdin": tc["stdin"],
            "expect": tc["expect"],
            "stdout": stdout,
            "stderr": stderr,
            "timed_out": timed_out,
            "passed": ok,
        })
    return {
        "passed": passed,
        "total": len(test_cases),
        "all_passed": passed == len(test_cases),
        "results": results,
    }
