from setuptools import setup, find_packages
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

about = {}
with open(path.join(this_directory, 'libvis', '__about__.py'), encoding='utf-8') as f:
    exec(f.read(), about)

setup(
    name = 'libvis',
    packages = find_packages(),
    version = about['__version__'],
    author = about['__author__'],
    author_email = 'lkvdan@gmail.com',
    url = 'https://github.com/libvis/python-libvis',
    description = 'Interactive live object visualization for python',
    long_description=long_description,
    long_description_content_type='text/markdown',

    install_requires=['legimens', 'matplotlib', 'numpy', 'requests',
                      'trio>=0.13','trio-websocket>=0.8'],
    python_requires='>=3.3',

    # On github actions, MANIFEST.in is not enough to include these. Why?
    # Why does python setup.py not respect MANIFEST.in? 
    # Even `include_package_data` does not help.
    # This one fixes the issue.
    data_files=[
        'libvis/front_build/index.html',
        'libvis/front_build/index.bundle.js'
    ],
    include_package_data=True,
    license='GPLv2',
    keywords = ['tools', 'data', 'framework', 'visualization'],
    classifiers = [],
)
