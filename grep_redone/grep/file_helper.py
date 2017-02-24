"""Supplies relevant files for grep.py."""

import os

def get_all_files(caller_dir, is_recursive):
    file_paths = []

    for root, dirs, files in os.walk(caller_dir):

        # Prepend root to every file path
        file_paths.extend(['{0}/{1}'.format(root, file) for file in files])

        assert type(is_recursive) is bool, "Should always be a boolean."
        if is_recursive is False:
            break

    return file_paths