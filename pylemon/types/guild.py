r"""
    :copyright: (c) 2021 by Zaid Ali (email@xarty.xyz) / Hazem Meqdad(hazemmeqdad@gmail.com).
    :license: MIT, see LICENSE for more details.
"""

import typing
import dataclasses

if typing.TYPE_CHECKING:
    from pylemon.client import BaseClient

from pylemon.types.channel import TextChannel, ChannelsTypes
from pylemon.types.member import Member
from pylemon.types.role import Role
from pylemon.types.sticker import Sticker
from pylemon.types.emoji import Emoji
from pylemon.types.voice import VoiceState
from pylemon.types.user import User


from rich import print

@dataclasses.dataclass(init=True)
class Guild:
    """
        The Guild class is a wrapper around the guild object.
        It is used to simplify the usage of the guild object by providing a more readable interface.

        Parameters
        ----------
        client : BaseClient
            The client that the guild is from.
        data : dict
            The guild data.

        Attributes
        ----------
        id : int
            The guild id.
        name : str
            The name of the guild.
        icon : str
            The icon of the guild.
        icon_hash : str
            The hash of the guild icon.
        owner_id : int
            The owner id of the guild.
        region : str
            The region of the guild.
        afk_channel_id : int
            The afk channel id of the guild.
        afk_timeout : int
            The afk timeout of the guild.
        embed_enabled : bool
            Whether the guild has embed enabled.
        embed_channel_id : int
            The embed channel id of the guild.
        verification_level : int
            The verification level of the guild.
        default_notifications : int
            The default notifications of the guild.
        explicit_content_filter : int
            The explicit content filter of the guild.
        roles : list
            The roles of the guild.
        emojis : list
            The emojis of the guild.client : BaseClient
    """
    def __init__(
        self,
        client: "BaseClient",
        data: typing.Dict[str, typing.Union[str,dict,list,int,float,bool]]
    ) -> None:
        from pylemon.types import snowflake
        from pylemon.utils import deserialize_channel

        self.client = client

        self.id: int = snowflake(data.get('id'))
        self.name: str = data.get('name')
        self.icon: typing.Union[str, None]  = data.get('icon')
        self.icon_hash: typing.Union[str, None] = data.get('icon_hash')
        self.splash: str = data.get('splash')
        self.discovery_splash: str = data.get('discovery_splash')
        self.owner_id: int = snowflake(data.get('owner_id'))
        self.region: str = data.get('region')
        self.afk_channel_id: typing.Union[int, None] = snowflake(data.get('afk_channel_id'))
        self.afk_timeout: int = int(data.get('afk_timeout'))
        self.widget_enabled: bool = data.get('widget_enabled')
        self.widget_channel_id: typing.Union[int, None] = snowflake(data.get('widget_channel_id'))
        self.verification_level: int = int(data.get('verification_level'))
        self.default_message_notifications: int = snowflake(data.get('default_message_notifications'))
        self.explicit_content_filter: int = snowflake(data.get('explicit_content_filter'))
        self.features: typing.List[str] = data.get('features')
        self.mfa_level: int = snowflake(data.get('mfa_level'))
        self.application_id: typing.Union[int, None] = snowflake(data.get('application_id'))
        self.system_channel_id: typing.Union[int, None] = snowflake(data.get('system_channel_id'))
        self.rules_channel_id: typing.Union[int, None] = snowflake(data.get('rules_channel_id'))
        self.joined_at: str = data.get('joined_at')
        self.large: bool = data.get('large')
        self.unavailable: bool = data.get('unavailable')
        self.member_count: int = snowflake(data.get('member_count'))
        self.max_presences: int = snowflake(data.get('max_presences'))
        self.max_members: int = snowflake(data.get('max_members'))
        self.vanity_url_code: typing.Union[str, None] = data.get('vanity_url_code')
        self.description: typing.Union[str, None] = data.get('description')
        self.banner: typing.Union[str, None] = data.get('banner')
        self.premium_tier: int = snowflake(data.get('premium_tier'))
        self.premium_subscription_count: int = snowflake(data.get('premium_subscription_count'))
        self.preferred_locale: str = data.get('preferred_locale')
        self.public_updates_channel_id: typing.Union[int, None] = snowflake(data.get('public_updates_channel_id'))
        self.max_video_channel_users: int = snowflake(data.get('max_video_channel_users'))
        self.approximate_member_count: int = snowflake(data.get('approximate_member_count'))
        self.approximate_presence_count: int = snowflake(data.get('approximate_presence_count'))
        self.welcome_screen: typing.Union[typing.Dict[str,typing.Any], None] = data.get('welcome_screen')
        self.nfsw_level: int = snowflake(data.get('nfsw_level'))
        self.premium_progress_bar_enabled: bool = data.get('premium_progress_bar_enabled')

        self.channels: typing.List["ChannelsTypes"] = [
            deserialize_channel(client,self.id, channel) for channel in data.get('channels')
        ]
        self.members: typing.List["Member"] = [
            Member(client, self.id, member['user'] , member) for member in data.get('members')
        ]
        self.users: typing.List["User"] = [
            User(client, user['user']) for user in data.get('members')
        ]
        self.roles: typing.List["Role"] = [
            Role(client, self.id, role) for role in data.get('roles')
        ]
        self.emojis: typing.List["Emoji"] = [
            Emoji(client, self.id, emoji) for emoji in data.get('emojis')
        ]
        self.stickers: typing.List["Sticker"] = [
            Sticker(client, self.id, sticker) for sticker in data.get('stickers')
        ]
        self.threads: typing.List["TextChannel"] = [
            TextChannel(client, self.id, channel) for channel in data.get('threads')
        ]
        self.voicestates: typing.List["VoiceState"] = [
            VoiceState(client, self.id , state) for state in data.get('voice_states')
        ]
        
    # Get method

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

    def get_role(self, id: int) -> "Role":
        """
            Gets a role by id.

            Parameters
            ----------
            id: int
                The id of the role.
        """
        for role in self.roles:
            if role.id == int(id):
                return role

    def get_member(self, id: int) -> "Member":
        """
            Gets a member by id.

            Parameters
            ----------
            id: int
                The id of the member.
        """
        for member in self.members:
            if member.id == int(id):
                return member

    def get_emoji(self, id: int) -> "Emoji":
        """
            Gets an emoji by id.

            Parameters
            ----------
            id: int
                The id of the emoji.
        """
        for emoji in self.emojis:
            if emoji.id == int(id):
                return emoji

    def get_sticker(self, id: int) -> "Sticker":
        """
            Gets a sticker by id.

            Parameters
            ----------
            id: int
                The id of the sticker.
        """
        for sticker in self.stickers:
            if sticker.id == int(id):
                return sticker

    # API

    async def channel_create(self, name: str, type: int, **kwargs) -> "ChannelsTypes":
        """
            Creates a channel.

            Parameters
            ----------
            name: str
                The name of the channel.
            type: int
                The type of the channel.
            kwargs:
                The extra parameters.
        """
        return await self.client.api.guild_create_channel(self.id, name, type, **kwargs)
    
    async def create_role(self, name: str, **kwargs) -> "Role":
        """
            Creates a role.

            Parameters
            ----------
            name: str
                The name of the role.
            kwargs:
                The extra parameters.
        """
        return await self.client.api.guild_create_role(self.id, name, **kwargs)

    async def remove_role(self, role: "Role") -> bool:
        """
            Removes a role.

            Parameters
            ----------
            role: Role
                The role to remove.
        """
        return await self.client.api.guild_delete_role(self.id, role.id)

    async def create_emoji(self, name: str, image: str, reason: str=None) -> "Emoji":
        """
            Creates an emoji.

            Parameters
            ----------
            name: str
                The name of the emoji.
            image: str
                The image of the emoji.
            kwargs:
                The extra parameters.
        """
        return await self.client.api.guild_emojis_create(self.id, name, image, reason=reason)

    async def remove_emoji(self, emoji: "Emoji") -> bool:
        """
            Removes an emoji.

            Parameters
            ----------
            emoji: Emoji
                The emoji to remove.
        """
        return await self.client.api.guild_emojis_delete(self.id, emoji.id)

    async def create_sticker(self, name: str, image: str, reason: str=None) -> "Sticker":
        """
            Creates a sticker.

            Parameters
            ----------
            name: str
                The name of the sticker.
            image: str
                The image of the sticker.
            kwargs:
                The extra parameters.
        """
        return await self.client.api.guild_sticker_create(self.id, name, image, reason=reason)

    async def remove_sticker(self, sticker: "Sticker") -> bool:
        """
            Removes a sticker.

            Parameters
            ----------
            sticker: Sticker
                The sticker to remove.
        """
        return await self.client.api.guild_sticker_delete(self.id, sticker.id)

    async def edit(self, **kwargs) -> "Guild":
        """
            Edits the guild.

            Parameters
            ----------
            kwargs:
                The extra parameters.
        """
        return await self.client.api.guild_edit(self.id, **kwargs)
    
    async def leave(self) -> None:
        """
            Leaves the guild.
        """
        await self.client.api.guild_delete(self.id)