"""Print matched items for grep_redone."""

import os
from clint.textui import colored

def print_matched_files_full_path(matched_lines, search_term):
    """Prints matched files in a dict using absolute paths."""

    assert type(matched_lines) == dict
    assert type(search_term) == str

    output = []

    for file, lines in matched_lines.iteritems():
        output.extend([(colored.magenta(os.path.normpath(file) + ':', True, False)
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
    for file, lines in matched_lines.iteritems():
        if is_binary_file(file):
            output.extend(['Binary file ' + file + ' matches'])

        else:
            output.extend([(colored.magenta(os.path.normpath(os.path.relpath(file)) + ':', True, False)
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

def color_string(list, term, color):
    """Colors a single term/word inside a list."""

    lightish_red = '\033[1;31m'
    no_color = '\033[0m'

    list = [rreplace(f, term, (lightish_red + term + no_color), 1) for f in list]
    if color == 'red':
        return list

    return None

def rreplace(f, old, new, num_occurrences):
    """Replace a term x times. Replacing is done from right to left."""

    li = f.rsplit(old, num_occurrences)
    print li
    return new.join(li)

def is_binary_file(file_path):
    """Test if a given file is binary."""

    textchars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
    is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))

    is_binary = True
    try:
        is_binary = is_binary_string(open(file_path, 'rb').read(1024))

    # For test cases
    except IOError:
        pass

    return is_binary