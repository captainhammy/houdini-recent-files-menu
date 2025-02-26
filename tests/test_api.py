"""Test the houdini_recent_files_menu.api module."""

# Standard Library
import json
import pathlib

# Third Party
import pytest

# Houdini Recent Files Menu
from houdini_recent_files_menu import api, constants

# Fixtures


@pytest.fixture(autouse=True)
def clear_cached_instance():
    """Fixture to automatically clear any Singleton instances."""
    api.RecentFileManager._instances.pop(api.RecentFileManager, None)


@pytest.fixture
def init_test_manager(mocker):
    """Callable fixture to initialize a RecentFileManager for testing without loading data."""
    mocker.patch.object(api.RecentFileManager, "__post_init__", return_value=None)

    def _create():
        return api.RecentFileManager()

    return _create


# Tests


class TestRecentFile:
    """Test the houdini_recent_files_menu.api.RecentFile object."""

    def test___init__(self, mocker):
        """Test object initialization."""
        mock_path = mocker.MagicMock(spec=pathlib.Path)

        inst = api.RecentFile(mock_path, 123456.789, "20.5.456")

        assert inst.path == mock_path
        assert inst.open_timestamp == 123456.789
        assert inst.save_version == "20.5.456"

    def test_as_json(self, mocker):
        """Test RecentFile.as_json()."""
        mock_path = mocker.MagicMock(spec=pathlib.Path)

        inst = api.RecentFile(mock_path, 123456.789, "20.5.456")

        result = inst.as_json()

        assert result == {
            mock_path.as_posix.return_value: {
                constants.DATA_NAME__OPEN_TIMESTAMP: 123456.789,
                constants.DATA_NAME__SAVE_VERSION: "20.5.456",
            }
        }


class TestRecentFileManager:
    """Test the houdini_recent_files_menu.api.RecentFileManager object."""

    def test___init__(self, init_test_manager):
        """Test object initialization."""
        inst = init_test_manager()
        assert inst.files == []
        assert inst.last_access_time == 0

    def test___post_init__(self, mocker):
        """Test object post initialization."""
        mock_init_from_disk = mocker.patch.object(api.RecentFileManager, "_init_from_disk")

        inst = api.RecentFileManager()
        assert inst.files == []
        assert inst.last_access_time == 0

        mock_init_from_disk.assert_called()

    def test__init_from_data(self, mocker, shared_datadir, init_test_manager):
        """Test RecentFileManager._init_from_data()."""
        data_file = shared_datadir / "test__init_from_data.json"
        with data_file.open() as handle:
            test_data = json.load(handle)

        # The test data contains 4 items, but we want to test out the logic to limit based
        # on the max display list, so patch it to 3 to ensure an item is removed.
        mocker.patch("houdini_recent_files_menu.constants.MAX_DISPLAY_FILES", 3)

        inst = init_test_manager()
        inst.files.append(None)  # Insert dummy data to test the files list is cleared.

        inst._init_from_data(test_data)

        assert len(inst.files) == 3

        # The expected ordering of file names from most recently opened to least recently.
        assert [f.path.name for f in inst.files] == ["file2.hipnc", "file4.hipnc", "file3.hipnc"]

    def test__init_from_disk(self, mocker, init_test_manager):
        """Test RecentFileManager._init_from_disk()."""
        mock_read = mocker.patch("houdini_recent_files_menu.filesystem.read_file_data")
        mock_update = mocker.patch.object(api.RecentFileManager, "update_last_access_time")
        mock_init_from_data = mocker.patch.object(api.RecentFileManager, "_init_from_data")

        inst = init_test_manager()
        inst._init_from_disk()

        mock_update.assert_called()
        mock_init_from_data.assert_called_with(mock_read.return_value)

    def test_add_recent_file(self, mocker, init_test_manager):
        """Test RecentFileManager.add_recent_file()."""
        mocker.patch("houdini_recent_files_menu.filesystem.read_file_data", return_value={})
        mock_write = mocker.patch("houdini_recent_files_menu.filesystem.write_file_data")

        mock_update = mocker.patch.object(api.RecentFileManager, "update_last_access_time")
        mock_init_from_data = mocker.patch.object(api.RecentFileManager, "_init_from_data")

        recent_data = {"/path/to/file1": {"foo": "bar"}}

        mock_recent = mocker.MagicMock(spec=api.RecentFile)
        mock_recent.as_json.return_value = recent_data

        inst = init_test_manager()
        inst.add_recent_file(mock_recent)

        mock_update.assert_called()
        mock_write.assert_called_with(recent_data)
        mock_init_from_data.assert_called_with(recent_data)

    @pytest.mark.parametrize(
        "last_modified,last_access,expect_update",
        (
            (10, 100, False),
            (100, 100, False),
            (110, 100, True),
        ),
    )
    def test_refresh_data(self, mocker, init_test_manager, last_modified, last_access, expect_update):
        """Test RecentFileManager.refresh_data()."""
        mocker.patch(
            "houdini_recent_files_menu.filesystem.get_source_file_modification_time", return_value=last_modified
        )

        mock_init_from_disk = mocker.patch.object(api.RecentFileManager, "_init_from_disk")

        inst = init_test_manager()
        inst.last_access_time = last_access

        inst.refresh_data()

        assert mock_init_from_disk.call_count == int(expect_update)

    def test_update_last_access_time(self, init_test_manager):
        """Test RecentFileManager.update_last_access_time()."""
        inst = init_test_manager()
        assert inst.last_access_time == 0

        inst.update_last_access_time()
        assert inst.last_access_time > 0


