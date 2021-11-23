"""Util module for the package. It holds some functions to use in core."""
from os.path import join

from .constants import TEMPLATE_PATH


def bool_js(value):
    return str(value).lower()


def read(filename, folder=""):
    with open(join(TEMPLATE_PATH, folder, filename), encoding="utf-8") as file:
        return file.read()
