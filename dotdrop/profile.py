"""
author: deadc0de6 (https://github.com/deadc0de6)
Copyright (c) 2019, deadc0de6

represent a profile in dotdrop
"""

from typing import Any, Dict, List, Optional

from dotdrop.dictparser import DictParser
from dotdrop.action import Action

__all__ = ['Profile']


class Profile(DictParser):
    """dotdrop profile"""

    # profile keys
    key_include = 'include'
    key_import = 'import'

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(self, key: str,
                 actions: Optional[List[Action]] = None,
                 dotfiles: Optional[List[str]] = None,
                 variables: Optional[List[str]] = None,
                 dynvariables: Optional[List[str]] = None) -> None:
        """
        constructor
        @key: profile key
        @actions: list of action keys
        @dotfiles: list of dotfile keys
        @variables: list of variable keys
        @dynvariables: list of interpreted variable keys
        """
        self.key = key
        self.actions = actions or []
        self.dotfiles = dotfiles or []
        self.variables = variables or []
        self.dynvariables = dynvariables or []

    def get_pre_actions(self) -> List[Action]:
        """return all 'pre' actions"""
        return [a for a in self.actions if a.kind == Action.pre]

    def get_post_actions(self) -> List[Action]:
        """return all 'post' actions"""
        return [a for a in self.actions if a.kind == Action.post]

    @classmethod
    def _adjust_yaml_keys(cls, value: Dict[str, Any]) -> Dict[str, Any]:
        """patch dict"""
        value.pop(cls.key_import, None)
        value.pop(cls.key_include, None)
        return value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Profile):
            return False
        return self.__dict__ == other.__dict__

    def __hash__(self) -> int:
        return (hash(self.key) ^
                hash(tuple(self.dotfiles)))

    def __str__(self) -> str:
        return f'key:"{self.key}"'

    def __repr__(self) -> str:
        return f'profile({self})'
