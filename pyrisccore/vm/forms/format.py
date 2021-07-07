""" An instruction "format" is a uniquely named composition of fields
"""

from dataclasses import dataclass
from typing import Tuple

from pyrisccore.vm.forms.field import Field


@dataclass
class Format:
    """ An instruction format
    """

    name: str  # e.g. J
    fields: Tuple[Field, ...]


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4