"""Supplies relevant files for grep.py."""

import os

# TODO refactor into a generator
def get_all_files(caller_dir, is_recursive):
    """Creates a list containing all files to be searched."""

    assert type(caller_dir) is str
    assert type(is_recursive) is bool

    file_paths = []

    for root, dirs, files in os.walk(caller_dir):
        for f in files:

            # Environment specific file paths.
            file_path = os.path.normpath('{0}/{1}'.format(root, f))

            # Check if it is an actual file on disk.
            if os.path.isfile(file_path):
                file_paths.extend([file_path])

        if is_recursive is False:
            break

    return file_paths
