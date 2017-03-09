import os
import tempfile
import platform
import pytest

from grep_redone.grep import print_helper
from grep_redone.tests.helper_for_tests import with_f_bwrite, with_f_write


def test_generate_output_for_matched_files_full_path():
    test_dict = {'/home/flo/Untitled Document': {1: 'aware\n', 2: 'aware werwer\n'}}

    test_output = [os.path.normpath('/home/flo/Untitled Document') + ':1:aware',
                   os.path.normpath('/home/flo/Untitled Document') + ':2:aware werwer']
    output = print_helper.generate_output_for_matched_files_full_path(test_dict, search_term='aware')

    assert output == test_output


def test_generate_output_for_matched_files_relative_path():
    if platform.system() == 'Windows':
        test_dict = {'./../../../../Untitled Document': {1: 'aware\n', 2: 'aware werwer\n'}}

    elif platform.system() == 'Linux':
        test_dict = {'/home/flo/Untitled Document': {1: 'aware\n', 2: 'aware werwer\n'}}

    else:
        raise ValueError('No system information found.')

    test_output = [os.path.normpath('../../../../Untitled Document') + ':1:aware',
                   os.path.normpath('../../../../Untitled Document') + ':2:aware werwer']
    output = print_helper.generate_output_for_matched_files_relative_path(test_dict, search_term='aware')

    try:
        assert output == test_output
    except AssertionError:
        pytest.fail(test_output)

def test_color_term_in_string():
    test_list = ['Thebrownfoxjumpsover.']
    term = 'fox'
    # FYI \33 gets turned into \x1b
    test_output = ['Thebrown\033[1;31mfox\033[0mjumpsover.']

    output = function_for_color_term_in_string(test_list, term)

    assert output == test_output

@print_helper.color_term_in_string
def function_for_color_term_in_string(l, term):
    return l