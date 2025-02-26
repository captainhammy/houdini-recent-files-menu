"""Callback function definitions for the package."""

# Houdini Recent Files Menu
from houdini_recent_files_menu import api

# Functions


def add_current_hip_to_recent_files(scriptargs: dict) -> None:
    """Callback to add the current hip file to the recent files list.

    Args:
        scriptargs: Callback event args.
    """
    api.add_current_hip_to_recent_files()
