"""
Tests for the open_windsurf.cli module.
"""

import sys
from unittest.mock import MagicMock, patch

import pytest

from open_windsurf.cli import main, parse_arguments


def test_parse_arguments():
    """Test that parse_arguments correctly parses command line arguments."""
    with patch('sys.argv', ['open-windsurf', 'path1', 'path2', '--wait', '--profile', 'test']):
        args = parse_arguments()
        
        assert args.paths == ['path1', 'path2']
        assert args.wait is True
        assert args.profile == 'test'
        assert args.new_window is False


@patch('open_windsurf.cli.validate_paths')
@patch('open_windsurf.cli.open_windsurf')
def test_main_with_valid_paths(mock_open_windsurf, mock_validate_paths):
    """Test that main correctly processes valid paths."""
    # Setup mocks
    mock_validate_paths.return_value = ['/valid/path1', '/valid/path2']
    mock_process = MagicMock()
    mock_open_windsurf.return_value = mock_process
    
    # Call main with mocked arguments
    with patch('sys.argv', ['open-windsurf', 'path1', 'path2']):
        with patch('open_windsurf.cli.parse_arguments') as mock_parse_args:
            mock_args = MagicMock()
            mock_args.paths = ['path1', 'path2']
            mock_args.wait = False
            mock_args.user_data_dir = None
            mock_args.profile = None
            mock_args.new_window = False
            mock_parse_args.return_value = mock_args
            
            main()
    
    # Verify validate_paths was called with the correct arguments
    mock_validate_paths.assert_called_once_with(['path1', 'path2'])
    
    # Verify open_windsurf was called for each valid path
    assert mock_open_windsurf.call_count == 2
    mock_open_windsurf.assert_any_call(
        path='/valid/path1',
        wait=False,
        user_data_dir=None,
        profile=None,
        new_window=False
    )
    mock_open_windsurf.assert_any_call(
        path='/valid/path2',
        wait=False,
        user_data_dir=None,
        profile=None,
        new_window=False
    )


@patch('open_windsurf.cli.validate_paths')
@patch('open_windsurf.cli.sys.exit')
def test_main_with_no_valid_paths(mock_exit, mock_validate_paths):
    """Test that main exits with an error when no valid paths are provided."""
    # Setup mocks
    mock_validate_paths.return_value = []
    
    # Call main with mocked arguments
    with patch('sys.argv', ['open-windsurf', 'invalid_path']):
        with patch('open_windsurf.cli.parse_arguments') as mock_parse_args:
            mock_args = MagicMock()
            mock_args.paths = ['invalid_path']
            mock_parse_args.return_value = mock_args
            
            main()
    
    # Verify sys.exit was called with exit code 1
    mock_exit.assert_called_once_with(1)
