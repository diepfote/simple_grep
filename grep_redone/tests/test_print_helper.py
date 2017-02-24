from grep_redone.grep import print_helper

def test_print_matched_files_full_path():
    test_dict = {'/home/flo/Untitled Document 1': {1: 'aware\n', 2: 'aware werwer\n'}}
    test_output = ['\x1b[35m\x1b[22m/home/flo/Untitled Document 1:\x1b[39m\x1b[22m1:\x1b[32m\x1b[22maware\x1b[39m\x1b[22m', '\x1b[35m\x1b[22m/home/flo/Untitled Document 1:\x1b[39m\x1b[22m2:\x1b[32m\x1b[22maware\x1b[39m\x1b[22m werwer']

    output = print_helper.print_matched_files_full_path(test_dict, search_term='aware')

    assert output == test_output

def test_print_matched_files_relative_path():
    test_dict = {'/home/flo/Untitled Document 1': {1: 'aware\n', 2: 'aware werwer\n'}}
    test_output = ['\x1b[35m\x1b[22m./../../../../Untitled Document 1:\x1b[39m\x1b[22m1:\x1b[32m\x1b[22maware\x1b[39m\x1b[22m', '\x1b[35m\x1b[22m./../../../../Untitled Document 1:\x1b[39m\x1b[22m2:\x1b[32m\x1b[22maware\x1b[39m\x1b[22m werwer']

    output = print_helper.print_matched_files_relative_path(test_dict, search_term='aware')

    print output

    assert output == test_output

def test_rreplace():

    original_string = "12234545235323"
    test_string = "1223454523533"
    string_to_test_against = print_helper.rreplace(original_string, '2', '', 1)

    assert test_string == string_to_test_against