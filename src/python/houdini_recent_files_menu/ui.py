"""Classes and functions for accessing and creating recently opened hip file entries."""

# Future
from __future__ import annotations

# Standard Library
import datetime

# Third Party
from tabulate import tabulate

# Houdini Recent Files Menu
from houdini_recent_files_menu import api, constants

# Houdini
import hou

# Non-Public Functions


def _build_display_table(manager: api.RecentFileManager) -> list[str]:
    rows = []

    for idx, recent_file in enumerate(manager.files):
        dt = datetime.datetime.fromtimestamp(recent_file.open_timestamp)

        rows.append([
            f"{idx + 1}. {hou.text.collapseCommonVars(recent_file.path.as_posix(), vars=constants.VARS_TO_COLLAPSE)}",
            f"({recent_file.save_version})",
            dt.strftime(constants.TIMESTAMP_FORMAT),
        ])

    # Generate the table data and split it back out into rows.
    return tabulate(rows, tablefmt="plain").split("\n")


# Functions


def build_recent_files_menu() -> list[str]:
    """Build the menu items for the Open Recent Files menu.

    Returns:
        The menu tokens and labels.
    """
    manager = api.RecentFileManager()
    # Always refresh the data before building the menu.
    manager.refresh_data()

    # Generate the table data and split it back out into rows.
    label_rows = _build_display_table(manager)

    menu: list[str] = []

    # Add each file and its label representation to the menu.
    for recent_file, row in zip(manager.files, label_rows):
        menu.extend((recent_file.path.as_posix(), row))

    return menu
