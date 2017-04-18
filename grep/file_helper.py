"""Supplies relevant files for grep.py."""

import os
import sys


def get_next_file(caller_dir, is_recursive):
    """Creates a list containing all files to be searched."""

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


def is_binary_file(file_path, blocksize=512):
    """ If more than 0% of the chars in the block are non-text or
        file can't be decoded by ascii, or there are NUL ('\x00') bytes 
        in the block, assume this is a binary file.
    """

    assert type(file_path) == str

    try:
        with open(file_path, 'rb') as f:
            block = f.read(blocksize)

            assert block is not None

            if b'\x00' in block:
                # Files with null bytes are binary
                return True
            elif not block:
                # An empty file is considered a valid text file
                return False


            # Py3
            # Files throwing UnicodeDecodeError are seen as binary files.
            if sys.version_info[0] > 2:
                try:
                    block.decode('ascii')
                    return False

                except UnicodeDecodeError:
                    return True

            # Py2
            # Use translate's 'deletechars' argument to efficiently remove all
            # occurrences of _text_characters from the block
            else:
                character_table = (b''.join(chr(i) for i in range(32, 127)) + b'\n\r\t\f\b')
                nontext = block.translate(None, bytes(character_table))

                assert nontext is not None

                return not float(len(nontext)) / len(block) <= 0

    except IOError as ioerror:
        print ('Error while reading file:\n\t{}'.format(ioerror))
        return False
