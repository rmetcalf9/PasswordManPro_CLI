# -*- coding: utf-8 -*-

"""
    passwordmanpro_cli
    ~~~~~~~~
    Python package which provides a base application class for an app with a restapi backend that provides a swagger
    :copyright: (c) 2018 by Robert Metcalf.
    :license: MIT, see LICENSE for more details.
"""

from .AppObj import AppObjClass

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions