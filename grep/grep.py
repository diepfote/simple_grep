"""Search functionality for grep_redone."""

import time
import re
import sre_constants

import print_helper
import file_helper


# TODO abstract IO
class Searcher(object):
    """Greps search functionality implemented as a class."""

    def __init__(self, caller_dir,
                 search_term,
                 specific_file,
                 is_recursive,
                 is_abs_path,
                 is_regex_pattern,
                 is_search_line_by_line,
                 is_from_stdin):

        assert type(caller_dir) == str
        assert type(search_term) == str
        assert type(specific_file) == str
        assert type(is_recursive) == bool
        assert type(is_abs_path) == bool
        assert type(is_regex_pattern) == bool
        assert type(is_search_line_by_line) == bool
        assert type(is_from_stdin) == bool

        self.caller_dir = caller_dir
        self.search_term = search_term
        self.specific_file = specific_file
        self.is_recursive = is_recursive
        self.is_abs_path = is_abs_path
        self.is_regex_pattern = is_regex_pattern
        self.is_search_line_by_line = is_search_line_by_line
        self.is_from_stdin = is_from_stdin

    def run(self):
        """Runs search_wrapper using a file if specified.."""

        all_matched = []
        if self.specific_file == '':
            for f in file_helper.get_next_file(self.caller_dir, self.is_recursive):
                matched_file = self.search_wrapper(f)

                if matched_file:
                    self.printing(matched_file)
                    all_matched.extend(matched_file)

        else:
            matched_file = self.search_wrapper(self.specific_file)

            if matched_file:
                self.printing(matched_file)
                all_matched.extend(matched_file)

        return all_matched

    def printing(self, matched_file):
        """Prints a matched file or line."""

        if self.is_abs_path:
            print_helper.generate_output_for_matched_files_full_path(matched_file, self.search_term, self.is_from_stdin)

        else:
            print_helper.generate_output_for_matched_files_relative_path(matched_file, self.search_term, self.is_from_stdin)

    def search_wrapper(self, file_path):
        """Wraps search_f to accommodate for errors."""

        matched_file = {}
        try:
            matched_file = self.search_f(file_path)
        except IOError, ioerror:
            print "Error while reading file:\n\t%s" % ioerror

        return matched_file

    def search_f(self, file_path):
        """Decides which type of search should be executed."""

        assert type(file_path) == str

        matched_line_dict = {}
        if self.is_search_line_by_line:
            if self.is_regex_pattern:
                try:
                    matched_line_dict = self.search_line_by_line_for_regex(file_path)

                except sre_constants.error, error:
                    print "Regex expression error:\n\t%s" % error

            else:
                matched_line_dict = self.search_line_by_line_for_term(file_path)

        else:
            if self.is_regex_pattern:
                try:
                    matched_line_dict = self.match_f_for_pattern(file_path)

                except sre_constants.error, error:
                    print "Regex expression error:\n\t%s" % error

            else:
                matched_line_dict = self.match_f_for_str(file_path)

        if matched_line_dict:
            return {file_path: matched_line_dict}
        else:
            return None

    def match_f_for_str(self, file_path):
        """Search a file for the occurrence of a string."""

        assert type(file_path) == str

        with open(file_path, 'r') as f:
            f.seek(0)
            entire_file = ""
            for line in f.readlines():
                entire_file += line

            matched = {}
            if self.search_term == '':
                return {'file': entire_file}

            if self.search_term in entire_file:
                # Do not include matches if file is binary
                if file_helper.is_binary_file(file_path):
                    return {'file_matched': ''}

                split_str = entire_file.split(self.search_term)
                shortened_file = (split_str[0][len(split_str[0]) - len(self.search_term) * 15:] + self.search_term
                                  + split_str[1][:-(len(split_str[1]) - len(self.search_term) * 15)]).strip()

                # assert len(shortened_file) != len(entire_file.strip())
                matched['file'] = shortened_file

            return matched

    def match_f_for_pattern(self, file_path):
        """Search a file for a pattern."""

        assert type(file_path) == str

        with open(file_path, 'r') as f:
            f.seek(0)
            entire_file = ""
            for line in f.readlines():
                entire_file += line

            regexp = re.compile(self.search_term)
            matches = regexp.findall(entire_file)
            matched = {}

            if self.search_term == '':
                return {'file': entire_file}

            if len(matches) >= 1:
                # Do not include matches if file is binary
                if file_helper.is_binary_file(file_path):
                    return {'file_matched': ''}

                f.seek(0)
                entire_file = ""
                for line in f.readlines():
                    entire_file += line

                shortened_file = ""
                for match in matches:
                    split_str = entire_file.split(match)
                    shortened_file = (split_str[0][len(split_str[0]) - len(self.search_term) * 15:]
                                      + self.search_term + split_str[1][:-(len(split_str[1]) - len(self.search_term) * 15)]).strip()

                # assert len(shortened_file) != len(entire_file.strip())

                matched['file'] = shortened_file

            return matched

    def search_line_by_line_for_term(self, file_path):
        """Search a single file for occurrences of a string; each line is searched separately."""

        assert type(file_path) == str

        matched_lines = {}
        with open(file_path, 'r') as f:
            for line_num, line in enumerate(f):

                if self.search_term == '':
                    matched_lines[line_num + 1] = line.strip()

                elif self.search_term in line:
                    # Do not include matches if file is binary
                    if file_helper.is_binary_file(file_path):
                        return {'file_matched': ''}

                    split_str = line.split(self.search_term)
                    matched_lines[line_num + 1] = (split_str[0] + self.search_term + split_str[1][:-len(
                        split_str[1]) + len(split_str[0] + self.search_term)]).strip()

        return matched_lines

    def search_line_by_line_for_regex(self, file_path):
        """Search a single file using a regex pattern; each line is searched separately."""

        assert type(file_path) == str

        regexp = re.compile(self.search_term)
        matched_lines = {}

        with open(file_path, 'r') as f:
            for line_num, line in enumerate(f):

                if self.search_term == '':
                    matched_lines[line_num + 1] = line.strip()

                match = regexp.findall(line)
                if match:
                    # Do not include matches if file is binary
                    if file_helper.is_binary_file(file_path):
                        return {'file_matched': ''}

                    for row in match:
                        if not row:
                            del row

                    try:
                        split_str = line.split(match[0])
                        matched_lines[line_num + 1] = (split_str[0] + match[0] + split_str[1][:-len(split_str[1]) + len(
                            split_str[0] + match[0])]).strip()

                    # Catch empty separator
                    except ValueError:
                        matched_lines[line_num + 1] = line.strip()

        return matched_lines
