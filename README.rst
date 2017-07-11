Simple grep
^^^^^^^^^^^

Simple grep is a minimal implementation of grep. It is entirely written in Python.

Most notable alteration: No file or directory specified implies searching in current directory.
Missing features: stdin support for Windows.

Simple grep is tested on:
* CPython 2.7 and 3.6.

(Some tests might fail on Windows)


Running it
----------

.. code-block:: bash

    $ python -m grep.__main__ -h


Installation
------------

On any system:

.. code-block:: bash

    $ pip install .


On Arch:

.. code-block:: bash

    $ makepkg

    $ sudo pacman -U simple_grep-1-1-x86_64.pkg.tar.xz

