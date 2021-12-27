r"""
    :copyright: (c) 2021 by Zaid Ali (email@xarty.xyz) / Hazem Meqdad(hazemmeqdad@gmail.com).
    :license: MIT, see LICENSE for more details.
"""

import io
import typing
import dataclasses

if typing.TYPE_CHECKING:
    from pylemon.client import BaseClient
    from pylemon.types import (
        Message,
        Invite,

        Webhook,
    )

from .permissions import Permission

from .types import snowflake

class ChannelType:
    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GROUP_DM = 3
    GUILD_CATEGORY = 4
    GUILD_NEW = 5
    GUILD_STORE = 6
    GUILD_NEWS_THREAD = 10
    GUILD_PUBLIC_THREAD = 11
    GUILD_PRIVATE_THREAD = 12
    GUILD_STAGE_VOICE = 13

class PermissionOverwriteType:
    ROLE = 0
    MEMBER = 1

class PermissionOverwrite:
    def __init__(
        self,
        data: typing.Dict[str, typing.Union[str, dict, list, int, float, bool]],
    ):
        self.id: int = snowflake(data.get('id'))
        self.type: int = snowflake(data.get('type'))
        self.allow: int = Permission(data.get('allow')).compute_permissions()
        self.deny: int = Permission(data.get('deny')).compute_permissions()

@dataclasses.dataclass(init=True)
class GuildChannel:
    
    def __init__(
        self,
        client: "BaseClient",
        guild_id: int,
        data: typing.Dict[str, typing.Union[str,dict,list,int,float,bool]],
    ) -> None:
        self.client = client

        self.guild_id: int = int(guild_id)

        self.id: int = snowflake(data.get('id'))
        self.name: str = data.get('name')
        self.type: int = data.get('type')
        self.position: snowflake = snowflake(data.get('position'))
        self.permission_overwrites: list = [PermissionOverwrite(x) for x in data.get('permission_overwrites')]

    async def delete(self,reason: str=None) -> "GuildChannel":
        """
            Deletes the channel.

            Parameters
            ----------
            reason : str    
                The reason of the deletion.
        """
        return await self.client.api.channel_delete(
            self.id,
            reason=reason
        )

    async def edit(self,name: str,reason: str=None, **kwargs) -> "GuildChannel":
        """
            Updates the channel.

            Parameters
            ----------
            name : str
                The new name of the channel.
            reason : str
                The reason of the update.
        """
        return await self.client.api.channel_modify(
            self.id,
            name=name,
            reason=reason
            **kwargs
        )

    async def create_invite(self,max_age: int=0,max_uses: int=0,temporary: bool=False,reason: str=None) -> "Invite":
        """
            Creates an invite for the channel.

            Parameters
            ----------
            max_age : int
                The max age of the invite.
            max_uses : int
                The max uses of the invite.
            temporary : bool
                Whether the invite is temporary.
            reason : str
                The reason of the creation.
        """
        return await self.client.api.channel_invite_create(
            self.id,
            max_age=max_age,
            max_uses=max_uses,
            temporary=temporary,
            reason=reason
        )

    async def remove_invite(self,code: str,reason: str=None) -> "Invite":
        """
            Removes an invite from the channel.

            Parameters
            ----------
            code : str
                The code of the invite.
            reason : str
                The reason of the removal.
        """
        return await self.client.api.channel_invite_delete(
            self.id,
            code=code,
            reason=reason
        )
        

