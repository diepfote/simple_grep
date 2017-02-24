from clint.textui import colored

# TODO decorator coloring matched string red
def print_matched_files_full_path(matched_lines):

    for key, value in matched_lines.iteritems():
        for k, v in value.iteritems():
            print (colored.magenta(key + ':', True, False) +
                   str(k) + ':' + v),

