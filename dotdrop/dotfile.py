"""
author: deadc0de6 (https://github.com/deadc0de6)
Copyright (c) 2017, deadc0de6

represents a dotfile in dotdrop
"""

from typing import Any, Dict, List, Optional, Union

from dotdrop.linktypes import LinkTypes
from dotdrop.dictparser import DictParser
from dotdrop.action import Action, Transform

__all__ = ['Dotfile']


class Dotfile(DictParser):
    """Represent a dotfile."""
    # pylint: disable=too-many-instance-attributes
    # dotfile keys
    key_noempty = 'ignoreempty'
    key_trans_install = 'trans_install'
    key_trans_update = 'trans_update'
    key_template = 'template'

    # pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-locals
    def __init__(self, key: str, dst: str, src: str,
                 actions: Optional[List[Action]] = None,
                 trans_install: Optional[List[Transform]] = None,
                 trans_update: Optional[List[Transform]] = None,
                 link: Union[LinkTypes, str] = LinkTypes.NOLINK,
                 noempty: bool = False,
                 cmpignore: Optional[List[str]] = None,
                 upignore: Optional[List[str]] = None,
                 instignore: Optional[List[str]] = None,
                 template: bool = True,
                 chmod: Optional[Union[int, str]] = None,
                 ignore_missing_in_dotdrop: bool = False) -> None:
        """
        constructor
        @key: dotfile key
        @dst: dotfile dst (in user's home usually)
        @src: dotfile src (in dotpath)
        @actions: dictionary of actions to execute for this dotfile
        @trans_install: transformation to change dotfile before it is installed
        @trans_update: transformation to change dotfile before updating it
        @link: link behavior
        @noempty: ignore empty template if True
        @upignore: patterns to ignore when updating
        @cmpignore: patterns to ignore when comparing
        @instignore: patterns to ignore when installing
        @template: template this dotfile
        @chmod: file permission
        """
        self.actions: List[Action] = actions or []
        self.dst = dst
        self.key = key
        self.link = LinkTypes.get(link)
        self.noempty = noempty
        self.src = src
        self.trans_install: List[Transform] = trans_install or []
        self.trans_update: List[Transform] = trans_update or []
        self.upignore: List[str] = upignore or []
        self.cmpignore: List[str] = cmpignore or []
        self.instignore: List[str] = instignore or []
        self.template = template
        self.chmod = chmod
        self.ignore_missing_in_dotdrop = ignore_missing_in_dotdrop

        if self.link != LinkTypes.NOLINK and \
                (
                    (trans_install and len(trans_install) > 0) or
                    (trans_update and len(trans_update) > 0)
                ):
            msg = f'[{key}] transformations disabled'
            msg += ' because dotfile is linked'
            self.log.warn(msg)
            self.trans_install = []
            self.trans_update = []

    def get_dotfile_variables(self) -> Dict[str, str]:
        """return this dotfile specific variables"""
        return {
            '_dotfile_abs_src': self.src,
            '_dotfile_abs_dst': self.dst,
            '_dotfile_key': self.key,
            '_dotfile_link': str(self.link),
        }

    def get_pre_actions(self) -> List[Action]:
        """return all 'pre' actions"""
        return [a for a in self.actions if a.kind == Action.pre]

    def get_post_actions(self) -> List[Action]:
        """return all 'post' actions"""
        return [a for a in self.actions if a.kind == Action.post]

    def get_trans_install(self) -> List[Transform]:
        """return trans_install object"""
        return self.trans_install

    def get_trans_update(self) -> List[Transform]:
        """return trans_update object"""
        return self.trans_update

    @classmethod
    def _adjust_yaml_keys(cls, value: Dict[str, Any]) -> Dict[str, Any]:
        """patch dict"""
        value['noempty'] = value.get(cls.key_noempty, False)
        value['template'] = value.get(cls.key_template, True)
        # remove old entries
        value.pop(cls.key_noempty, None)
        return value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Dotfile):
            return False
        return self.__dict__ == other.__dict__

    def __hash__(self) -> int:
        return hash(self.dst) ^ hash(self.src) ^ hash(self.key)

    def __str__(self) -> str:
        msg = f'key:\"{self.key}\"'
        msg += f', src:\"{self.src}\"'
        msg += f', dst:\"{self.dst}\"'
        msg += f', link:\"{self.link}\"'
        msg += f', template:{self.template}'
        if self.trans_install:
            msg += f', trans_install:{self.trans_install}'
        if self.trans_update:
            msg += f', trans_update:{self.trans_update}'
        if self.chmod:
            if isinstance(self.chmod, int) or len(self.chmod) == 3:
                msg += f', chmod:{self.chmod:o}'
            else:
                msg += f', chmod:\"{self.chmod}\"'
        return msg

    def prt(self) -> str:
        """extended dotfile to str"""
        indent = '  '
        out = f'dotfile: \"{self.key}\"'
        out += f'\n{indent}src: \"{self.src}\"'
        out += f'\n{indent}dst: \"{self.dst}\"'
        out += f'\n{indent}link: \"{self.link}\"'
        out += f'\n{indent}template: \"{self.template}\"'
        if self.chmod:
            if isinstance(self.chmod, int) or len(self.chmod) == 3:
                out += f'\n{indent}chmod: \"{self.chmod:o}\"'
            else:
                out += f'\n{indent}chmod: \"{self.chmod}\"'

        out += f'\n{indent}pre-action:'
        some = self.get_pre_actions()
        if some:
            for act in some:
                out += f'\n{2 * indent}- {act}'

        out += f'\n{indent}post-action:'
        some = self.get_post_actions()
        if some:
            for act in some:
                out += f'\n{2 * indent}- {act}'

        out += f'\n{indent}trans_install:'
        some = self.get_trans_install()
        if some:
            out += f'\n{2 * indent}- {some}'

        out += f'\n{indent}trans_update:'
        some = self.get_trans_update()
        if some:
            out += f'\n{2 * indent}- {some}'
        return out

    def __repr__(self) -> str:
        return f'dotfile({self})'
