from setuptools import setup

setup(
    name='Grep Redone',
    version='0.9',
    packages=['grep'],
    install_requires=['appdirs',
                      'args',
                      'clint',
                      'coverage',
                      'docopt',
                      'packaging',
                      'py',
                      'pyparsing',
                      'pytest',
                      'pytest-cov',
                      'six'],
    entry_points={
        'console_scripts': [
            'grep_redone=grep.__main__:main']
    },
)
