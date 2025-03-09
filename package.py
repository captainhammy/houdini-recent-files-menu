"""Package definition file for houdini_recent_files_menu."""

name = "houdini_recent_files_menu"

description = "More advanced Open Recent Files menu."


@early()
def version() -> str:
    """Get the package version.

    Because this project is not versioned we'll just use the short git hash as the version.

    Returns:
        The package version.
    """
    return "0.1.0"


authors = ["graham thompson"]

requires = [
    "python_singleton",
    "tabulate",
    "you_can_call_me_houdini",
]

build_system = "cmake"

tests = {
    "unit": {
        "command": "coverage erase && hython -m pytest tests",
        "requires": ["pytest", "pytest_cov", "pytest_datadir", "pytest_mock", "pytest_sugar"],
    }
}


def commands():
    """Run commands on package setup."""
    env.PYTHONPATH.prepend("{root}/python")

    # We don't want to set HOUDINI_PATH when testing as this will cause Houdini to
    # load and run various things at startup and interfere with test coverage.
    if "HOUDINI_PACKAGE_TESTING" not in env:
        env.HOUDINI_PATH.prepend("{root}/houdini")


def pre_test_commands():
    """Run commands before testing."""
    # Set an indicator that a test is running, so we can set paths differently.
    env.HOUDINI_PACKAGE_TESTING = True
