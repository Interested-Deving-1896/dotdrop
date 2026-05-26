"""
author: deadc0de6 (https://github.com/deadc0de6)
Copyright (c) 2019, deadc0de6

dictionary parser abstract class
"""

from typing import Any, Dict, List, Mapping, Type, TypeVar

from dotdrop.logger import Logger

__all__ = ['DictParser']

T = TypeVar('T', bound='DictParser')


class DictParser:
    """a dict parser"""

    log = Logger()

    @classmethod
    def _adjust_yaml_keys(cls, value: Dict[str, Any]) -> Dict[str, Any]:
        """adjust value for object 'cls'"""
        return value

    @classmethod
    def parse(cls: Type[T], key: Any, value: Dict[str, Any]) -> T:
        """parse (key,value) and construct object 'cls'"""
        tmp = value
        try:
            tmp = value.copy()
        except AttributeError:
            pass
        newv = cls._adjust_yaml_keys(tmp)
        if not key:
            return cls(**newv)
        return cls(key=key, **newv)

    @classmethod
    def parse_dict(
            cls: Type[T],
            items: Mapping[Any, Dict[str, Any]]) -> List[T]:
        """parse a dictionary and construct object 'cls'"""
        if not items:
            return []
        return [cls.parse(k, v) for k, v in items.items()]
