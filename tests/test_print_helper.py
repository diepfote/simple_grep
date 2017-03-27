import os
import tempfile
import platform
import pytest

from grep import print_helper
from tests.helper_for_tests import with_f_bwrite, hotfix_delete_temp_dir


def test_generate_output_for_matched_files_full_path():
    matched_items = {'/home/flo/Untitled Document': {1: 'aware\n', 2: 'aware werwer\n'}}

    test_output = [os.path.normpath('/home/flo/Untitled Document') + ':1:aware',
                   os.path.normpath('/home/flo/Untitled Document') + ':2:aware werwer']
    output = print_helper.generate_output_for_matched_files_full_path(matched_items, search_term='aware')

    assert output == test_output


def test_generate_output_for_matched_files_relative_path():
    if platform.system() == 'Windows':
        matched_items = {'./../../../../Untitled Document': {1: 'aware\n', 2: 'aware werwer\n'}}

    elif platform.system() == 'Linux':
        matched_items = {'/home/flo/Untitled Document': {1: 'aware\n', 2: 'aware werwer\n'}}

    else:
        raise ValueError('No system information found.')

    test_output = [os.path.normpath('../../../../Untitled Document') + ':1:aware',
                   os.path.normpath('../../../../Untitled Document') + ':2:aware werwer']
    output = print_helper.generate_output_for_matched_files_relative_path(matched_items, search_term='aware')

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


def test_outptut_binary_file_matches_full_path(with_f_bwrite):
    matched_items = {with_f_bwrite.name: {'file_matched': ''}}
    with_f_bwrite.write(b'\x00')
    with_f_bwrite.seek(0)

    test_output = ['Binary file ' + with_f_bwrite.name + ' matches']
    output = print_helper.generate_output_for_matched_files_full_path(matched_items, search_term='aware')

    assert output == test_output


def test_outptut_binary_file_matches_relative_path(with_f_bwrite):
    matched_items = {with_f_bwrite.name: {'file_matched': ''}}
    with_f_bwrite.write(b'\x00')
    with_f_bwrite.seek(0)

    test_output = ['Binary file ' + with_f_bwrite.name + ' matches']
    output = print_helper.generate_output_for_matched_files_relative_path(matched_items, search_term='aware')

    assert output == test_output


# TODO FIX calling hotfix_delete_temp_dir manually
def test_hotfix_delete_temp_dir(hotfix_delete_temp_dir):
    pass
