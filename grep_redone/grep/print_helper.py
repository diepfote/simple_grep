"""Print matched items for grep_redone."""

import os
from clint.textui import colored

from grep_redone.grep import file_helper


def generate_output_for_matched_files_full_path(matched_files_and_lines, search_term):
    """Prints matched files in a dict using absolute paths."""

    assert type(matched_files_and_lines) == dict
    assert type(search_term) == str

    output = []
    for f, lines in matched_files_and_lines.iteritems():
        output.extend([(colored.magenta(os.path.normpath(f)) + colored.green(':')
                        + colored.green(str(line_num)) + colored.green(':') + line)
                       for line_num, line in lines.iteritems()
                       ])

    # Remove last occurrence of new line
    output = [''.join(f.rsplit('\n', 1)) for f in output]

    # Color term and print
    for line in color_matched(output, search_term):
        print line

    return output


def generate_output_for_matched_files_relative_path(matched_files_and_lines, search_term):
    """Prints matched files in a dict using relative paths."""

    assert type(matched_files_and_lines) == dict
    assert type(search_term) == str

    output = []
    for f, lines in matched_files_and_lines.iteritems():
        if file_helper.is_f_binary_file(f):
            output.extend(['Binary file ' + f + ' matches'])

        else:
            output.extend([(colored.magenta(os.path.normpath(os.path.relpath(f))) + colored.blue(':')
                            + colored.green(str(line_num)) + colored.blue(':') + line)
                           for line_num, line in lines.iteritems()
                           ])

    # Remove last occurrence of new line
    output = [''.join(f.rsplit('\n', 1)) for f in output]

    # Color term and print
    for line in color_matched(output, search_term):
        print line

    return output



def color_term_in_string(func):
    def func_wrapper(list_to_edit, term):
        assert type(list_to_edit) == list
        assert type(term) == str

        lightish_red = '\033[1;31m'
        no_color = '\033[0m'
        return [(lightish_red + term + no_color).join(f.rsplit(term, 1)) for f in func(list_to_edit, term)]
    return func_wrapper


@color_term_in_string
def color_matched(output, search_term):
    return output
