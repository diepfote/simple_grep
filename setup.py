from setuptools import setup

setup(
    name='Grep Redone',
    version='0.9',
    packages=['grep'],
    install_requires=['clint',
                      'docopt'],
    entry_points={
        'console_scripts': [
            'grep_redone=grep.__main__:main']
    },
)
