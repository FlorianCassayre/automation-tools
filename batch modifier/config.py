# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2020 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Contains the settings to repository modifications."""

from github import Github

organization = "invenio-toaster"
destination = "origin"

# Directory path to hold a copy of the repositories
local_repositories_path = 'Invenio clones'

# Github credentials / token
github_token = 'c5bd60144cc355327fd519bdb21124341a6abc5a'
github = Github(github_token)
