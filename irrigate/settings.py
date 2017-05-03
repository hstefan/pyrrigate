#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Classes and functions that provide ways to access user configurations for the application."""

import os.path
from typing import List, Optional
import logging
from .PyrrigateConfig_pb2 import PyrrigateConf
import google.protobuf.text_format as tpb


DEFAULT_CONFIG_PATHS = [os.path.expanduser('~/.pyrrigate.tpb'),
                        '/etc/pyrrigate.tpb',
                        'pyrrigate.tpb']


def get_default_config() -> Optional[PyrrigateConf]:
    """Loads the first existing configuration from the default list of possible paths.
    Returns:
        A PyrrigateConfig object at least one file was found, None otherwise.
    """
    return get_first_config(DEFAULT_CONFIG_PATHS)


def get_first_config(config_paths: List[str]) -> Optional[PyrrigateConf]:
    """Returns the first successfully parsed configuration.
    Returns:
        PyrrigateConfig if successful, None otherwise.
    """
    for path in config_paths:
        conf = _try_parse_pbt(path)
        if conf:
            return conf
    return None


def _try_parse_pbt(path: str) -> Optional[PyrrigateConf]:
    """Attempts to open file and parse a PyrrigateConf from the textual protobuf representation."""
    if not os.path.isfile(path):
        return None
    conf = PyrrigateConf()
    try:
        with open(path, 'r') as conf_file:
            return tpb.Parse(conf_file.read(), conf)
    except tpb.ParseError:
        logging.warning('Unable to parse protobuf file at "%s."', path)
