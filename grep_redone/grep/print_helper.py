"""Print matched items for grep_redone."""

import os
from clint.textui import colored


def print_matched_files_full_path(matched_lines, search_term):
    """Prints matched files in a dict using absolute paths."""

    assert type(matched_lines) == dict
    assert type(search_term) == str

    output = []

    for f, lines in matched_lines.iteritems():
        output.extend([(colored.magenta(os.path.normpath(f) + ':', True, False)
                        + colored.green(str(line_num)) + ':' + line)
                       for line_num, line in lines.iteritems()
                       ])

    # Remove last occurrence of new line
    output = [rreplace(f, '\n', '', 1) for f in output]

    # Color search term.
    if search_term:
        output = color_string(output, search_term, 'red')

    output.reverse()
    for f in iter(output):
        print f

    return output


def print_matched_files_relative_path(matched_lines, search_term):
    """Prints matched files in a dict using relative paths."""

    assert type(matched_lines) == dict
    assert type(search_term) == str

    output = []
    for f, lines in matched_lines.iteritems():
        if is_f_binary_file(f):
            output.extend(['Binary file ' + f + ' matches'])

        else:
            output.extend([(colored.magenta(os.path.normpath(os.path.relpath(f)) + ':', True, False)
                            + colored.green(str(line_num)) + ':' + line)
                           for line_num, line in lines.iteritems()
                           ])

    # Remove last occurrence of new line
    output = [rreplace(f, '\n', '', 1) for f in output]

    # Color search term.
    if search_term:
        output = color_string(output, search_term, 'red')

    output.reverse()
    for f in iter(output):
        print f

    return output


def color_string(list_to_edit, term, color):
    """Colors a single term/word inside a list."""

    assert type(list_to_edit) == list
    assert type(term) == str
    assert type(color) == str

    lightish_red = '\033[1;31m'
    no_color = '\033[0m'

    list_to_edit = [rreplace(f, term, (lightish_red + term + no_color), 1) for f in list_to_edit]
    if color == 'red':
        return list_to_edit

    return None


def rreplace(string_to_edit, old, new, num_occurrences):
    """Replace a term x times. Replacing is done from right to left."""

    assert type(string_to_edit) == str
    assert type(old) == str
    assert type(new) == str
    assert type(num_occurrences) == int

    li = string_to_edit.rsplit(old, num_occurrences)
    return new.join(li)


def is_f_binary_file(file_path, blocksize=512):
    """ Uses heuristics to guess whether the given file is text or binary,
        by reading a single block of bytes from the file.
        If more than 30% of the chars in the block are non-text, or there
        are NUL ('\x00') bytes in the block, assume this is a binary file.
    """

    assert type(file_path)

    is_binary_file = False
    character_table = (
        b''.join(chr(i) for i in range(32, 127)) +
        b'\n\r\t\f\b')

    try:
        f = open(file_path, 'rb')

        block = f.read(blocksize)
        if b'\x00' in block:
            # Files with null bytes are binary
            return False
        elif not block:
            # An empty file is considered a valid text file
            return True

        # Use translate's 'deletechars' argument to efficiently remove all
        # occurrences of _text_characters from the block
        nontext = block.translate(None, character_table)

        is_binary_file = not float(len(nontext)) / len(block) <= 0.30

    except IOError:
        pass

    return is_binary_file
