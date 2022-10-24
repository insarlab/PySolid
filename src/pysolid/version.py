#!/usr/bin/env python3
# Author: Zhang Yunjun, Jan 2021
# Copyright 2020, by the California Institute of Technology.


import collections
import os
import subprocess


###########################################################################
# release history
Tag = collections.namedtuple('Tag', 'version date')
release_history = (
    Tag('0.2.2', '2022-07-20'),
    Tag('0.2.1', '2022-01-05'),
    Tag('0.2.0', '2021-11-10'),
    Tag('0.1.2', '2021-02-24'),
    Tag('0.1.1', '2021-02-01'),
    Tag('0.1.0', '2021-01-22'),
)

# latest release
release_version = release_history[0].version
release_date = release_history[0].date

# get development version info
def get_version_info():
    """Grab version and date of the latest commit from a git repository"""
    # go to the repository directory
    dir_orig = os.getcwd()
    os.chdir(os.path.dirname(os.path.dirname(__file__)))

    try:
        # grab from git cmd
        cmd = "git describe --tags"
        version = subprocess.check_output(cmd.split(), stderr=subprocess.DEVNULL)
        version = version.decode('utf-8').strip()[1:]

        # if there are new commits after the latest release
        if '-' in version:
            version, num_commit = version.split('-')[:2]
            version += f'-{num_commit}'

        cmd = "git log -1 --date=short --format=%cd"
        date = subprocess.check_output(cmd.split(), stderr=subprocess.DEVNULL)
        date = date.decode('utf-8').strip()

    except:
        # use the latest release version/date
        version = release_version
        date = release_date

    # go back to the original directory
    os.chdir(dir_orig)
    return version, date


###########################################################################
version, version_date = get_version_info()

