from __future__ import annotations

import argparse
import shutil
from pathlib import Path


DEFAULT_INPUT_FRAME_DIR = Path("/Volumes/PortableSSD/tutrtletest/turtlepond_2026-06-29_112336")
DEFAULT_OUTPUT_FRAME_DIR = DEFAULT_INPUT_FRAME_DIR / "frames"
DEFAULT_PNG_FOLDER_NAME = "frames"


def unique_destination(destination: Path) -> Path:
    """Return a non-existing destination path by adding a numeric suffix if needed."""
    if not destination.exists():
        return destination

    for index in range(1, 100_000):
        candidate = destination.with_name(
            f"{destination.stem}_{index}{destination.suffix}"
        )
        if not candidate.exists():
            return candidate

    raise RuntimeError(f"Could not find an available filename for {destination}")


def move_pngs(source_dir: Path, destination_dir: Path, dry_run: bool = False) -> int:
    if not source_dir.exists():
        raise FileNotFoundError(f"Source folder does not exist: {source_dir}")
    if not source_dir.is_dir():
        raise NotADirectoryError(f"Source path is not a folder: {source_dir}")

    png_files = sorted(
        path
        for path in source_dir.iterdir()
        if path.is_file() and path.suffix.lower() == ".png"
    )

    if not dry_run:
        destination_dir.mkdir(parents=True, exist_ok=True)

    for png_file in png_files:
        destination = unique_destination(destination_dir / png_file.name)
        print(f"{'Would move' if dry_run else 'Moving'} {png_file} -> {destination}")
        if not dry_run:
            shutil.move(str(png_file), str(destination))

    return len(png_files)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Move PNG files from a frames folder into a frames subfolder."
    )
    parser.add_argument(
        "source_dir",
        nargs="?",
        type=Path,
        default=DEFAULT_INPUT_FRAME_DIR,
        help=f"Folder containing PNG frames. Default: {DEFAULT_INPUT_FRAME_DIR}",
    )
    parser.add_argument(
        "--destination-dir",
        type=Path,
        help="Folder to move PNGs into. Default: SOURCE_DIR/png_frames",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be moved without changing files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_dir = args.source_dir.expanduser()
    destination_dir = (
        args.destination_dir.expanduser()
        if args.destination_dir
        else source_dir / DEFAULT_PNG_FOLDER_NAME
    )

    moved_count = move_pngs(source_dir, destination_dir, dry_run=args.dry_run)
    action = "would be moved" if args.dry_run else "moved"
    print(f"{moved_count} PNG file(s) {action}.")


if __name__ == "__main__":
    main()
