import sys
import warnings

def main():
    warnings.warn(
        "The 'devspeed' command is deprecated. Please use 'krickstart' instead.",
        DeprecationWarning,
        stacklevel=2
    )
    print("⚠️  WARNING: 'devspeed' is now 'krickstart'. Please update your scripts.")
    try:
        from krickstart.cli import main as new_main
        new_main()
    except ImportError:
        print("Error: krickstart package not found. Please reinstall.", file=sys.stderr)
        sys.exit(1)