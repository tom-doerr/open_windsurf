"""
Tests for the open_windsurf.core module.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from open_windsurf.core import validate_paths


def test_validate_paths_with_valid_paths():
    """Test that validate_paths returns valid paths."""
    with tempfile.TemporaryDirectory() as temp_dir:
        paths = [temp_dir]
        valid_paths = validate_paths(paths)
        assert valid_paths == [str(Path(temp_dir).resolve())]


def test_validate_paths_with_invalid_paths(capsys):
    """Test that validate_paths filters out invalid paths."""
    with tempfile.TemporaryDirectory() as temp_dir:
        valid_path = temp_dir
        invalid_path = "/path/does/not/exist"
        
        paths = [valid_path, invalid_path]
        valid_paths = validate_paths(paths)
        
        assert valid_paths == [str(Path(valid_path).resolve())]
        
        # Check that a warning was printed for the invalid path
        captured = capsys.readouterr()
        assert "Warning: Path does not exist" in captured.err
        assert invalid_path in captured.err


def test_validate_paths_with_all_invalid_paths():
    """Test that validate_paths returns an empty list when all paths are invalid."""
    paths = ["/path/does/not/exist", "/another/invalid/path"]
    valid_paths = validate_paths(paths)
    assert valid_paths == []


def test_validate_paths_with_home_directory():
    """Test that validate_paths correctly expands the home directory."""
    home_path = "~"
    valid_paths = validate_paths([home_path])
    assert valid_paths == [str(Path.home())]
