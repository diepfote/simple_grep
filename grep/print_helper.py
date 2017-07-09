"""Print matched items for grep.py."""

import os
import sys
from clint.textui import colored

from . import file_helper


def generate_output_for_matched_files_full_path(matched_files_and_lines, search_term, is_from_stdin, is_line_by_line):
	"""Prints matching files using absolute paths."""

	assert type(matched_files_and_lines) == dict
	assert type(search_term) == str
	assert type(is_from_stdin) == bool

	output = []
	# Py2
	if sys.version_info[0] < 3:
		for f, lines in matched_files_and_lines.iteritems():
			if file_helper.is_binary_file(f):
				output.extend(['Binary file ' + f + ' matches'])

			else:
				if is_from_stdin:
					output.extend([line for line_num, line in lines.iteritems()])

				elif not is_line_by_line:
					output.extend([(colored.magenta(os.path.normpath(f)) + colored.green(':') + line)
					               for line_num, line in lines.iteritems()])

				else:
					output.extend([(colored.magenta(os.path.normpath(f)) + colored.green(':')
					                + colored.green(str(line_num)) + colored.green(':') + line)
					               for line_num, line in lines.iteritems()])

	# Py3
	else:
		for f, lines in matched_files_and_lines.items():
			if file_helper.is_binary_file(f):
				output.extend(['Binary file ' + f + ' matches'])

			else:
				if is_from_stdin:
					output.extend([line for line_num, line in lines.items()])

				elif not is_line_by_line:
					output.extend([(colored.magenta(os.path.normpath(f)) + colored.green(':') + line)
					               for line_num, line in lines.items()])

				else:
					output.extend([(colored.magenta(os.path.normpath(f)) + colored.green(':')
					                + colored.green(str(line_num)) + colored.green(':') + line)
					               for line_num, line in lines.items()])

	# Remove last occurrence of new line
	output = [''.join(f.rsplit('\n', 1)) for f in output]

	# Color and print term
	for line in color_matched_items(output, search_term):
		print (line)

	# TODO make test appropriate
	return output


def generate_output_for_matched_files_relative_path(matched_files_and_lines, search_term, is_from_stdin,
                                                    is_line_by_line):
	"""Prints matching files using relative paths."""

	assert type(matched_files_and_lines) == dict
	assert type(search_term) == str
	assert type(is_from_stdin) == bool

	output = []
	# Py2
	if sys.version_info[0] < 3:
		for f, lines in matched_files_and_lines.iteritems():
			if file_helper.is_binary_file(f):
				output.extend(['Binary file ' + f + ' matches'])

			else:
				if is_from_stdin:
					output.extend([line for line_num, line in lines.iteritems()])

				elif not is_line_by_line:
					output.extend([(colored.magenta(os.path.normpath(os.path.relpath(f))) + colored.blue(':') + line)
					               for line_num, line in lines.iteritems()])

				else:
					output.extend([(colored.magenta(os.path.normpath(os.path.relpath(f))) + colored.blue(':')
					                + colored.green(str(line_num)) + colored.blue(':') + line)
					               for line_num, line in lines.iteritems()])

	# Py3
	else:
		for f, lines in matched_files_and_lines.items():
			if file_helper.is_binary_file(f):
				output.extend(['Binary file ' + f + ' matches'])

			else:
				if is_from_stdin:
					output.extend([line for line_num, line in lines.items()])

				elif not is_line_by_line:
					output.extend([(colored.magenta(os.path.normpath(os.path.relpath(f))) + colored.blue(':') + line)
					               for line_num, line in lines.items()])

				else:
					output.extend([(colored.magenta(os.path.normpath(os.path.relpath(f))) + colored.blue(':')
					                + colored.green(str(line_num)) + colored.blue(':') + line)
					               for line_num, line in lines.items()])

	# Remove last occurrence of new line
	output = [''.join(f.rsplit('\n', 1)) for f in output]

	# Color and print term
	for line in color_matched_items(output, search_term):
		print (line)

	# TODO make test appropriate
	return output


def color_term_in_string(func):
	"""Colors the last occurrence of a term in a string."""


	def func_wrapper(list_to_edit, term):
		assert type(list_to_edit) == list
		assert type(term) == str

		lightish_red = '\033[1;31m'
		no_color = '\033[0m'

		if term:
			# Don't color output if output is 'Binary file x matches'
			if list_to_edit[0].startswith("Binary file"):
				return list_to_edit

			return [(lightish_red + term + no_color).join(f.rsplit(term, 1)) for f in func(list_to_edit, term)]

		else:
			return list_to_edit


	return func_wrapper


@color_term_in_string
def color_matched_items(output, search_term):
	return output
