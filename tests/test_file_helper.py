import os

from grep import file_helper
from tests.helper_for_tests import with_f_bwrite, with_f_write, temp_path


def test_get_next_f():
	caller_dir = os.path.dirname(temp_path)
	f = next(file_helper.get_next_file(caller_dir, is_recursive=False))

	assert f == temp_path


def test_is_binary_file_with_binary_file(with_f_bwrite):
	test_result = True
	actual = file_helper.is_binary_file(with_f_bwrite.name)

	assert actual == test_result


def test_is_binary_file_with_text_file(with_f_write):
	with_f_write.write('asdadsf')
	with_f_write.seek(0)

	test_result = False
	actual = file_helper.is_binary_file(with_f_write.name)

	assert actual == test_result


def test_is_binary_file_null_bytes(with_f_bwrite):
	test_result = True
	actual = file_helper.is_binary_file(with_f_bwrite.name)

	assert actual == test_result


def test_is_binary_file_empty_file(with_f_write):
	with_f_write.flush()

	test_result = False
	actual = file_helper.is_binary_file(with_f_write.name)

	assert actual == test_result


def test_null_bytes_file_is_binary(with_f_bwrite):
	name = with_f_bwrite.name
	with_f_bwrite.close()
	f = open(name, 'wb')
	try:
		f.write(b'\x00')
		f.seek(0)

	finally:
		f.close()

	test_result = True
	actual = file_helper.is_binary_file(name)

	assert actual == test_result
