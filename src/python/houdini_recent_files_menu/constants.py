"""Constants and global values for use in the package."""

RECENT_FILE_SOURCE_FILE_NAME = "recent_houdini_files.json"
"""The source data file name."""

RECENT_FILE_SOURCE_VAR_NAME = "HOUDINI_RECENT_FILES_MENU_FILE"
"""Environment variable name that can point to the source file."""

MAX_RECENT_FILES = 100
"""Maximum number of entries to keep in the file."""

MAX_DISPLAY_FILES = 100
"""Maximum number of entries to display in the menu."""

# Key names for storing data in the file.
DATA_NAME__OPEN_TIMESTAMP = "open_timestamp"
DATA_NAME__SAVE_VERSION = "save_version"

VARS_TO_COLLAPSE = ("$HIP", "$HOME")
"""Variables to collapse when displaying file paths in the menu."""

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M"
"""Timestamp format for UI display."""
