import os
import tempfile
import pytest


# TODO FIX
global temp_dir, fd, temp_path
temp_dir = tempfile.mkdtemp()
fd, temp_path = tempfile.mkstemp(dir=temp_dir, suffix='.txt', text=True)


@pytest.fixture(scope='function')
def with_f_read():
    f = open(temp_path, 'r')
    yield f
    f.close()


@pytest.fixture(scope='function')
def with_f_bread():
    f = open(temp_path, 'rb')
    yield f
    f.close()


@pytest.fixture(scope='function')
def with_f_write():
    f = open(temp_path, 'w')
    yield f
    f.close()


@pytest.fixture(scope='function')
def with_f_bwrite():
    f = open(temp_path, 'wb')
    yield f
    f.close()


@pytest.fixture(scope='function')
def with_restricted_file():
    f = open(temp_path, 'r')
    # Leading zero ensures int is treated as octal
    os.chmod(f.name, 0000)
    yield temp_dir

    # Leading zero ensures int is treated as octal
    os.chmod(f.name, 0777)


# TODO FIX
@pytest.fixture(scope='function')
def hotfix_delete_temp_dir(request):
    # Delete directory after tests finished
    def fin():
        os.close(fd)
        os.remove(temp_path)
        os.removedirs(temp_dir)

        # Check that file has been deleted
        with pytest.raises(IOError):
            open(temp_path, 'r')

    # Run fin function after all tests have run
    request.addfinalizer(fin)