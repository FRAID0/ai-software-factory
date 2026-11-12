import sys
import unittest
from pathlib import Path

# Add root directory to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))


def run_all_tests() -> int:
    print("\n" + "=" * 60)
    print("   AI SOFTWARE FACTORY - TEST SUITE")
    print("=" * 60 + "\n")

    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=str(root_dir / "tests"), pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 60)
    print(
        f"SUMMARY: Ran {result.testsRun} tests | "
        f"Failures: {len(result.failures)} | "
        f"Errors: {len(result.errors)}"
    )
    print("=" * 60 + "\n")

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
