import argparse
import re
import shutil
from pathlib import Path
from typing import List

IGNORED_DIRS = {
    ".venv",
    "venv",
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    ".idea",
    ".vscode",
    "dist",
    "build",
    "*.egg-info",
}

IGNORED_EXTENSIONS = {
    ".pyc",
    ".pyo",
    ".pyd",
    ".so",
    ".dll",
    ".dylib",
    ".exe",
    ".bin",
    ".dat",
    ".db",
    ".sqlite",
    ".lock",
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".ico",
    ".svg",
    ".pdf",
    ".zip",
    ".tar",
    ".gz",
    ".bz2",
    ".xz",
}

TEXT_EXTENSIONS = {
    ".py",
    ".txt",
    ".md",
    ".rst",
    ".toml",
    ".yaml",
    ".yml",
    ".json",
    ".ini",
    ".cfg",
    ".conf",
    ".sh",
    ".bat",
    ".ps1",
    ".html",
    ".css",
    ".js",
    ".ts",
    ".xml",
    ".Dockerfile",
    ".gitignore",
    ".dockerignore",
    "Makefile",
    "Dockerfile",
    ".tpl",
}


def normalize_name(name: str) -> tuple[str, str]:
    """Normalize name to underscore and hyphen versions."""
    underscore_name = name.replace("-", "_")
    hyphen_name = name.replace("_", "-")
    return underscore_name, hyphen_name


def should_ignore_path(path: Path, root: Path) -> bool:
    try:
        relative = path.relative_to(root)
        parts = relative.parts

        for part in parts:
            for ignored in IGNORED_DIRS:
                if ignored.endswith("*"):
                    pattern = ignored.replace("*", ".*")
                    if re.match(pattern, part):
                        return True
                elif part == ignored:
                    return True

        return False
    except ValueError:
        return True


def should_process_file(file_path: Path) -> bool:
    if file_path.suffix in IGNORED_EXTENSIONS:
        return False

    if file_path.suffix in TEXT_EXTENSIONS:
        return True

    if not file_path.suffix and file_path.name in TEXT_EXTENSIONS:
        return True

    return False


def collect_paths_to_rename(
    root: Path, old_underscore: str, old_hyphen: str
) -> List[Path]:
    """Collect all paths that need to be renamed."""
    paths_to_rename = []

    for path in root.rglob("*"):
        if should_ignore_path(path, root):
            continue

        name = path.name
        if old_underscore in name or old_hyphen in name:
            paths_to_rename.append(path)

    paths_to_rename.sort(key=lambda p: len(p.parts), reverse=True)

    return paths_to_rename


def rename_path(
    old_path: Path,
    old_underscore: str,
    old_hyphen: str,
    new_underscore: str,
    new_hyphen: str,
    dry_run: bool = False,
) -> Path:
    """Rename a single path."""
    old_name = old_path.name
    new_name = old_name

    new_name = new_name.replace(old_underscore, new_underscore)
    new_name = new_name.replace(old_hyphen, new_hyphen)

    if new_name != old_name:
        new_path = old_path.parent / new_name

        if not dry_run:
            if old_path.exists() and not new_path.exists():
                shutil.move(str(old_path), str(new_path))

        return new_path

    return old_path


def replace_in_file(
    file_path: Path,
    old_underscore: str,
    old_hyphen: str,
    new_underscore: str,
    new_hyphen: str,
    dry_run: bool = False,
) -> int:
    """Replace old name in file content."""
    if not should_process_file(file_path):
        return 0

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except (UnicodeDecodeError, PermissionError):
        return 0

    new_content = content
    new_content = new_content.replace(old_underscore, new_underscore)
    new_content = new_content.replace(old_hyphen, new_hyphen)

    changes = content.count(old_underscore) + content.count(old_hyphen)

    if new_content != content and changes > 0:
        if not dry_run:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)

        return changes

    return 0


def rename_project(root: Path, old_name: str, new_name: str, dry_run: bool = False):
    """Rename the entire project."""
    old_underscore, old_hyphen = normalize_name(old_name)
    new_underscore, new_hyphen = normalize_name(new_name)

    print(f"\nRenaming project{' (dry-run)' if dry_run else ''}:")
    print(f"  {old_underscore} / {old_hyphen} -> {new_underscore} / {new_hyphen}")

    paths_to_rename = collect_paths_to_rename(root, old_underscore, old_hyphen)

    if paths_to_rename:
        for path in paths_to_rename:
            rename_path(
                path, old_underscore, old_hyphen, new_underscore, new_hyphen, dry_run
            )

    total_changes = 0

    for file_path in root.rglob("*"):
        if not file_path.is_file():
            continue

        if should_ignore_path(file_path, root):
            continue

        changes = replace_in_file(
            file_path, old_underscore, old_hyphen, new_underscore, new_hyphen, dry_run
        )

        if changes > 0:
            total_changes += changes

    print(f"\nCompleted: {total_changes} replacements")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Rename project package name")

    parser.add_argument("old_name", help="Old project name (xx_xx_xx or xx-xx-xx)")
    parser.add_argument("new_name", help="New project name (yy_yy_yy or yy-yy-yy)")
    parser.add_argument("--dry-run", action="store_true", help="Preview mode only")
    parser.add_argument("--root", type=str, default=".", help="Project root directory")

    args = parser.parse_args()

    root = Path(args.root).resolve()

    if not root.exists():
        print(f"Error: Directory not found: {root}")
        return 1

    rename_project(root, args.old_name, args.new_name, args.dry_run)

    return 0


if __name__ == "__main__":
    exit(main())
