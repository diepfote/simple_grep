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
    for f in output:
        print f

    return output


def print_matched_files_relative_path(matched_lines, search_term):
    """Prints matched files in a dict using relative paths."""

    assert type(matched_lines) == dict
    assert type(search_term) == str

    output = []
    for f, lines in matched_lines.iteritems():
        if is_binary_file(f):
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
    for f in output:
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
    print li
    return new.join(li)


def is_binary_file(file_path):
    """Test if a given file is binary."""

    assert type(file_path)

    textchars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
    # TODO FIX PEP8
    is_binary_string = lambda translate: bool(bytes.translate('', textchars))

    is_binary = True
    try:
        is_binary = is_binary_string(open(file_path, 'rb').read(1024))

    # For test cases
    except IOError:
        pass

    return is_binary
