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
from os import path

from automation_tools import config
from automation_tools.config import github
from automation_tools.utils import execute


def list_invenio_modules():
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
        pygit2.clone_repository(f"{url_github}/{repository_name}", f"{local_repositories_path}/{repository_name}")


def cd_repository(repository):
    os.chdir(config.local_repositories_path + os.path.sep + repository)


def check_status(repository, expected):
    """Check if modifications are the ones expected."""
    cd_repository(repository)
    outputs = []
    for out in execute(["git", "status", "-s"]):
        outputs.append(out.strip())

    if outputs == expected:
        modifs_ok = True

    else:
        modifs_ok = False

    return modifs_ok


def commit(repository, message, extra_before=None, extra_after=None):
    """Commit if changes."""
    cd_repository(repository)
    try:
        subprocess.check_output(["git", "add", "."])
        commit = ["git"]
        if extra_before:
            commit.extend(extra_before)
        commit.extend(["commit", "-m", message])
        if extra_after:
            commit.extend(extra_after)
        subprocess.check_output(commit)
        commited = True
    except:
        commited = False

    return commited


def push(repository, destination, local_branch, remote_branch, force=False):
    """Push commited changes."""
    cd_repository(repository)
    try:
        push = ["git", "push", destination, local_branch + ':' + remote_branch]
        if force:
            push.extend(['--force'])
        subprocess.check_output(push)
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


def github_process(is_mode_pr, expected, repository, local_branch, remote_branch, message, title, body, base,
                   commit_extra_before, commit_extra_after):
    """."""
    # TODO: raise Exception
    modifs_ok = check_status(repository, expected)
    if modifs_ok:
        print("Has to be committed")
        committed = commit(repository, message, commit_extra_before, commit_extra_after)
        if committed:
            print("Has been committed")
            pushed = push(repository, config.destination, local_branch, remote_branch)
            if not pushed:
                raise Exception("Failed to push")

            if pushed and is_mode_pr:
                print("Has been pushed")
                gh_repository = github.get_repo(f"{config.organization}/{repository}")
                pr_opened = open_pr(gh_repository, title, body, remote_branch, base)
                if pr_opened:
                    print("PR has been opened")
                else:
                    raise Exception("PR has not been opened")
        else:
            raise Exception("Failed to commit")

    else:
        raise Exception("Please review modifications")


def create_organization_repository(repository):
    org = config.github.get_organization(config.organization)
    org.create_repo(repository)


def set_origin(repository, new_origin_url):
    os.chdir(config.local_repositories_path + os.path.sep + repository)
    execute(["git", "remote", "set-url", config.destination, new_origin_url])
