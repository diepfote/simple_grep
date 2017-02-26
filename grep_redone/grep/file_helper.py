"""Supplies relevant files for grep.py."""

import os

def get_all_files(caller_dir, is_recursive):

    assert type(is_recursive) is bool, "Should always be a boolean."

    file_paths = []

    for root, dirs, files in os.walk(caller_dir):
        for f in files:

            if os.path.isfile(root + "/" + f):
                # Prepend root to every file path
                file_paths.extend(['{0}/{1}'.format(root, f)])

        if is_recursive is False:
            break

    return file_paths