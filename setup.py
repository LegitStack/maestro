'''
install project in development mode:
/maestro> python setup.py develop
'''

import os
from setuptools import setup, find_packages  # , findall

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

NAME = 'maestro'
VERSION = '0.0.1'

setup(
    name=NAME,
    version=VERSION,
    namespace_packages=[NAME],
    description='maestro ai - a naive sensorimotor inference engine.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=[f'{NAME}.{p}' for p in find_packages(where=NAME)],
    install_requires=[
    ],
    # python_requires='>=3.5.2',
    # author="",
    # author_email="@wcf.com",
    # url="https://bitbucket.wcf.com/maestro",
    # classifiers=[
    #     "Programming Language :: Python :: 3",
    #     "License :: OSI Approved :: Apache Software License",
    #     "Operating System :: OS Independent",
    # ],
    # scripts=[f for f in findall(dir='pm3/bin') if f.endswith('.py')],

    ## to make it a command line utility uncomment:
    entry_points={
        "console_scripts": [
            "maestro = maestro.bin.workflow:run_workflow",
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
