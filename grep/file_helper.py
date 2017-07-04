"""Supplies relevant files for grep.py."""

import os
import sys


def get_next_file(caller_dir, is_recursive):
    """Generates next file to be searched."""

    assert type(caller_dir) is str
    assert type(is_recursive) is bool

    for root, dirs, files in os.walk(caller_dir):
        for f in files:

            # Environment specific file paths.
            file_path = os.path.normpath('{0}/{1}'.format(root, f))

            # Check if it is an actual file on disk.
            if os.path.isfile(file_path):
                yield file_path

        if is_recursive is False:
            break


def is_binary_file(file_path, block_size=512):
    """ If a file can't be decoded by ascii or there are NULL ('\x00') bytes 
        in the block, assume this is a binary file.
    """

    assert type(file_path) == str

    try:
        with open(file_path, 'rb') as f:
            block = f.read(block_size)

            if b'\x00' in block:
                # Files with null bytes are binary
                return True
            elif not block:
                # An empty file is considered a valid text file
                return False

            try:
                block.decode('ascii')
                return False

            except UnicodeDecodeError:
                return True

    except IOError as io_error:
        sys.stderr.write('Error occurred during is_binary_file check:\n\t{}'.format(io_error))
        return False


# TODO implement
def with_read(function):

    def wrapper(file_path):
        pass

    return wrapper