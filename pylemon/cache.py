r"""
    :copyright: (c) 2021 by Zaid Ali (email@xarty.xyz) / Hazem Meqdad(hazemmeqdad@gmail.com).
    :license: MIT, see LICENSE for more details.
"""

import typing

if typing.TYPE_CHECKING:
    from pylemon.client import BaseClient

from pylemon.types import *

from rich import print

class GatewayCache:
    def __init__(
        self,
        client: "BaseClient",
    ) -> None:
        self.client = client

    def __call__(self):
        for method in dir(self):
            if method.startswith("on_"):
                self.client.add_event(method[3:], getattr(self, method))

    async def on_guild_create(self, guild: "Guild") -> None:
        for channel in guild.channels:
            self.client.channels.append(channel)
        for thread in guild.threads:
            self.client.threads.append(thread)
        for user in guild.users:
            self.client.users.append(user)
        for emoji in guild.emojis:
            self.client.emojis.append(emoji)
        for sticker in guild.stickers:
            self.client.stickers.append(sticker)

        self.client.guilds.append(guild)

    async def on_message_create(self, message: "Message") -> None:
        self.client.messages.append(message)
    
    async def on_message_delete(self, message: "Message") -> None:
        self.client.messages.remove(message)

    async def on_message_update(self, before: "Message", after: "Message") -> None:
        self.client.messages.remove(before)
        self.client.messages.append(after)
    
    async def on_guild_role_create(self, guild: "Guild",role: "Role") -> None:
        guild.roles.append(role)

    async def on_guild_role_delete(self, guild: "Guild",role: "Role") -> None:
        guild.roles.remove(role)

    async def on_guild_role_update(self, guild: "Guild",before: "Role",after: "Role") -> None:
        guild.roles.remove(before)
        guild.roles.append(after)

    async def on_channel_create(self, channel: "ChannelsTypes") -> None:
        self.client.channels.append(channel)

    async def on_channel_delete(self, channel: "ChannelsTypes") -> None:
        self.client.channels.remove(channel)
    
    async def on_channel_update(self, before: "ChannelsTypes", after: "ChannelsTypes") -> None:
        self.client.channels.remove(before)
        self.client.channels.append(after)
        
    async def on_guild_member_add(self,guild: "Guild", member: "Member") -> None:
        self.client.users.append(User(self.client, vars(member)))
        guild.members.append(member)

    async def on_guild_member_remove(self, guild: "Guild", member: "Member") -> None:
        self.client.users.remove([user for user in self.client.users if user.id == member.id][0])
        guild.members.remove(member)
    
    async def on_guild_member_update(self, guild: "Guild", before: "Member", after: "Member") -> None:
        guild.members.remove(before)
        guild.members.append(after)
    
    async def on_guild_update(self, guild: "Guild", before: "Guild", after: "Guild") -> None:
        ... 

    async def on_message_reaction_add(self, message: "Message", reaction: "Reaction") -> None:
        message.reactions.append(reaction)

    async def on_message_reaction_remove(self, message: "Message", reaction: "Reaction") -> None:
        message.reactions.remove([_reaction for _reaction in message.reactions if _reaction.emoji == reaction.emoji][0])

    async def on_guild_emojis_update(self, guild: "Guild", emojis: typing.List["Emoji"]) -> None:
        for emoji in emojis:
            for emoji in guild.emojis:
                if emoji.id == emoji.id:
                    guild.emojis.remove(emoji)
                    self.client.emojis.remove(emoji)
            guild.emojis.append(emoji)
            self.client.emojis.append(emoji)
    
    async def on_guild_stickers_update(self, guild: "Guild", stickers: typing.List["Sticker"]) -> None:
        for sticker in stickers:
            for sticker in guild.stickers:
                if sticker.id == sticker.id:
                    guild.stickers.remove(sticker)
                    self.client.stickers.remove(sticker)
            guild.stickers.append(sticker)
            self.client.stickers.append(sticker)
    
    async def on_voice_server_update(self, guild: "Guild", voice_server: "VoiceServer") -> None:
        if voice_server.endpoint:
            guild.voice_server = voice_server
        else:
            guild.voice_server = None
            
    
    

    
    


    