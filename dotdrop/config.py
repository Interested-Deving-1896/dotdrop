"""
author: deadc0de6 (https://github.com/deadc0de6)
Copyright (c) 2024, deadc0de6

default config
"""

from typing import Final

__all__ = ['DEFAULT_CONFIG']

DEFAULT_CONFIG: Final[str] = """config:
  backup: true
  banner: true
  create: true
  dotpath: dotfiles
  keepdot: false
  link_dotfile_default: nolink
  link_on_import: nolink
  longkey: false
dotfiles:
profiles:"""
