from clint.textui import colored

# TODO decorator coloring matched string red
def print_matched_files(matched_file_dict):
    for key, value in matched_file_dict.iteritems():
        for k, v in value.iteritems():
            print (colored.magenta("./" + key + ':', True, False) +
                   str(k) + ':' + v),