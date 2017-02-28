"""Print matched items for grep_redone."""

import os
from clint.textui import colored

def print_matched_files_full_path(matched_lines, search_term):

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
        output = [rreplace(f, search_term, ('\033[1;31m' + search_term + '\033[0m'), 1 ) for f in output]

    output.reverse()
    for f in output:
        print f

    return output

def print_matched_files_relative_path(matched_lines, search_term):

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

    # print "\033[59m" + search_term
    # print [colored.green(search_term, True, False).__str__()]
    # Color search term.
    if search_term:
        output = [rreplace(f, search_term, ('\033[1;31m' + search_term + '\033[0m '), 1 ) for f in output]

    output.reverse()
    for f in output:
        print f

    return output

def rreplace(string, old, new, num_occurrences):


    li = string.rsplit(old, num_occurrences)
    return new.join(li)

def is_binary_file(file_path):

    textchars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
    is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))

    is_binary = False
    try:
        is_binary_string(open(file_path, 'rb').read(1024))

    # For test cases
    except IOError:
        pass

    return is_binary