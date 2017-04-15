from setuptools import setup

setup(
    name='Simple Grep',
    version='0.95',
    packages=['grep'],
    install_requires=['clint',
                      'docopt'],
    entry_points={
        'console_scripts': [
            'simple_grep=grep.__main__:main']
    },
)
