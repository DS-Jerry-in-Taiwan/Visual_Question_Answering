# scripts/extract_phase_docs.py
#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path
from typing import Dict, Iterable, List

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / ".agentdoc" / "text.txt"
OUTPUT_DIR = ROOT / ".agentdoc" / "phase0"
DEFAULT_TARGET_FILE = ROOT / ".agentdoc" / "phase0" / "phase0_step03_targets.txt"

SECTION_PATTERN = re.compile(
    r"\*\*檔案名稱\*\*:\s*`(?P<filename>[^`]+)`\s*\n+```(?:[^\n]*)\n(?P<body>.*?)```",
    re.DOTALL,
)


def extract_sections(source: Path) -> Dict[str, str]:
    text = source.read_text(encoding="utf-8")
    sections: Dict[str, str] = {}
    for match in SECTION_PATTERN.finditer(text):
        filename = match.group("filename").strip()
        body = match.group("body").strip("\n")
        sections[filename] = body
    if not sections:
        raise ValueError(f"No sections matched in {source}")
    return sections


def load_targets_from_file(path: Path) -> List[str]:
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Targets file not found: {path}") from exc

    targets: List[str] = []
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        targets.append(stripped)

    if not targets:
        raise ValueError(f"Targets file {path} does not contain any filenames.")
    return targets


def resolve_targets(requested: Iterable[str]) -> Dict[str, Path]:
    return {name: OUTPUT_DIR / name for name in requested}


def write_and_verify(path: Path, content: str) -> None:
    normalized = content.rstrip("\n") + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(normalized, encoding="utf-8")
    written = path.read_text(encoding="utf-8")
    if written != normalized:
        raise ValueError(f"Verification failed for {path}")


def main(argv: Iterable[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Extract Step 0.3 documents from .agentdoc/text.txt."
    )
    parser.add_argument(
        "filenames",
        nargs="*",
        help="Target filenames to emit (overrides targets file).",
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help=f"Source file to parse (default: {DEFAULT_SOURCE})",
    )
    parser.add_argument(
        "--targets-file",
        type=Path,
        help=(
            "Path to a text file listing target filenames (one per line, "
            f"default: {DEFAULT_TARGET_FILE if DEFAULT_TARGET_FILE.exists() else 'none'})."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview the sections that would be written without touching the filesystem.",
    )
    args = parser.parse_args(argv)

    sections = extract_sections(args.source)

    if args.filenames:
        requested = list(args.filenames)
    else:
        targets_file = args.targets_file or DEFAULT_TARGET_FILE
        if not targets_file.exists():
            raise SystemExit(
                "No target filenames provided. Pass explicit filenames or supply --targets-file."
            )
        requested = load_targets_from_file(targets_file)

    targets = resolve_targets(requested)

    missing = [name for name in requested if name not in sections]
    if missing:
        raise SystemExit(f"Missing sections for: {', '.join(missing)}")

    for name, destination in targets.items():
        if args.dry_run:
            status = "exists" if destination.exists() else "missing"
            print(f"[DRY-RUN] {name} -> {destination.relative_to(ROOT)} ({status})")
            continue
        write_and_verify(destination, sections[name])
        lines = sections[name].count("\n") + 1
        print(f"[WRITE] {name} -> {destination.relative_to(ROOT)} ({lines} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))