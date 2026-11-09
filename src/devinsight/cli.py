from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .pipeline import clean_rows, deduplicate, read_csv, run_pipeline, validate_rows


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(prog="devinsight", description="Auditable public-issue evidence pipeline")
    subcommands = command.add_subparsers(dest="command", required=True)

    validate = subcommands.add_parser("validate", help="Validate a raw evidence CSV without writing outputs")
    validate.add_argument("input", type=Path)

    build = subcommands.add_parser("build", help="Validate, clean, deduplicate, code, and generate an evidence pack")
    build.add_argument("input", type=Path)
    build.add_argument("--output-dir", type=Path, default=Path("outputs"))
    build.add_argument("--llm-suggestions", type=Path, default=None, help="Optional offline JSON suggestions to review; never auto-accepted")
    return command


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "validate":
            rows = read_csv(args.input)
            issues = validate_rows(rows)
            if issues:
                for issue in issues:
                    print(issue.format(), file=sys.stderr)
                return 1
            unique, duplicates = deduplicate(clean_rows(rows))
            print(json.dumps({"valid_rows": len(rows), "unique_rows": len(unique), "duplicates": len(duplicates)}, indent=2))
            return 0
        summary = run_pipeline(args.input, args.output_dir, args.llm_suggestions)
        print(json.dumps(summary, indent=2))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
