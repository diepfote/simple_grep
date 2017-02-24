import os
import print_helper


class Searcher(object):
    """Searches files in dirs for specified string."""

    isfirst = True

    def __init__(self, caller_dir, string_to_search_for, is_recursive):
        self.caller_dir = caller_dir
        self.string_to_search_for = string_to_search_for

        matched_files = self.search_files(self.get_all_files(is_recursive))

        print_helper.print_matched_files_full_path(matched_files)

    def get_all_files(self, is_recursive):
        full_file_paths = []
        index = 0

        for root, dirs, files in os.walk(self.caller_dir):

            # Prepend root to every file path
            full_file_paths.extend(['{0}/{1}'.format(root, file) for file in files])

            if is_recursive is False:
                break

        return full_file_paths

    def search_files(self, file_list):
        matched_files = {}

        for f in file_list:
            matched_line_dict = self.search_file_for_string(f)

            if matched_line_dict:
                matched_files[f] = matched_line_dict

        return matched_files

    def search_file_for_string(self, file_path):
        """Search a single file for occurrences of a string."""

        matched_lines = {}
        if not os.path.isdir(file_path):
            with open(file_path, 'r') as f:
                for index, line in enumerate(f):
                    if self.string_to_search_for in line:
                        matched_lines[index + 1] = line

        return matched_lines
