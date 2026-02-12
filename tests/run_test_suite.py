import subprocess
import sys
from pathlib import Path

"""
Runs the full test suite and prints output summary.
"""

def indent(text: str, spaces: int = 4) -> str:
    pad = " " * spaces
    return "\n".join(pad + line for line in text.rstrip("\n").splitlines()) if text else ""

def main() -> int:
    here = Path.cwd()
    runner = Path(__file__).resolve()

    tests = sorted(
        p for p in here.iterdir()
        if p.is_file()
        and p.suffix == ".py"
        and p.resolve() != runner
    )

    if not tests:
        print("No .py tests found.")
        return 0

    passed = 0
    failed = 0

    for test in tests:
        print(f"\n=== {test.name} ===")

        proc = subprocess.run(
            [sys.executable, str(test)],
            text=True,
            capture_output=True,
        )

        if proc.returncode == 0:
            passed += 1
            print("✅ PASSED")
            if proc.stdout.strip():
                print("stdout:")
                print(indent(proc.stdout))
        else:
            failed += 1
            print(f"🟥 FAILED (exit code {proc.returncode})")

            if proc.stdout.strip():
                print("stdout:")
                print(indent(proc.stdout))

            if proc.stderr.strip():
                print("stderr:")
                print(indent(proc.stderr))

    print("\n=== Summary ===")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())
