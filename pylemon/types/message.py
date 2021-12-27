r"""
    :copyright: (c) 2021 by Zaid Ali (email@xarty.xyz) / Hazem Meqdad(hazemmeqdad@gmail.com).
    :license: MIT, see LICENSE for more details.
"""

import typing
import dataclasses
from pylemon.types.emoji import Emoji

if typing.TYPE_CHECKING:
    from pylemon.client import BaseClient
    from pylemon.types import Reaction as _Reaction
    from pylemon.types import (
        Guild,
        Member,
        User,
        ChannelsTypes,
    )

from .emoji import Emoji

@dataclasses.dataclass(init=True)
class Attachment:
    def __init__(
        self,
        data: typing.Dict[str, typing.Union[str, dict, list, int, float, bool]],
    ) -> None:
        self.id: int = int(data.get('id'))
        self.filename: str = data.get('filename')
        self.width: int = int(data.get('width'))
        self.height: int = int(data.get('height'))
        self.size: int = int(data.get('size'))
        self.url: str = data.get('url')
        self.proxy_url: str = data.get('proxy_url')
        self.mime_type: str = data.get('content_type')

@dataclasses.dataclass(init=True)
class Field:
    def __init__(
        self,
        data: typing.Dict[str, typing.Union[str, dict, list, int, float, bool]],
    ):
        self.name: str = data.get('name')
        self.value: str = data.get('value')
        self.inline: bool = data.get('inline')

@dataclasses.dataclass(init=True)
class Embed:
    def __init__(
        self,
        data: typing.Dict[str, typing.Union[str, dict, list, int, float, bool]],
    ) -> None:
        self.tittle: typing.Union[str,None] = data.get('title')
        self.type: typing.Union[str,None] = data.get('type')
        self.description: typing.Union[str,None] = data.get('description')
        self.url: typing.Union[str,None] = data.get('url')
        self.timestamp: typing.Union[str,None] = data.get('timestamp') if data.get('timestamp') else None
        self.color: typing.Union[int,None] = data.get('color')
        self.footer: typing.Union[str,None] = data.get('footer')
        self.footer_icon: typing.Union[str,None] = data.get('footer_icon')
        self.image: typing.Union[str,None] = data.get('image')
        self.thumbnail: typing.Union[str,None] = data.get('thumbnail')
        self.video: typing.Union[str,None] = data.get('video')
        self.provider: typing.Union[str,None] = data.get('provider')
        self.fileds: typing.Union[list,None] = [
            Field(field) for field in data.get('fields')
        ]

@dataclasses.dataclass(init=True)
class Reaction:
    def __init__(
        self,
        client: "BaseClient",
        data: typing.Dict[str, typing.Union[str, dict, list, int, float, bool]],
    ) -> None:
        self.client = client

        self.count: int = int(data.get('count'))
        self.me: bool = data.get('me')
        self.emoji: typing.Union[Emoji,None] = Emoji(self.client, data.get('emoji'))

