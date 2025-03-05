#!/usr/bin/env python3
"""
Open Windsurf (VS Code-based) instances for multiple directories.

This script allows you to specify multiple directories/paths via command line
and opens a separate Windsurf instance for each one.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Open Windsurf instances for multiple directories/paths."
    )
    parser.add_argument(
        "paths", 
        nargs="+", 
        help="Directories or files to open in separate Windsurf instances"
    )
    parser.add_argument(
        "--wait", 
        action="store_true", 
        help="Wait for the Windsurf instances to close before exiting"
    )
    parser.add_argument(
        "--user-data-dir",
        help="Specify a custom user data directory for all instances"
    )
    parser.add_argument(
        "--profile",
        help="Use a specific profile for all instances"
    )
    parser.add_argument(
        "--new-window", 
        action="store_true", 
        help="Force opening in new windows"
    )
    
    return parser.parse_args()


def validate_paths(paths: List[str]) -> List[str]:
    """
    Validate that all provided paths exist.
    
    Args:
        paths: List of path strings to validate
        
    Returns:
        List of valid, absolute paths
    """
    valid_paths = []
    
    for path_str in paths:
        path = Path(path_str).expanduser().resolve()
        
        if not path.exists():
            print(f"Warning: Path does not exist: {path}", file=sys.stderr)
            continue
            
        valid_paths.append(str(path))
    
    return valid_paths


def open_windsurf(
    path: str, 
    wait: bool = False,
    user_data_dir: Optional[str] = None,
    profile: Optional[str] = None,
    new_window: bool = False
) -> subprocess.Popen:
    """
    Open a Windsurf instance for the specified path.
    
    Args:
        path: Path to open
        wait: Whether to wait for Windsurf to close
        user_data_dir: Custom user data directory
        profile: Profile to use
        new_window: Force opening in a new window
        
    Returns:
        Subprocess handle
    """
    cmd = ["windsurf"]
    
    if wait:
        cmd.append("--wait")
    
    if user_data_dir:
        cmd.extend(["--user-data-dir", user_data_dir])
    
    if profile:
        cmd.extend(["--profile", profile])
    
    if new_window:
        cmd.append("--new-window")
    
    cmd.append(path)
    
    print(f"Opening Windsurf for: {path}")
    return subprocess.Popen(cmd)


def main():
    """Main entry point."""
    args = parse_arguments()
    
    # Validate paths
    valid_paths = validate_paths(args.paths)
    
    if not valid_paths:
        print("Error: No valid paths provided.", file=sys.stderr)
        sys.exit(1)
    
    # Open Windsurf for each path
    processes = []
    for path in valid_paths:
        process = open_windsurf(
            path=path,
            wait=args.wait,
            user_data_dir=args.user_data_dir,
            profile=args.profile,
            new_window=args.new_window
        )
        processes.append(process)
    
    # If wait flag is set, wait for all processes to complete
    if args.wait:
        for i, process in enumerate(processes):
            print(f"Waiting for Windsurf instance {i+1}/{len(processes)} to close...")
            process.wait()
    
    print(f"Opened {len(valid_paths)} Windsurf instance(s)")


if __name__ == "__main__":
    main()
