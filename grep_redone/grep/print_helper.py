import os
from clint.textui import colored

# TODO decorator coloring matched string red
def print_matched_files_full_path(matched_lines):

    for file, lines in matched_lines.iteritems():
        for line_num, line in lines.iteritems():
            print (colored.magenta(file + ':', True, False) +
                   str(line_num) + ':' + line),

def print_matched_files_relative_path(matched_lines):

    for file, lines in matched_lines.iteritems():
        for line_num, line in lines.iteritems():
            print (colored.magenta("./" + os.path.relpath(file) + ':', True, False) +
                   str(line_num) + ':' + line),

