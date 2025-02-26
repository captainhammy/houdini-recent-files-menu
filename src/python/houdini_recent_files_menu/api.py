"""Classes and functions for accessing and creating recently opened hip file entries."""

# Future
from __future__ import annotations

# Standard Library
import dataclasses
import operator
import pathlib
import time

# Third Party
import singleton

# Houdini Recent Files Menu
from houdini_recent_files_menu import constants, filesystem

# Houdini
import hou

# Classes


@dataclasses.dataclass
class RecentFile:
    """An object representing a recently opened hip file."""

    path: pathlib.Path
    open_timestamp: float
    save_version: str | None

    def as_json(self) -> dict:
        """Return a json representation of the recent file data."""
        return {
            self.path.as_posix(): {
                constants.DATA_NAME__OPEN_TIMESTAMP: self.open_timestamp,
                constants.DATA_NAME__SAVE_VERSION: self.save_version,
            }
        }


@dataclasses.dataclass
class RecentFileManager(metaclass=singleton.Singleton):
    """Manage to handle accessing and updating the recently saved files list."""

    files: list[RecentFile] = dataclasses.field(default_factory=list, init=False)
    last_access_time: float = dataclasses.field(default=0, init=False)

    def __post_init__(self) -> None:
        self._init_from_disk()

    def _init_from_data(self, data: dict) -> None:
        """Initialize the internal recent files list from the data.

        Args:
            data: The source recent file data.
        """
        self.files.clear()

        read_items = []

        for hip_path, extra_data in data.items():
            recent_file = RecentFile(
                pathlib.Path(hip_path),
                extra_data[constants.DATA_NAME__OPEN_TIMESTAMP],
                extra_data.get(constants.DATA_NAME__SAVE_VERSION),
            )
            read_items.append(recent_file)

        read_items.sort(key=operator.attrgetter("open_timestamp"), reverse=True)

        # Limit the number of items based on the max to display.
        self.files = read_items[: min(constants.MAX_DISPLAY_FILES, len(read_items))]

    def _init_from_disk(self) -> None:
        """Initialize recent files list from the source file on disk."""
        data = filesystem.read_file_data()
        self.update_last_access_time()

        self._init_from_data(data)

    def add_recent_file(self, recent_file: RecentFile) -> None:
        """Add a recent file item to the list.

        Args:
            recent_file: The recent file to add.
        """
        # Get the latest version of the data from disk.
        data = filesystem.read_file_data()

        # Add the information for the required file.
        data.update(recent_file.as_json())

        # Reduce the entries, if necessary.
        data = _reduce_entries(data)

        # Write the update data back to the disk.
        filesystem.write_file_data(data)

        # Update the access time to reflect that it was just written to
        # with the most up-to-date data.
        self.update_last_access_time()

        # Rebuild the internal data with the current state.
        self._init_from_data(data)

    def refresh_data(self) -> None:
        """Refresh the files list from disk, if necessary.

        This will check the file modified time against the last access time and reload
        the data if necessary.
        """
        modified = filesystem.get_source_file_modification_time()

        if modified > self.last_access_time:
            self._init_from_disk()

    def update_last_access_time(self) -> None:
        """Update the internal time of when the file was last accessed."""
        self.last_access_time = time.time()


# Non-Public Functions


def _reduce_entries(data: dict) -> dict:
    """Reduce the number of entries if necessary.

    In the event that there are more entries than allowable, the entries will be
    sorted by most recently opened, and the oldest one(s) will be discarded.

    Args:
        data: The data to reduce.

    Returns:
        The reduced data, if necessary.
    """
    # If we're not at the max, don't do anything.
    if len(data) <= constants.MAX_RECENT_FILES:
        return data

    # Sort the data by most recent and discard any extra older entries.
    return dict(
        sorted(data.items(), key=lambda item: item[1][constants.DATA_NAME__OPEN_TIMESTAMP], reverse=True)[
            : constants.MAX_RECENT_FILES
        ]
    )


# Functions


def add_current_hip_to_recent_files() -> None:
    """Add the current hip file path to the recent files list."""
    hip_file = pathlib.Path(hou.hipFile.path())
    version = hou.text.expandString("$_HIP_SAVEVERSION") or None

    recent_file = RecentFile(hip_file, time.time(), version)
    RecentFileManager().add_recent_file(recent_file)
