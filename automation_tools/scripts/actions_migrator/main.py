# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2020 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import re

import automation_tools.scripts.actions_migrator.config as script_config
from automation_tools.utils import (file_path, index_of,
                                    list_local_repository_names, read_content,
                                    split_lines)


def content_pypy_release_yml(python_version='3.7'):
    return f"""
on:
  push:
    tags:
      - v*

jobs:
  build-n-publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python ${python_version}
        uses: actions/setup-python@v2
        with:
          python-version: ${python_version}
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install setuptools wheel
      - name: Build package
        run: |
          python setup.py compile_catalog sdist bdist_wheel
      - name: pypi-publish
        uses: pypa/gh-action-pypi-publish@v1.3.1
        with:
          user: __token__
          password: ${{ secrets.pypi_password }}
          """.strip()


def main():
    not_patchable = {}
    patchable = []

    for repository in list_local_repository_names():
        content_travis = read_content(file_path(repository, '.travis.yml'))
        if content_travis:
            lines_travis = split_lines(content_travis)
            if 'deploy:' in lines_travis:
                content_manifest = read_content(file_path(repository, 'MANIFEST.in'))
                if content_manifest:
                    index = index_of('python:', lines_travis)
                    if index:
                        versions = 0
                        while lines_travis[index + 1 + versions].startswith('  - ') or lines_travis[index + 1 + versions].startswith('   - '):
                            versions += 1
                        if script_config.python_version_detect:
                            if script_config.python_version_lowest:
                                version_line = lines_travis[index + 1]
                            else:
                                version_line = lines_travis[index + versions]
                            match = re.match(' +- "(\\d\\.\\d)"', version_line)
                            if match:
                                version = match.group(1)
                            else:
                                version = None
                        else:
                            version = script_config.python_version

                        if version:
                            patchable.append(repository)
                        else:
                            not_patchable[repository] = 'Unrecognized python version'
                    else:
                        not_patchable[repository] = 'No python version detected'

                else:
                    not_patchable[repository] = 'No file `MANIFEST.in`'
            else:
                if any('- stage: deploy' in line for line in lines_travis):
                    not_patchable[repository] = 'Unsupported deployment scheme'
                else:
                    not_patchable[repository] = 'No deploy line'
        else:
            not_patchable[repository] = 'No file `.travis.yml`'

    print(len(patchable))
    for k in not_patchable:
        print(k + ': ' + not_patchable[k])

    #  DEPLOY=true


if __name__ == "__main__":
    main()
