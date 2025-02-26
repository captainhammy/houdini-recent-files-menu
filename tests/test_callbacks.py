"""Test the houdini_recent_files_menu.callbacks module."""

# Houdini Recent Files Menu
from houdini_recent_files_menu import callbacks

# Tests


def test_add_current_hip_to_recent_files(tmp_path, mocker):
    """Test houdini_recent_files_menu.callbacks.add_current_hip_to_recent_files()."""
    test_path = (tmp_path / "test_hip_to_add.hip").as_posix()
    mocker.patch("hou.hipFile.path", return_value=test_path)

    mock_add = mocker.patch("houdini_recent_files_menu.api.add_current_hip_to_recent_files")

    callbacks.add_current_hip_to_recent_files({})

    mock_add.assert_called()
