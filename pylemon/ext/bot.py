r"""
    :copyright: (c) 2021 by Zaid Ali (email@xarty.xyz) / Hazem Meqdad(hazemmeqdad@gmail.com).
    :license: MIT, see LICENSE for more details.
"""

import typing
import asyncio

if typing.TYPE_CHECKING:
    from pylemon.plugin import Plugin

from pylemon.client import BaseClient
from pylemon.intents import Intents
from pylemon.cache import GatewayCache
from pylemon.types import Message

from rich import print

class Bot(BaseClient):
    def __init__(
        self,
        prefix: str,
        token: str,
        intents: typing.Union[typing.List["Intents"], "Intents"],
        *,
        bot: bool = True,
        debug: bool = True,
        cache_client: object = GatewayCache,
        loop: typing.Optional[asyncio.AbstractEventLoop] = None,
        activity: typing.Optional[str] = None,
    ) -> None:
        super().__init__(token, intents, bot=bot, debug=debug, cache_client=cache_client, loop=loop, activity=activity)
        self.prefix = prefix
        self.commands = []

    async def on_message(self,message: Message):
        """
            The handler for the command_create event.
            This event is fired when a message is created.
            This event is the responsible for the command handling. It parse the message and call the command.
        """
        if message.content.startswith(self.prefix) == False:
            return
        
        command = message.content.split(self.prefix)[1].split(' ')[0]
        args = message.content.split(self.prefix)[1].split(' ')[1:]

        for name, callback in self.commands:
            if name == command:
                utils = vars(callback)
                try:
                    if 'required_permission' in utils:
                        if all(permission in message.author.permissions for permission in utils['required_permission']) == False:
                            return
                    elif 'before_command' in utils:
                        resp = await utils['before_command'](message, args)
                        if resp == False:
                            return
                    
                    await callback(message, args)
                except TypeError as e:
                    self.client.log.warn(f'{name} command has wrong args \n{e}')
    
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

    def add_plugin(self, plugin: "Plugin") -> None:
        """
            Add a plugin to the bot.
            That's a special method because it's add command too :) Isn't that crazy?

            Parameters
            ----------
            plugin : Plugin
                The plugin to add.
        """
        for name, callback, args in plugin.comamnds:
            self.commands.append((name, callback, args))
        return super().add_plugin(plugin)
    
    def connect(self, reconnect: bool = True, custom_handler: typing.Awaitable = None) -> None:
        """
            Connect to the gateway and add the command handler.

            Parameters
            ----------
            reconnect : bool
                Whether to reconnect or not.
        """
        if custom_handler is None:
            custom_handler = self.on_message
        self.add_event('message_create', custom_handler)

        return super().connect(reconnect=reconnect)