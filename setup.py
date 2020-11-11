from setuptools import setup, find_packages

setup(
    name='src',
    version='0.0.1',
    packages=find_packages(),
    url='',
    license='MIT',
    author='mohira',
    author_email='mohira@example.com',
    description='',

    install_requires=[
        'Click',
        'psycopg2'
    ],

    entry_points={'console_scripts': ['db=src.cli.main:main']}
)