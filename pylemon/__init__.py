r"""
    :copyright: (c) 2021 by Zaid Ali (email@xarty.xyz) / Hazem Meqdad(hazemmeqdad@gmail.com).
    :license: MIT, see LICENSE for more details.
    
    Pylemon is a Discord wrapper to build high efficiency bots. It is built for simplicity and efficiency.
"""

__version__ = "0.1"
__author__ = ("Zaid Ali", "Hazem Meqdad")
__license__ = "MIT"

from .client import Client
from .plugin import Plugin
from .events import Events
from .intents import Intents

from .ext import Bot
from .ext import has_permission, before_command

from .types import *