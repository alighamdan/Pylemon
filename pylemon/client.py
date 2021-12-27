r"""
    :copyright: (c) 2021 by Zaid Ali (email@xarty.xyz) / Hazem Meqdad(hazemmeqdad@gmail.com).
    :license: MIT, see LICENSE for more details.
"""

import typing
import asyncio

if typing.TYPE_CHECKING:
    from pylemon.plugin import Plugin
    from pylemon.intents import Intents

from pylemon.emitter import Emitter
from pylemon.gateway import Gateway
from pylemon.http import HTTP
from pylemon.api import APIClient
from pylemon.logger import logger

from pylemon.types import (
    Guild,

    VoiceState,

    ChannelsTypes,
    TextChannel,
    
    Emoji,
    Sticker,

    Message,

    User,
)

from pylemon.cache import GatewayCache

class BaseClient(Emitter):
    """
        The minmal required class for a client class.
        This help us to inherit from this class and implemnent the required methods and tools.
    """
    def __init__(
        self,
        token: str,
        intents: typing.Union[typing.List["Intents"], "Intents"],
        *,
        bot: bool = True,
        debug: bool = True,
        cache_client: object = GatewayCache,
        loop: typing.Optional[asyncio.AbstractEventLoop] = None,
        activity: typing.Optional[str] = None,
    ) -> None:
        self.token = f'Bot {token}' if bot == True else token
        self.intents = sum(intents) if type(intents) == list else intents
        self.bot = bot
        self.debug = debug
        self.cache_client = cache_client
        self.loop = loop or asyncio.get_event_loop() or asyncio.new_event_loop() ; asyncio.set_event_loop(self.loop)
        self.activity = activity

        self.gateway = Gateway(self)
        self.http = HTTP(self)
        self.api = APIClient(self)
        self.log = logger(self.debug)

        self.user: User = None 

        self.voice_states: typing.List["VoiceState"] = []
        self.guilds: typing.List["Guild"] = []
        self.channels: typing.List["ChannelsTypes"] = []
        self.messages: typing.List["Message"] = []
        self.emojis: typing.List["Emoji"] = []
        self.users: typing.List["User"] = []
        self.stickers: typing.List["Sticker"] = []
        self.threads: typing.List["TextChannel"] = []

        super().__init__(self)
        self.cache_client(self)()


    def listen(self, event: str) -> typing.Callable:
        """
            A decorator that helps us to listen to events.

            Parameters
            ----------
            event: str
                The event to listen to.
        """
        def decorator(func):
            self.add_event(event, func)
            return func
        return decorator

    def event(self, func: typing.Callable):
        """
            Another way to register a event.
        """
        return self.add_event(func.__name__[3:], func)

    def get_guild(self, id: int) -> "Guild":
        """
            Gets a guild by id.

            Parameters
            ----------
            id: int
                The id of the guild.
        """
        for guild in self.guilds:
            if guild.id == int(id):
                return guild

    def get_user(self, id: int) -> "User":
        """
            Gets a user by id.

            Parameters
            ----------
            id: int
                The id of the user.
        """
        for user in self.users:
            if user.id == str(id):
                return user

    def get_channel(self, id: int) -> "ChannelsTypes":
        """
            Gets a channel by id.

            Parameters
            ----------
            id: int
                The id of the channel.
        """
        for channel in self.channels:
            if channel.id == int(id):
                return channel

    def get_message(self, id: int) -> "Message":
        """
            Gets a message by id.

            Parameters
            ----------
            id: int
                The id of the message.
        """
        for message in self.messages:
            if message.id == int(id):
                return message

    def get_emoji(self, id: int) -> "Emoji":
        """
            Gets a emoji by id

            Parameters
            ----------
            id: int
                The id of the emoji
        """

        for emoji in self.emojis:
            if emoji.id == str(id):
                return emoji

    def add_plugin(self, plugin: "Plugin") -> None:
        """
            Adds a plugin to the client.

            Parameters
            ----------
            plugin: typing.Any
                The plugin to add.
        """
        plugin.client = self

        for key,value in plugin.emitter.events:
            self.add_event(key, value)


    def connect(self, reconnect: bool=True) -> None:
        """
            Connects to the gateway.
            This method is a coroutine.

            Parameters
            ----------
            reconnect: bool
                Whether to reconnect to the gateway or not.
            chaced: bool
                Whether to load the cache or not.
        """

        self.loop.run_until_complete(
            self.gateway.connect(reconnect)
        )

class Client(BaseClient):
    """
        The main client class.
        This help us to inherit from this class and implemnent the required methods and tools.
    """
    def __init__(
        self,
        token: str,
        intents: typing.Union[typing.List[int], int],
        *,
        bot: bool = True,
        debug: bool = True,
        loop: typing.Optional[asyncio.AbstractEventLoop] = None,
        activity: typing.Optional[str] = None,
    ) -> None:
        super(Client,self).__init__(
            token,
            intents,
            bot=bot,
            debug=debug,
            loop=loop,
            activity=activity
        )
        
        