r"""
    :copyright: (c) 2021 by Zaid Ali (email@xarty.xyz) / Hazem Meqdad(hazemmeqdad@gmail.com).
    :license: MIT, see LICENSE for more details.
"""

import typing

if typing.TYPE_CHECKING:
    from pylemon.client import BaseClient
    from pylemon.plugin import Plugin

class Emitter:
    def __init__(
        self,
        client: "BaseClient",
    ) -> None:
        self.client = client
        self.loop = self.client.loop
        self.events = []
            

    def add_event(
        self,
        event: str,
        callback: typing.Callable,
    ) -> None:
        self.events.append((event.lower(), callback))

    def remove_event(
        self,
        event: str,
    ) -> None:
        for event_, callback in self.events:
            if event_ == event:
                self.events.remove((event, callback))

    async def emit(
        self,
        event: str,
        *args,
        **kwargs,
    ) -> None:
        for event_, callback in self.events:
            if event_ == event:
                await callback(*args, **kwargs)