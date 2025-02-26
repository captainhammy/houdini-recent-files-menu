"""Filesystem related operations for the package."""

# Future
from __future__ import annotations

# Standard Library
import json
import os
import pathlib

# Houdini Recent Files Menu
from houdini_recent_files_menu import constants

# Functions


def get_source_file_modification_time() -> float:
    """Get the modification timestamp of the source file.

    Returns:
        The modification timestamp of the source file.
    """
    return source_file_path().stat().st_mtime


def read_file_data() -> dict:
    """Read the recent file data fom disk."""
    with source_file_path().open() as handle:
        return json.load(handle)


def source_file_path() -> pathlib.Path:
    """Get the path for the source data file.

    This uses $HOUDINI_RECENT_FILES_MENU_FILE if it exists, otherwise $HOME/recent_houdini_files.json

    Returns:
        The path for the source data file.
    """
    return pathlib.Path(
        os.environ.get("HOUDINI_RECENT_FILES_MENU_FILE", pathlib.Path.home() / constants.RECENT_FILE_SOURCE_FILE_NAME)
    )


def write_file_data(data: dict) -> None:
    """Write the data to the disk file.

    Args:
        data: The recent file data to write.
    """
    with source_file_path().open(mode="w") as handle:
        json.dump(data, handle, indent=4)