@dataclasses.dataclass(init=True)
class TextChannel(GuildChannel):

    def __init__(
        self,
        client: "BaseClient",
        guild_id: int,
        data: typing.Dict[str, typing.Union[str,dict,list,int,float,bool]],
    ) -> None:
        self.client = client

        self.ratelimit: int = snowflake(data.get('rate_limit_per_user',None))
        self.topic: str = data.get('topic')
        self.nsfw: bool = data.get('nsfw')
        self.last_message_id: int = snowflake(data.get('last_message_id'))

        super().__init__(client, guild_id , data)

    async def send(self, content: str, embeds: typing.List=[], tts: bool=False, files: typing.List[io.StringIO]=[], **kwargs) -> "Message":
        """
            Sends a message to the channel.

            Parameters
            ----------
            content : str
                The content of the message.
            embeds : list
                The embeds of the message.
            tts : bool
                Whether the message is text-to-speech.
            files : list
                The files of the message.
        """
        return await self.client.api.channel_message_post(
            self.id,
            content=content,
            tts=tts,
            embeds=embeds,
            files=files,
            **kwargs
        )

    async def create_webhook(self,name: str,reason: str=None) -> "Webhook":
        """
            Creates a webhook for the channel.

            Parameters
            ----------
            name : str
                The name of the webhook.
            reason : str
                The reason of the creation.
        """
        return await self.client.api.channel_webhook_create(
            self.id,
            name=name,
            reason=reason
        )

    async def remove_webhok(self,webhook_id: int,reason: str=None) -> "Webhook":
        """
            Removes a webhook from the channel.

            Parameters
            ----------
            webhook_id : int
                The id of the webhook.
            reason : str
                The reason of the deletion.
        """
        return await self.client.api.channel_webhook_delete(
            self.id,
            webhook_id=webhook_id,
            reason=reason
        )

    async def get_webhooks(self) -> typing.List["Webhook"]:
        """
            Gets the webhooks of the channel.
        """
        return await self.client.api.channel_webhook_list(
            self.id
        )
    
    async def fetch_messages(self,limit: int=100,before: int=None,after: int=None) -> typing.List["Message"]:
        """
            Gets the messages of the channel.

            Parameters
            ----------
            limit : int
                The limit of the messages.
            before : int
                The message before the one to get.
            after : int
                The message after the one to get.
        """
        return await self.client.api.channel_message_list(
            self.id,
            limit=limit,
            before=before,
            after=after
        )
    
    async def fetch_message(self,message_id: int) -> "Message":
        """
            Gets the message of the channel.

            Parameters
            ----------
            message_id : int
                The id of the message.
        """
        return await self.client.api.channel_message_get(
            self.id,
            message_id=message_id
        )

    async def fetch_invites(self) -> typing.List["Invite"]:
        """
            Gets the invites of the channel.
        """
        return await self.client.api.channel_invites_list(
            self.id
        )

    async def fetch_pins(self) -> typing.List["Message"]:
        """
            Gets the pins of the channel.
        """
        return await self.client.api.channel_pins_list(
            self.id
        )
    


@dataclasses.dataclass(init=True)
class VoiceChannel(GuildChannel):
    def __init__(
        self,
        client: "BaseClient",
        guild_id: int,
        data: typing.Dict[str, typing.Union[str,dict,list,int,float,bool]],
        ) -> None:

        self.bitrate: int = snowflake(data.get('bitrate',None))
        self.video_quality_mode: str = data.get('video_quality_mode',None)
        self.rtc_region: str = data.get('rtc_region',None)

        super().__init__(client, guild_id, data)

    async def connect(self):
        await self.client.gateway.send(4,{
            "guild_id": self.guild_id,
            "channel_id": self.id,
        })

@dataclasses.dataclass(init=True)
class DMChannel(GuildChannel):
    def __init__(
        self,
        client: "BaseClient",
        guild_id: int,
        data: typing.Dict[str, typing.Union[str,dict,list,int,float,bool]],
        ) -> None:

        self.recipients: typing.List = data.get('recipients',None)
        self.owner_id: int = snowflake(data.get('owner_id',None))

        super().__init__(client, guild_id, data)

@dataclasses.dataclass(init=True)
class CategoryChannel(GuildChannel):
    def __init__(
        self,
        client: "BaseClient",
        guild_id: int,
        data: typing.Dict[str, typing.Union[str,dict,list,int,float,bool]],
        ) -> None:

        self.id: int = snowflake(data.get('id',None))

        super().__init__(client, guild_id, data)

ChannelsTypes = typing.Union[
    CategoryChannel,
    TextChannel,
    VoiceChannel,
    DMChannel,
]

