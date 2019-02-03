'''
install project in development mode:
/maestro> python setup.py develop
'''

import os
from setuptools import setup, find_packages  # , findall

def get_long_description():
    with open("README.md", "r") as fh:
        return fh.read()

def get_name():
    return 'maestro'

def get_version():
    return '0.0.1'

setup(
    name=get_name(),
    version=get_version(),
    namespace_packages=[get_name()],
    description='maestro ai - a naive sensorimotor inference engine, a distributed collaboration framework',
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=[f'{get_name()}.{p}' for p in find_packages(where=get_name())],
    install_requires=[
    ],
    python_requires='>=3.5.2',
    author='Jordan Miller',
    author_email="paradoxlabs@protonmail.com",
    url="https://github.com/LegitStack/maestro",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    # scripts=[f for f in findall(dir='maestro/bin') if f.endswith('.py')],
    entry_points={
        "console_scripts": [
            "maestro = maestro.bin.maestro:main",
        ]
    },
)


def install_pytest_hook():
    '''
    installs a git hook to run tests before commit
    skip tests with: git commit --no-verify -m "commit without testing"
    '''
    if not os.path.exists('.git/hooks'):
        os.makedirs('.git/hooks')

    pytest_hook = '''#!/bin/sh
BRANCH=$(git branch | grep \* | cut -d ' ' -f2)
if [ $BRANCH = "master" ]; then
  echo "Running pre-commit hook pytest tests"
  pytest tests
  if [ $? -ne 0 ]; then
   echo "Tests must pass before commit!"
   exit 1
  fi
fi
'''
    with open('.git/hooks/pre-commit', mode='w') as git_file:
        git_file.write(pytest_hook)


if os.path.exists('.git'):
    install_pytest_hook()
