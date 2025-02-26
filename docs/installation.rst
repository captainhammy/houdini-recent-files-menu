============
Installation
============

------------
Requirements
------------

This package requires general Python package dependencies, as well as custom Houdini packages. Please ensure
they are appropriately installed prior to launching Houdini.

PyPi packages (detailed in ``requirements.txt``)

* `python-singleton <https://pypi.org/project/python-singleton/>`_
* `tabulate <https://pypi.org/project/tabulate/>`_

Custom Tools

* `you-can-call-me-houdini <https://github.com/captainhammy/you-can-call-me-houdini>`_

------
Source
------

In order to install this tool you'll first need to get a copy of the files from `Github <https://github.com/captainhammy/houdini-recent-files-menu>`_. You
can either clone the repository or download and extract an official release.

-----------------
Adding to Houdini
-----------------

``houdini-recent-files-menu`` supports being loaded into Houdini in multiple ways:

    - `Houdini Packages <https://www.sidefx.com/docs/houdini/ref/plugins.html>`_
    - `Rez packages <https://rez.readthedocs.io/en/stable/>`_
    - Standard path based setup

^^^^^^^^^^^^^^^
Houdini Package
^^^^^^^^^^^^^^^

This tool comes with a ``houdini_recent_files_menu.json`` file which can be used to tell Houdini how to load
the package. Add the containing directory to ``$HOUDINI_PACKAGE_DIR`` or one of the other methods defined
`here <https://www.sidefx.com/docs/houdini/ref/plugins.html#using_packages>`_

^^^^^^^^^^^^
Rez Package
^^^^^^^^^^^^

This package supports Rez packaging via a ``package.py`` file in the root directory.

^^^^^^^^^^^^^^^^
Path Based Setup
^^^^^^^^^^^^^^^^

In order to manually setup the tooling you'll need to do the following:

    - Add the ``src/houdini`` path to ``$HOUDINI_PATH``
    - Add the ``src/python`` path to ``$PYTHONPATH``
