#!/usr/bin/env python3
"""
UnitiveFiles - Python version
Combine files of the same type into a single file.
"""

import os
import sys
from pathlib import Path


def print_usage():
    """Print usage instructions."""
    print("Usage: python unitivefiles.py <directory> <extension>")
    print("Example: python unitivefiles.py ./data txt")


def list_matching_files(root_dir, ext_normalized, output_path):
    """
    Recursively find all files matching the given extension.
    
    Args:
        root_dir: Root directory to search
        ext_normalized: Extension to match (lowercase, without dot)
        output_path: Path to exclude from results
    
    Returns:
        List of matching file paths
    """
    results = []
    skip_dirs = {"node_modules", ".git"}
    
    for root, dirs, files in os.walk(root_dir):
        # Modify dirs in-place to skip certain directories
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            full_path = os.path.join(root, file)
            
            if os.path.abspath(full_path) == os.path.abspath(output_path):
                continue
            
            _, file_ext = os.path.splitext(file)
            if file_ext.lower() == f".{ext_normalized}":
                results.append(full_path)
    
    return results


def combine_files(directory_arg, extension_arg):
    """
    Combine all files of the same type into a single file.
    
    Args:
        directory_arg: Directory path
        extension_arg: File extension to match
    
    Raises:
        ValueError: If directory does not exist or extension is empty
    """
    root_dir = os.path.abspath(directory_arg)
    
    if not os.path.isdir(root_dir):
        raise ValueError("Provided path is not a directory.")
    
    ext_normalized = (
        extension_arg[1:].lower()
        if extension_arg.startswith(".")
        else extension_arg.lower()
    )
    
    if not ext_normalized:
        raise ValueError("Extension cannot be empty.")
    
    output_path = os.path.join(
        root_dir, f"{ext_normalized}_combined.{ext_normalized}"
    )
    
    files = list_matching_files(root_dir, ext_normalized, output_path)
    
    # Sort alphabetically by relative path
    files.sort(key=lambda f: os.path.relpath(f, root_dir))
    
    contents = []
    for file_path in files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                contents.append(f.read())
        except Exception as e:
            print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(contents))
    
    print(f"Combined {len(files)} file(s) into: {output_path}")


def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)
    
    directory_arg = sys.argv[1]
    extension_arg = sys.argv[2]
    
    try:
        combine_files(directory_arg, extension_arg)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