class Test__reduce_entries:
    """Test houdini_recent_files_menu.api._reduce_entries()."""

    def test_less_than(self, mocker):
        """Test _reduce_entries() with less than the max files."""
        mocker.patch("houdini_recent_files_menu.constants.MAX_RECENT_FILES", 2)

        mock_data = mocker.MagicMock(spec=dict)
        mock_data.__len__.return_value = 1

        result = api._reduce_entries(mock_data)
        assert result == mock_data

    def test_equal(self, mocker):
        """Test _reduce_entries() with the max files."""
        mocker.patch("houdini_recent_files_menu.constants.MAX_RECENT_FILES", 2)

        mock_data = mocker.MagicMock(spec=dict)
        mock_data.__len__.return_value = 2

        result = api._reduce_entries(mock_data)
        assert result == mock_data

    def test_greater_than(self, mocker):
        """Test _reduce_entries() with more than the max files."""
        mocker.patch("houdini_recent_files_menu.constants.MAX_RECENT_FILES", 2)

        test_data = {
            "/path/to/file3.hip": {
                constants.DATA_NAME__OPEN_TIMESTAMP: 25,
                constants.DATA_NAME__SAVE_VERSION: "20.5.789",
            },
            "/path/to/file1.hip": {
                constants.DATA_NAME__OPEN_TIMESTAMP: 45,
                constants.DATA_NAME__SAVE_VERSION: "20.5.123",
            },
            "/path/to/file2.hip": {
                constants.DATA_NAME__OPEN_TIMESTAMP: 35,
                constants.DATA_NAME__SAVE_VERSION: "20.5.456",
            },
        }

        result = api._reduce_entries(test_data)

        assert result == {
            "/path/to/file1.hip": {
                constants.DATA_NAME__OPEN_TIMESTAMP: 45,
                constants.DATA_NAME__SAVE_VERSION: "20.5.123",
            },
            "/path/to/file2.hip": {
                constants.DATA_NAME__OPEN_TIMESTAMP: 35,
                constants.DATA_NAME__SAVE_VERSION: "20.5.456",
            },
        }


@pytest.mark.parametrize("hip_version,expected_version", (("20.5.456", "20.5.456"), ("", None)))
def test_add_current_hip_to_recent_files(mocker, hip_version, expected_version):
    """Test houdini_recent_files_menu.api.add_path_to_recent_files()."""
    mocker.patch("hou.hipFile.path", return_value="/path/to/file1.hip")
    mocker.patch("time.time", return_value=123456)
    mocker.patch("hou.text.expandString", return_value=hip_version)

    mock_mgr = mocker.patch("houdini_recent_files_menu.api.RecentFileManager")
    mock_recent = mocker.patch("houdini_recent_files_menu.api.RecentFile")

    api.add_current_hip_to_recent_files()

    mock_recent.assert_called_with(
        pathlib.Path("/path/to/file1.hip"),
        123456,
        expected_version,
    )

    mock_mgr.return_value.add_recent_file.assert_called_with(mock_recent.return_value)
