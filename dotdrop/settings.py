"""
author: deadc0de6 (https://github.com/deadc0de6)
Copyright (c) 2019, deadc0de6

settings block
"""

import os
from typing import Dict, List, Optional, Union

from dotdrop.exceptions import YamlException

# local imports
from dotdrop.linktypes import LinkTypes
from dotdrop.dictparser import DictParser
from dotdrop.utils import is_bin_in_path

__all__ = ['Settings']


ENV_WORKDIR = 'DOTDROP_WORKDIR'


class Settings(DictParser):
    """Settings block in config"""
    # pylint: disable=too-many-instance-attributes
    # key in yaml file
    key_yaml = 'config'

    # settings item keys
    key_backup = 'backup'
    key_banner = 'banner'
    key_create = 'create'
    key_default_actions = 'default_actions'
    key_dotpath = 'dotpath'
    key_ignoreempty = 'ignoreempty'
    key_keepdot = 'keepdot'
    key_longkey = 'longkey'
    key_link_dotfile_default = 'link_dotfile_default'
    key_link_on_import = 'link_on_import'
    key_showdiff = 'showdiff'
    key_upignore = 'upignore'
    key_impignore = 'impignore'
    key_cmpignore = 'cmpignore'
    key_instignore = 'instignore'
    key_workdir = 'workdir'
    key_minversion = 'minversion'
    key_func_file = 'func_file'
    key_filter_file = 'filter_file'
    key_diff_command = 'diff_command'
    key_force_chmod = 'force_chmod'
    key_template_dotfile_default = 'template_dotfile_default'
    key_ignore_missing_in_dotdrop = 'ignore_missing_in_dotdrop'
    key_chmod_on_import = 'chmod_on_import'
    key_check_version = 'check_version'
    key_clear_workdir = 'clear_workdir'
    key_compare_workdir = 'compare_workdir'
    key_key_prefix = 'key_prefix'
    key_key_separator = 'key_separator'

    # import keys
    key_import_actions = 'import_actions'
    key_import_configs = 'import_configs'
    key_import_variables = 'import_variables'

    # defaults
    default_diff_cmd = 'diff -r -u {0} {1}'

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments,too-many-locals
    def __init__(self, backup: bool = True, banner: bool = True,
                 create: bool = True,
                 default_actions: Optional[List[str]] = None,
                 dotpath: str = 'dotfiles',
                 ignoreempty: bool = False,
                 import_actions: Optional[List[str]] = None,
                 import_configs: Optional[List[str]] = None,
                 import_variables: Optional[List[str]] = None,
                 keepdot: bool = False,
                 link_dotfile_default: Union[LinkTypes, str] =
                 LinkTypes.NOLINK,
                 link_on_import: Union[LinkTypes, str] = LinkTypes.NOLINK,
                 longkey: bool = False,
                 upignore: Optional[List[str]] = None,
                 cmpignore: Optional[List[str]] = None,
                 instignore: Optional[List[str]] = None,
                 impignore: Optional[List[str]] = None,
                 workdir: str = '~/.config/dotdrop',
                 showdiff: bool = False,
                 minversion: Optional[str] = None,
                 func_file: Optional[List[str]] = None,
                 filter_file: Optional[List[str]] = None,
                 diff_command: str = default_diff_cmd,
                 template_dotfile_default: bool = True,
                 ignore_missing_in_dotdrop: bool = False,
                 force_chmod: bool = False,
                 chmod_on_import: bool = False,
                 check_version: bool = False,
                 clear_workdir: bool = False,
                 compare_workdir: bool = False,
                 key_prefix: bool = True,
                 key_separator: str = '_') -> None:
        self.backup = backup
        self.banner = banner
        self.create = create
        self.default_actions = default_actions or []
        self.dotpath = dotpath
        self.ignoreempty = ignoreempty
        self.import_actions = import_actions or []
        self.import_configs = import_configs or []
        self.import_variables = import_variables or []
        self.keepdot = keepdot
        self.longkey = longkey
        self.showdiff = showdiff
        self.upignore = upignore or []
        self.cmpignore = cmpignore or []
        self.instignore = instignore or []
        self.impignore = impignore or []
        self.workdir = workdir
        if ENV_WORKDIR in os.environ:
            self.workdir = os.environ[ENV_WORKDIR]
        self.link_dotfile_default = LinkTypes.get(link_dotfile_default)
        self.link_on_import = LinkTypes.get(link_on_import)
        self.minversion = minversion
        self.func_file = func_file or []
        self.filter_file = filter_file or []
        self.diff_command = diff_command
        self.template_dotfile_default = template_dotfile_default
        self.ignore_missing_in_dotdrop = ignore_missing_in_dotdrop
        self.force_chmod = force_chmod
        self.chmod_on_import = chmod_on_import
        self.check_version = check_version
        self.clear_workdir = clear_workdir
        self.compare_workdir = compare_workdir
        self.key_prefix = key_prefix
        self.key_separator = key_separator

        # check diff command
        if not is_bin_in_path(self.diff_command):
            err = f'bad diff_command: {diff_command}'
            raise YamlException(err)

    def _serialize_seq(self, name: str, dic: Dict[str, object]) -> None:
        """serialize attribute 'name' into 'dic'"""
        seq = getattr(self, name)
        dic[name] = seq

    def serialize(self) -> Dict[str, Dict[str, object]]:
        """Return key-value pair representation of the settings"""
        dic = {
            self.key_backup: self.backup,
            self.key_banner: self.banner,
            self.key_create: self.create,
            self.key_dotpath: self.dotpath,
            self.key_ignoreempty: self.ignoreempty,
            self.key_keepdot: self.keepdot,
            self.key_link_dotfile_default: str(self.link_dotfile_default),
            self.key_link_on_import: str(self.link_on_import),
            self.key_longkey: self.longkey,
            self.key_showdiff: self.showdiff,
            self.key_workdir: self.workdir,
            self.key_minversion: self.minversion,
            self.key_diff_command: self.diff_command,
            self.key_template_dotfile_default: self.template_dotfile_default,
            self.key_ignore_missing_in_dotdrop: self.ignore_missing_in_dotdrop,
            self.key_force_chmod: self.force_chmod,
            self.key_chmod_on_import: self.chmod_on_import,
            self.key_check_version: self.check_version,
            self.key_clear_workdir: self.clear_workdir,
            self.key_compare_workdir: self.compare_workdir,
            self.key_key_prefix: self.key_prefix,
            self.key_key_separator: self.key_separator,
        }
        self._serialize_seq(self.key_default_actions, dic)
        self._serialize_seq(self.key_import_actions, dic)
        self._serialize_seq(self.key_import_configs, dic)
        self._serialize_seq(self.key_import_variables, dic)
        self._serialize_seq(self.key_cmpignore, dic)
        self._serialize_seq(self.key_upignore, dic)
        self._serialize_seq(self.key_instignore, dic)
        self._serialize_seq(self.key_impignore, dic)
        self._serialize_seq(self.key_func_file, dic)
        self._serialize_seq(self.key_filter_file, dic)

        return {self.key_yaml: dic}
