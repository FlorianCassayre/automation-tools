# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2020 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Script configuration."""

workflow_filename = 'pypi_release.yml'

# Choose whether the python release version should automatically detected
python_version_detect = True

python_version = '3.7'  # Manually define the version (only applies if the previous parameter is False)
python_version_lowest = False  # True: selects the lowest version; False: selects the highest version (applies if the parameter is True)

gh_publish_module = 'pypa/gh-action-pypi-publish@v1.3.1'
