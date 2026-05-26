"""
author: deadc0de6 (https://github.com/deadc0de6)
Copyright (c) 2018, deadc0de6

jinja2 helper methods
"""

import os
import shutil
from typing import Optional

__all__ = ['exists', 'exists_in_path', 'basename', 'dirname']


def exists(path: str) -> bool:
    """return true when path exists"""
    return os.path.exists(os.path.expandvars(path))


def exists_in_path(name: str, path: Optional[str] = None) -> bool:
    """return true when executable exists in os path"""
    return shutil.which(name, os.F_OK | os.X_OK, path) is not None


def basename(path: str) -> str:
    """return basename"""
    return os.path.basename(path)


def dirname(path: str) -> str:
    """return dirname"""
    return os.path.dirname(path)
