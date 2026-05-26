"""
author: deadc0de6 (https://github.com/deadc0de6)
Copyright (c) 2020, deadc0de6

represents a type of link in dotdrop
"""

# https://github.com/PyCQA/pylint/issues/2062
# pylint: disable=E1101

from enum import IntEnum
from typing import Optional, Union

__all__ = ['LinkTypes']


class LinkTypes(IntEnum):
    """A type of link."""

    NOLINK = 0
    LINK = 1
    LINK_CHILDREN = 2
    ABSOLUTE = 3
    RELATIVE = 4

    @classmethod
    def get(cls, key: Union['LinkTypes', str],
            default: Optional['LinkTypes'] = None) -> 'LinkTypes':
        """Return a LinkTypes from a string or instance."""
        try:
            return key if isinstance(key, cls) else cls[key.upper()]
        except KeyError as exc:
            if default and isinstance(default, cls):
                return default
            err = f'bad {cls.__name__} value: "{key}"'
            raise ValueError(err) from exc

    def __str__(self) -> str:
        """Return the lowercase name."""
        return self.name.lower()
