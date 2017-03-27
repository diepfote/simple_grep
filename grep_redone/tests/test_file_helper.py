import os

from grep_redone.grep import file_helper
from grep_redone.tests.helper_for_tests import with_f_bwrite, with_f_write, temp_path


def test_get_next_f():
    caller_dir = os.path.dirname(temp_path)
    f = file_helper.get_next_file(caller_dir, is_recursive=False).next()

    assert f == temp_path


def test_is_binary_file_with_binary_file(with_f_bwrite):
    with_f_bwrite.write(b'\x07\x08\x07')
    with_f_bwrite.seek(0)

    test_result = True
    result = file_helper.is_binary_file(with_f_bwrite.name)

    assert result == test_result


def test_is_binary_file_with_text_file(with_f_write):
    with_f_write.write('asdadsf')
    with_f_write.seek(0)

    test_result = False
    result = file_helper.is_binary_file(with_f_write.name)

    assert result == test_result


def test_is_binary_file_null_bytes(with_f_bwrite):
    with_f_bwrite.write(b'\x00')
    with_f_bwrite.seek(0)

    test_result = True
    result = file_helper.is_binary_file(with_f_bwrite.name)

    assert result == test_result


def test_is_binary_file_empty_file(with_f_write):
    with_f_write.flush()

    test_result = False
    result = file_helper.is_binary_file(with_f_write.name)

    assert result == test_result
