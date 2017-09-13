from setuptools import setup

setup(
    name='Simple Grep',
    version='1.11',
    packages=['grep'],
    entry_points={
        'console_scripts': [
            'simple_grep=grep.__main__:main']
    },
)

