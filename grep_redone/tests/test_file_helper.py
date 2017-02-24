import os

from grep_redone.grep import file_helper

def test_get_all_files():
    # TODO make setup
    starting_dir = os.path.abspath(os.curdir)
    os.chdir(os.path.abspath(os.curdir) + "/grep_redone/tests/testing_directory")

    caller_dir = os.path.abspath(os.curdir)
    is_recursive = False
    files = file_helper.get_all_files(caller_dir, is_recursive)

    files = [os.path.relpath(f) for f in files]

    # TODO make teardown
    os.chdir(starting_dir)

    assert files == ['test_file.txt']
