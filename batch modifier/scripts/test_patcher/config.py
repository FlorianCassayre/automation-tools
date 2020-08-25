# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2020 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Script configuration."""

def should_apply_changes(repository):
    """Configure what repository should take the changes."""
    return repository in ['invenio-db']

# Modifcations
replacements = {
    'python setup.py test': 'python -m pytest',
    'python setup.py test && \\': 'python -m pytest && \\',
    'python setup.py test # && \\': 'python -m pytest # && \\',
}

run_tests_sh = 'run-tests.sh'
setup_cfg = 'setup.cfg'
setup_py = 'setup.py'


# Github config
open_pr = False

branch = "pytest_modifs"

base = "master"

message = "tests: bypass setuptools and use pytest"
title = message
body = "Modification of the repository to use pytest instead of setuptools"

expected = [
        'M run-tests.sh',
        'M setup.cfg'
        ]