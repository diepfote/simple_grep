import os
import tempfile

from grep_redone.grep import file_helper
from grep_redone.tests.helper_for_tests import with_f_bwrite, with_f_write


def test_get_all_files():
    temp_dir = tempfile.mkdtemp()
    temp = tempfile.NamedTemporaryFile(dir=temp_dir)

    try:
        files = file_helper.get_all_files(temp_dir, is_recursive=False)
        assert files == [temp.name]

    finally:
        temp.close()
        os.removedirs(temp_dir)


def test_is_f_binary_file_with_binary_file(with_f_bwrite):
    with_f_bwrite.flush()
    with_f_bwrite.write(b'\x07\x08\x07')
    with_f_bwrite.seek(0)
    with_f_bwrite.close()

    try:
        with_f_bwrite = open(with_f_bwrite.name , 'rb')
        test_result = True
        result = file_helper.is_f_binary_file(with_f_bwrite.name)

        assert result == test_result
    finally:
        with_f_bwrite.close()


def test_is_f_binary_file_with_text_file(with_f_write):
    with_f_write.flush()
    with_f_write.write('asdadsf')
    with_f_write.seek(0)
    with_f_write.close()

    try:
        with_f_write = open(with_f_write.name, 'r')
        test_result = False
        result = file_helper.is_f_binary_file(with_f_write.name)

        assert result == test_result

    finally:
        with_f_write.close()
