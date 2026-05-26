"""
author: deadc0de6 (https://github.com/deadc0de6)
Copyright (c) 2019, deadc0de6

diverse exceptions
"""

from typing import Any

__all__ = [
    'YamlException',
    'ConfigException',
    'OptionsException',
    'UndefinedException',
    'UnmetDependency',
]


class YamlException(Exception):
    """Exception raised when parsing or loading YAML content."""

    def __init__(self, message: Any = '') -> None:
        super().__init__(message)


class ConfigException(Exception):
    """Exception raised during config parsing or aggregation."""

    def __init__(self, message: Any = '') -> None:
        super().__init__(message)


class OptionsException(Exception):
    """Exception raised for invalid CLI options."""

    def __init__(self, message: Any = '') -> None:
        super().__init__(message)


class UndefinedException(Exception):
    """Exception raised when templating variables are undefined."""

    def __init__(self, message: Any = '') -> None:
        super().__init__(message)


class UnmetDependency(Exception):
    """Exception raised when a required dependency is missing."""

    def __init__(self, message: Any = '') -> None:
        super().__init__(message)
