# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2020 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""GitHub utilities."""

import os
import shutil
import subprocess
import sys

import pygit2
from config import local_repositories_path, organization, github
from os import path


def list_invenio_modules(github):
    """List invenio modules by parsing inveniosoftware organization
     - https://github.com/inveniosoftware.
    """
    username = 'inveniosoftware'
    try:
        user = github.get_user(username)
        # invenio_repositories = [repository.name for repository in user.get_repos() \
                        # if repo.name.startswith('invenio-')]
        # invenio_repositories = [repository.name for repository in g.search_repositories(query='language:python')]
        invenio_repositories = github.search_repositories(query='language:python')
        return invenio_repositories

    except:
        print('Failed to process the request')


def download_invenio_modules(repositories, local_repositories_path):
    """Download all the invenio modules in a newly created subfolder."""
    if path.exists(local_repositories_path):
        shutil.rmtree(local_repositories_path)
    os.mkdir(local_repositories_path)
    url_github = "https://github.com/inveniosoftware"
    for repository_name in repositories:
        pygit2.clone_repository(f"{url_github}/{repository_name}", \
            f"{local_repositories_path}/{repository_name}")


def check_status(repository, expected):
    """Check if modifications are the ones expected."""
    os.chdir(repository)
    outputs = []
    for out in execute(["git", "status", "-s"]):
        outputs.append(out.strip())

    if outputs == expected:
        modifs_ok = True

    else:
        modifs_ok = False

    return modifs_ok 


def commit(repo, message):
    """Commit if changes."""
    try:
        subprocess.check_output(["git", "add", "."])
        subprocess.check_output(["git", "commit", "-m", message])
        commited = True
    except:
        commited = False
    
    return commited


def push(destination, branch):
    """Push commited changes."""
    try:
        subprocess.check_output(["git", "push", destination, branch])
        pushed = True
    except:
        pushed = False

    return pushed


def open_pr(gh_repository, title, body, branch, base):
    """Open PR with previous changes"""
    try:
        gh_repository.create_pull(
            title=title,
            body=body,
            head=branch,
            base=base
            )
        pr_opened = True
    except:
        pr_opened = False

    return pr_opened


def github_process(open_pr, expected, repository, branch, message, title, body, base):
    """."""
    # TODO: raise Exception
    modifs_ok = check_status(repository, expected)
    if modifs_ok:
        print("Has to be committed")
        committed = commit(repository, message)
        if committed:
            print("Has been committed")
            pushed = push(destination, branch)
            if pushed and open_pr:
                print("Has been pushed")
                gh_repository = f"{organization}/{repository}"
                pr_opened = open_pr(gh_repository, title, body, branch, base)
                if pr_opened:
                    print("PR has been opened")
                else:
                    raise Exception("PR has not been opened")

            else:
                raise Exception("Failed to push")
        else:
            raise Exception("Failed to commit")

    else:
        raise Exception("Please review modifications")
