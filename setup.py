from setuptools import setup, find_packages
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

about = {}
with open(path.join(this_directory, 'webvis', '__about__.py'), encoding='utf-8') as f:
    exec(f.read(), about)

setup(
    name = 'webvis',
    packages = find_packages(),
    version = about['__version__'],
    author = about['__author__'],
    author_email = 'lkvdan@gmail.com',
    url = 'https://github.com/DaniloZZZ/pywebviz',
    description = 'A live two-way data binder for python',
    long_description=long_description,
    long_description_content_type='text/markdown',

    install_requires=['legimens', 'matplotlib', 'numpy', 'requests',
                      'mpld3','trio','trio-websocket'],
    python_requires='>=3.3',
    include_package_data=True,
    license='MIT',
    keywords = ['tools', 'data', 'framework', 'visualization'], 
    classifiers = [],
)
