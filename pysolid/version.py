#!/usr/bin/env python3
# Author: Zhang Yunjun, Jan 2021
# Copyright 2020, by the California Institute of Technology.


import collections

# release history
Tag = collections.namedtuple('Tag', 'version date')
release_history = (
    Tag('0.1.0', '2021-01-22'),
    Tag('0.1.1', '2021-02-01'),
    Tag('0.1.2', '2021-02-24'),
)

# latest release
release_version = 'v{}'.format(release_history[-1].version)
release_date = release_history[-1].date
