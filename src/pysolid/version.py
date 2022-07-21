#!/usr/bin/env python3
# Author: Zhang Yunjun, Jan 2021
# Copyright 2020, by the California Institute of Technology.


import collections

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
release_version = 'v{}'.format(release_history[0].version)
release_date = release_history[0].date