@dataclasses.dataclass(init=True)
class Message:
    """
    """
    def __init__(
        self,
        client: "BaseClient",
        data: typing.Dict[str, typing.Union[str,dict,list,int,float,bool]],
    ) -> None:
        self.client = client

        self.id: int = int(data.get("id"))
        self.channel_id: int = int(data.get("channel_id"))
        self.guild_id: typing.Union[int,None] = (int(data.get("guild_id")) 
            if data.get("guild_id") else None)
        self.content: str = data.get("content")
        self.timestamp: str = data.get("timestamp")
        self.edited_timestamp: str = data.get("edited_timestamp") if data.get("edited_timestamp") else None
        self.tts: bool = data.get("tts")
        self.mention_everyone: bool = data.get("mention_everyone")
        self.mentions: typing.List[int] = [
            int(user['id']) for user in data.get("mentions")
        ]
        self.mention_roles: typing.List[int] = [
            int(role['id']) for role in data.get("mention_roles")
        ]
        self.mention_channels: typing.Union[typing.List[int],None] = [
            int(channel['id']) for channel in data.get("mention_channels",[])
        ]
        self.attachments: typing.List[Attachment,None] = [
            Attachment(attachment) for attachment in data.get("attachments")
        ]
        self.embeds: typing.List[Embed] = [
            Embed(embed) for embed in data.get("embeds")
        ]
        self.author_id: int = int(data.get("author").get("id"))
        self.thread_id: typing.Union[int,None] = (int(data.get("thread",{}).get("id",None)) if 
            data.get("thread",{}).get("id",None) else None)
        self.message_flags: int = data.get("flags")
        self.message_reference: typing.Dict[str,str] = data.get("message_reference")
        self.reacts: typing.Union[typing.List[Reaction],None] = [
            Reaction(self.client, reaction) for reaction in data.get("reactions",[])
        ]
        self.reactions: typing.List["_Reaction"] = []


        self.flags_dict = {
            'CROSSPOSTED': 1 << 0,
            'IS_CROSSPOST': 1 << 1,
            'SUPPRESS_EMBEDS': 1 << 2,
            'SOURCE_MESSAGE_DELETED': 1 << 3,
            'URGENT': 1 << 4,
            'HAS_THREAD': 1 << 5,
            'EPHEMERAL': 1 << 6,
            'LOAD_REPLY_MESSAGE': 1 << 7,
        }

    def has_flag(self, flag: str) -> bool:
        """
            Check if the message has a flag.

            Parameters
            ----------
            flag: str
                The flag to check.
        """

        return self.message_flags & self.flags_dict[flag]

    @property
    def flags(self) -> typing.List[str]:
        """
            Get the message flags.
        """
        return [ 
            key for key ,val in self.flags_dict.items() if self.message_flags & val
        ]

    @property
    def guild(self) -> typing.Union["Guild",None]:
        """
            Get the guild the message was sent in.
        """
        if self.guild_id:
            return self.client.get_guild(self.guild_id)

    @property
    def channel(self) -> typing.Union["ChannelsTypes",None]:
        """
            Get the channel the message was sent in.
        """
        return self.client.get_channel(self.channel_id)

    @property
    def author(self) -> "Member":
        """
            Get the author of the message.
        """
        return self.client.get_guild(self.guild_id).get_member(self.author_id)

    async def delete(self,reason: str=None) -> bool:
        """
            Delete the message.

            Parameters
            ----------
            reason: str
                The reason for deleting the message.
        """
        return await self.client.api.channel_message_delete(self.channel_id, self.id, reason=reason)

    async def edit(self,content: str,embed: typing.Union[Embed,None]=None) -> bool:
        """
            Edit the message.

            Parameters
            ----------
            content: str
                The new content for the message.
            embed: Embed
                The new embed for the message.
        """
        return await self.client.api.channel_message_modfiy(
            self.channel_id,
            self.id,
            content=content,
            embed=embed,
        )

    async def pin(self, reason: str=None) -> bool:
        """
            Pin the message.

            Parameters
            ----------
            reason: str
                The reason for pinning the message.
        """
        return await self.client.api.channel_pins_add(
            self.channel_id,
            self.id,
            reason=reason,
        )

    async def unpin(self, reason: str=None) -> bool:
        """
            Unpin the message.

            Parameters
            ----------
            reason: str
                The reason for unpinning the message.
        """
        return await self.client.api.channel_pins_remove(
            self.channel_id,
            self.id,
            reason=reason,
        )

    async def add_reaction(self,emoji: "Emoji") -> bool:
        """
            Add a reaction to the message.

            Parameters
            ----------
            emoji: Emoji
                The emoji to add.
        """
        return await self.client.api.channel_message_reaction_post(
            self.channel_id,
            self.id,
            emoji.id,
        )

    async def remove_reaction(self,emoji: "Emoji",user: "User") -> bool:
        """
            Remove a reaction from the message.

            Parameters
            ----------
            emoji: Emoji
                The emoji to remove.
            user: User
                The user to remove the reaction from.
        """
        return await self.client.api.channel_message_reaction_delete(
            self.channel_id,
            self.id,
            emoji.id,
            user.id,
        )
        

    def __repr__(self) -> str:
        return f"<Message id={self.id} content={self.content}>"

