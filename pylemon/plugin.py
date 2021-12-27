r"""
    :copyright: (c) 2021 by Zaid Ali (email@xarty.xyz) / Hazem Meqdad(hazemmeqdad@gmail.com).
    :license: MIT, see LICENSE for more details.
"""

import typing
import asyncio

if typing.TYPE_CHECKING:
    from pylemon.client import BaseClient

from pylemon.emitter import Emitter

class Plugin:
    def __init__(
        self,
        name: str,
    ) -> None:
        self.name = name
        self.loop = asyncio.get_event_loop()
        self.client: "BaseClient" = None

        self.emitter = Emitter(self)
        self.comamnds = []

    def listen(self, event: str) -> typing.Callable:
        """
            A decorator that helps us to listen to events.

            Parameters
            ----------
            event: str
                The event to listen to.
        """
        def decorator(func):
            self.emitter.add_event(event, func)
            return func
        return decorator

    def command(self, name: str) -> None:
        """
            To create a command.
            
            Parameters
            ----------
            name : str
                The name of the command.
        """
        def deco(func):
            self.commands.append((name, func))
            return func
        return deco

    def event(self, func: typing.Callable):
        """
            Another way to register a event.
        """
        return self.emitter.add_event(func.__name__[3:], func)
