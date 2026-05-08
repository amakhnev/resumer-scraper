import sys

from dev import run


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/dev_run.py <source> or python scripts/dev.py run <source>")

    source = sys.argv[1]
    run(source)


if __name__ == "__main__":
    main()
