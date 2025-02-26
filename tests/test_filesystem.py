"""Test the houdini_recent_files_menu.filesystem module."""

# Standard Library
import json
import os
import pathlib

# Houdini Recent Files Menu
from houdini_recent_files_menu import constants, filesystem

# Tests


def test_get_source_file_modification_time(mocker):
    """Test houdini_recent_files_menu.filesystem.get_source_file_modification_time()."""
    expected_time = 1234567.890

    mock_stat = mocker.MagicMock(spec=os.stat_result)
    mock_stat.st_mtime = expected_time

    mock_path = mocker.MagicMock(spec=pathlib.Path)
    mock_path.stat.return_value = mock_stat

    mocker.patch(
        "houdini_recent_files_menu.filesystem.source_file_path",
        return_value=mock_path,
    )

    result = filesystem.get_source_file_modification_time()
    assert result == expected_time


def test_read_file_data(mocker, shared_datadir):
    """Test houdini_recent_files_menu.filesystem.read_file_data()."""
    data_file = shared_datadir / "test_read_file_data.json"

    mocker.patch("houdini_recent_files_menu.filesystem.source_file_path", return_value=data_file)

    result = filesystem.read_file_data()

    assert result == {"this": ["is", "a", "test"]}


class Test_source_file_path:
    """Test houdini_recent_files_menu.filesystem.source_file_path()."""

    def test_from_env(self, tmp_path, monkeypatch):
        """Test when the file path is defined by the environment variable."""
        test_file = tmp_path / "source_data.json"

        monkeypatch.setenv(constants.RECENT_FILE_SOURCE_VAR_NAME, test_file.as_posix())

        assert filesystem.source_file_path() == test_file

    def test_default(self, tmp_path, monkeypatch, mocker):
        """Test the default path when no environment variable is defined."""
        home_path = tmp_path / "home"
        mocker.patch("pathlib.Path.home", return_value=home_path)

        monkeypatch.delenv(constants.RECENT_FILE_SOURCE_VAR_NAME)

        assert filesystem.source_file_path() == home_path / constants.RECENT_FILE_SOURCE_FILE_NAME


def test_write_file_data(tmp_path, mocker):
    """Test houdini_recent_files_menu.filesystem.write_file_data()."""
    data_file = tmp_path / "test_write_file_data.json"
    mocker.patch("houdini_recent_files_menu.filesystem.source_file_path", return_value=data_file)

    test_data = {"this": ["is", "a", "test"]}
    filesystem.write_file_data(test_data)

    with data_file.open() as fp:
        result = json.load(fp)

    assert result == test_data
