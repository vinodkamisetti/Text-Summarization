# src/textSummarizer/utils/common.py
import unittest
# Monkey-patch to fix ensure annotations on Python 3.12+
unittest.TestCase.assertRaisesRegexp = unittest.TestCase.assertRaisesRegex
import os
from box.exceptions import BoxValueError
import yaml
from textSummarizer.logging import logger
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """Reads YAML file and returns ConfigBox."""
    try:
        with open(path_to_yaml, "r", encoding="utf-8-sig") as yaml_file:
            content = yaml.safe_load(yaml_file)

        if not isinstance(content, dict):
            raise ValueError(f"\nYAML file is not a dictionary.\nPath: {path_to_yaml}\nType: {type(content)}\nContent:\n{content}")

        logger.info(f"YAML file: {path_to_yaml} loaded successfully")
        return ConfigBox(content)

    except BoxValueError:
        raise ValueError("YAML file is empty or contains invalid content.")
    except Exception as e:
        raise e


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """create list of directories

    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")



@ensure_annotations
def get_size(path: Path) -> str:
    """get size in KB

    Args:
        path (Path): path of the file

    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"