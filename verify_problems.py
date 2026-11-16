import subprocess
import sys
import tempfile
import os
from content.problems import PROBLEMS


def normalize(text):
    lines = [ln.rstrip() for ln in text.splitlines()]
    while lines and lines[0] == "":
        lines.pop(0)
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def run(code, stdin_text):
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(code)
        path = f.name
    try:
        proc = subprocess.run(
            [sys.executable, path],
            input=stdin_text,
            capture_output=True,
            text=True,
            timeout=10,
        )
        return proc.stdout, proc.stderr
    finally:
        os.unlink(path)


failures = 0
for p in PROBLEMS:
    for i, tc in enumerate(p["test_cases"]):
        out, err = run(p["reference_solution"], tc["stdin"])
        if err.strip():
            print(f"[STDERR] {p['id']} test {i}: {err}")
            failures += 1
            continue
        if normalize(tc["expect"]) not in normalize(out):
            print(f"[FAIL] {p['id']} test {i}")
            print(f"  expect contains: {tc['expect']!r}")
            print(f"  actual stdout:   {out!r}")
            failures += 1

print(f"\n{len(PROBLEMS)} problems checked, {failures} failures")
