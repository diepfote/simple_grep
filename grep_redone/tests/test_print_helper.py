import os
import tempfile
import platform
import pytest

from grep_redone.grep import print_helper
from grep_redone.tests.helper_for_tests import with_f_bwrite, with_f_write


def test_print_matched_files_full_path():
    test_dict = {'/home/flo/Untitled Document': {1: 'aware\n', 2: 'aware werwer\n'}}

    test_output = ['\x1b[35m\x1b[22m' + os.path.normpath('/home/flo/Untitled Document') + ':\x1b[39m\x1b[22m2:\x1b[1;31maware\x1b[0m werwer', '\x1b[35m\x1b[22m' + os.path.normpath('/home/flo/Untitled Document') + ':\x1b[39m\x1b[22m1:\x1b[1;31maware\x1b[0m']
    output = print_helper.print_matched_files_full_path(test_dict, search_term='aware')

    assert output == test_output


def test_print_matched_files_relative_path():
    if platform.system() == 'Windows':
        test_dict = {'./../../../../Untitled Document': {1: 'aware\n', 2: 'aware werwer\n'}}

    elif platform.system() == 'Linux':
        test_dict = {'/home/flo/Untitled Document': {1: 'aware\n', 2: 'aware werwer\n'}}

    else:
        raise ValueError('No system information found.')

    test_output = ['\x1b[35m\x1b[22m' + os.path.normpath('../../../../Untitled Document') + ':\x1b[39m\x1b[22m2:\x1b[1;31maware\x1b[0m werwer', '\x1b[35m\x1b[22m' + os.path.normpath('../../../../Untitled Document') + ':\x1b[39m\x1b[22m1:\x1b[1;31maware\x1b[0m']
    output = print_helper.print_matched_files_relative_path(test_dict, search_term='aware')

    assert output == test_output


def test_rreplace():

    original_string = "12234545235323"
    test_string = "1223454523533"
    string_to_test_against = print_helper.rreplace(original_string, '2', '', 1)

    assert test_string == string_to_test_against


def test_color_string():
    test_list = ['Thebrownfoxjumpsover.']
    term = 'fox'
    # FYI \33 gets turned into \x1b
    test_output = ['Thebrown\033[1;31mfox\033[0mjumpsover.']

    output = print_helper.color_string(list_to_edit=test_list, term=term, color='red')

    assert output == test_output
