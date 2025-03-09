"""Test the houdini_saved_file_menu.ui module."""

# Standard Library
import pathlib
from datetime import datetime

# Houdini Recent Files Menu
from houdini_recent_files_menu import api, constants, ui

# Tests


def test__build_display_table(mocker):
    """Test houdini_saved_file_menu.ui._build_display_table()."""
    mock_manager = mocker.patch("houdini_recent_files_menu.api.RecentFileManager")
    mock_manager.files = [
        api.RecentFile(pathlib.Path.cwd() / "file1.hipnc", 1710886869.0176835, "20.5.178"),
        api.RecentFile(pathlib.Path.home() / "file2.hipnc", 1738076128.2437088, None),
        api.RecentFile(pathlib.Path("/test/path/file3.hipnc"), 1722337846.0559487, "20.5.310"),
    ]

    expected = [
        f"1. $HIP/file1.hipnc        (20.5.178)  {datetime.fromtimestamp(1710886869.0176835).strftime(constants.TIMESTAMP_FORMAT)}",
        f"2. $HOME/file2.hipnc       (None)      {datetime.fromtimestamp(1738076128.2437088).strftime(constants.TIMESTAMP_FORMAT)}",
        f"3. /test/path/file3.hipnc  (20.5.310)  {datetime.fromtimestamp(1722337846.0559487).strftime(constants.TIMESTAMP_FORMAT)}",
    ]

    result = ui._build_display_table(mock_manager)

    assert result == expected


def test_build_recent_files_menu(mocker):
    """Test houdini_saved_file_menu.ui.build_recent_files_menu()."""
    rows = [
        "row1",
        "row2",
    ]

    mocker.patch("houdini_recent_files_menu.ui._build_display_table", return_value=rows)

    mock_file1 = mocker.MagicMock()
    mock_file2 = mocker.MagicMock()

    mock_manager = mocker.patch("houdini_recent_files_menu.api.RecentFileManager")
    mock_manager.return_value.files = [mock_file1, mock_file2]

    result = ui.build_recent_files_menu()

    mock_manager.return_value.refresh_data.assert_called()

    assert result == [
        mock_file1.path.as_posix.return_value,
        "row1",
        mock_file2.path.as_posix.return_value,
        "row2",
    ]
