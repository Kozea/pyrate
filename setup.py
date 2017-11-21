#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from setuptools import find_packages, setup

# Private
if 'register' in sys.argv or 'upload' in sys.argv:
    print('Private package')
    sys.exit(1)

__version__ = "0.0.1"

tests_requirements = [
    'pytest-runner == 2.12.1',
    'pytest-cov == 2.5.1',
    'pytest-flake8 == 0.9.0',
    'pytest-isort == 0.1.0',
    'pytest == 3.2.3'
]  # yapf: disable

setup(
    name="pyrate__private",
    version=__version__,
    description="...",
    author="Kozea",
    author_email="florian.mounier@kozea.fr",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'alembic == 0.9.6',
        'bcrypt == 3.1.4',
        'cffi == 1.11.2',
        'click == 6.7',
        'ddt == 1.1.1',
        'Flask == 0.12.2',
        'Flask-Bcrypt == 0.7.1',
        'Flask-Migrate == 2.1.1',
        'Flask-Script == 2.0.5',
        'Flask-SQLAlchemy == 2.3.2',
        'Flask-Testing == 0.6.2',
        'itsdangerous == 0.24',
        'Jinja2 == 2.10',
        'Mako == 1.0.7',
        'markovify == 0.6.4'
        'MarkupSafe == 1.0',
        'pycparser == 2.18',
        'PyJWT == 1.5.3',
        'python-dateutil == 2.6.1',
        'python-editor == 1.0.3',
        'six == 1.11.0',
        'SQLAlchemy == 1.1.15',
        'Werkzeug == 0.12.2',
    ],
    provides=["pyrate__private"],
    setup_requires=['pytest-runner'],
    test_requires=tests_requirements,
    extras_require={'test': tests_requirements}
)  # yapf: disable
