r"""
    :copyright: (c) 2021 by Zaid Ali (email@xarty.xyz) / Hazem Meqdad(hazemmeqdad@gmail.com).
    :license: MIT, see LICENSE for more details.
"""

import typing
import json
import asyncio

from pylemon.types.message import Embed

if typing.TYPE_CHECKING:
    from pylemon.client import BaseClient

from pylemon.http import Route

from pylemon.types import (
    Guild,
    Invite,
    Role,

    Emoji,
    Sticker,
    Reaction,

    ChannelsTypes,
    TextChannel,
    Webhook,

    VoiceState,
    Member,
    User,

    Message,
)
from pylemon.utils import deserialize_channel


def _reason(reason: str) -> str:
    return {'X-Audit-Log-Reason': reason.encode('utf-8')}

class APIClient:
    def __init__(
        self,
        client: "BaseClient",
    ) -> None:
        self.client = client

    async def gateway_get(self) -> typing.Dict[str, str]:
        return await self.client.http.request(
            Route('/gateway', 'GET'),
        )
    
    async def gateway_bot_get(self) -> typing.Dict[str, str]:
        return await self.client.http.request(
            Route('/gateway/bot', 'GET')
        )

    async def channel_get(self, channel_id: int) -> "ChannelsTypes":
        r =  await self.client.http.request(
            Route(f'/channels/{channel_id}', 'GET')
        )
        return deserialize_channel(self.client, r)

    async def channel_modify(self, reason: str=None, **kwargs) -> "ChannelsTypes":
        r = await self.client.http.request(
            Route('/channels', 'PATCH'),
            json=kwargs,
            headears=_reason(reason)
        )
        return deserialize_channel(self.client, r)

    async def channel_delete(self, channel_id: int, reason: str=None) -> "ChannelsTypes":
        r = await self.client.http.request(
            Route(f'/channels/{channel_id}', 'DELETE'),
            headears=_reason(reason)
        )
        return deserialize_channel(self.client, r)

    async def channel_typing(self, channel_id: int) -> None:
        await self.client.http.request(
            Route(f'/channels/{channel_id}/typing', 'POST')
        )
    
    async def channel_message_list(self, channel_id: int, limit: int=100) -> typing.List["Message"]:
        r = await self.client.http.request(
            Route(f'/channels/{channel_id}/messages', 'GET'),
            params={'limit': limit}
        )
        return [Message(self.client,m) for m in r]

    async def channel_message_get(self, channel_id: int, message_id: int) -> "Message":
        r = await self.client.http.request(
            Route(f'/channels/{channel_id}/messages/{message_id}', 'GET')
        )
        return Message(self.client, r)

    async def channel_message_post(
        self, 
        channel_id: int, 
        content: str, 
        embeds: typing.List["Embed"]=[],
        tts: bool=False,
        files: typing.List[typing.IO]=None,
        nonce: int=None,
        allowed_mentions: typing.Dict[str, typing.Any]=None,
        **kwargs
    ) -> "Message":
        r = await self.client.http.request(
            Route(f'/channels/{channel_id}/messages', 'POST'),
            data={'payload_json': json.dumps({
                'content': content,
                'embed': embeds,
                'tts': tts,
                'nonce': nonce,
                'allowed_mentions': allowed_mentions,
                'files': files,
                **kwargs
            })},
        )
        return Message(self.client, r)

    async def channel_message_modfiy(
        self, 
        channel_id: int, 
        message_id: int, 
        content: str, 
        embeds: typing.List["Embed"]=[]
    ) -> "Message":
        r = await self.client.http.request(
            Route(f'/channels/{channel_id}/messages/{message_id}', 'PATCH'),
            json={
                'content': content,
                'embed': [embed.to_dict() for embed in embeds],
            },
        )
        return Message(self.client, r)

    async def channel_message_delete(
        self, 
        channel_id: int, 
        message_id: int, 
        reason: str=None
    ) -> None:
        await self.client.http.request(
            Route(f'/channels/{channel_id}/messages/{message_id}', 'DELETE'),
            headears=_reason(reason)
        )

    async def channel_message_bulk_delete(
        self, 
        channel_id: int, 
        message_ids: typing.List[int], 
        reason: str=None
    ) -> None:
        await self.client.http.request(
            Route(f'/channels/{channel_id}/messages', 'DELETE'),
            json={'messages': message_ids},
            headears=_reason(reason)
        )

    async def channel_message_pin(
        self, 
        channel_id: int, 
        message_id: int, 
        reason: str=None
    ) -> None:
        await self.client.http.request(
            Route(f'/channels/{channel_id}/pins/{message_id}', 'PUT'),
            headears=_reason(reason)
        )

    async def channel_message_reaction_get(
        self, 
        channel_id: int, 
        message_id: int, 
        emoji: "Emoji", 
        limit: int=100
    ) -> typing.List["Reaction"]:
        r = await self.client.http.request(
            Route(f'/channels/{channel_id}/messages/{message_id}/reactions/{emoji.name}:{emoji.id}', 'GET'),
            params={'limit': limit}
        )
        return [Reaction(self.client, r) for r in r]

    async def channel_message_reaction_post(
        self, 
        channel_id: int, 
        message_id: int, 
        emoji: "Emoji"
    ) -> None:
        await self.client.http.request(
            Route(f'/channels/{channel_id}/messages/{message_id}/reactions/{emoji.name}:{emoji.id}/@me', 'PUT')
        )

    async def channel_message_reaction_delete_emoji(
        self, 
        channel_id: int, 
        message_id: int, 
        emoji: "Emoji"
    ) -> None:
        await self.client.http.request(
            Route(f'/channels/{channel_id}/messages/{message_id}/reactions/{emoji.name}:{emoji.id}/@me', 'DELETE')
        )

    async def channel_message_reaction_user_delete_emoji(
        self, 
        channel_id: int, 
        message_id: int, 
        user_id: int,
        emoji: "Emoji"
    ) -> None:
        await self.client.http.request(
            Route(f'/channels/{channel_id}/messages/{message_id}/reactions/{emoji.name}:{emoji.id}/{user_id}', 'DELETE')
        )

    async def channel_permissions_modfiy(
        self,
        channel_id: int, 
        overwrite_id: int, 
        allow: int, 
        deny: int, 
        type: str,
        reason: str=None,
    ) -> None:
        await self.client.http.request(
            Route(f'/channels/{channel_id}/permissions/{overwrite_id}', 'PUT'),
            json={
                'allow': allow,
                'deny': deny,
                'type': type,
            },
            headears=_reason(reason)
        )

    async def channel_permissions_delete(
        self,
        channel_id: int, 
        overwrite_id: int, 
        reason: str=None,
    ) -> None:
        await self.client.http.request(
            Route(f'/channels/{channel_id}/permissions/{overwrite_id}', 'DELETE'),
            headears=_reason(reason)
        )
    
    async def channel_invites_list(
        self, 
        channel_id: int, 
        limit: int=100
    ) -> typing.List["Invite"]:
        r = await self.client.http.request(
            Route(f'/channels/{channel_id}/invites', 'GET'),
            params={'limit': limit}
        )
        return [Invite(self.client, i) for i in r]

    async def channel_invite_create(
        self, 
        channel_id: int, 
        max_age: int=0, 
        max_uses: int=0, 
        temporary: bool=False, 
        unique: bool=False, 
        reason: str=None
    ) -> "Invite":
        r = await self.client.http.request(
            Route(f'/channels/{channel_id}/invites', 'POST'),
            json={
                'max_age': max_age,
                'max_uses': max_uses,
                'temporary': temporary,
                'unique': unique,
            },
            headears=_reason(reason)
        )
        return Invite(self.client, r)

    async def channel_invite_delete(
        self, 
        channel_id: int, 
        code: str, 
        reason: str=None
    ) -> None:
        await self.client.http.request(
            Route(f'/channels/{channel_id}/invites/{code}', 'DELETE'),
            headears=_reason(reason)
        )

    async def channel_pins_list(
        self, 
        channel_id: int, 
        limit: int=100
    ) -> typing.List["Message"]:
        r = await self.client.http.request(
            Route(f'/channels/{channel_id}/pins', 'GET'),
            params={'limit': limit}
        )
        return [Message(self.client, m) for m in r]

    async def channel_pins_add(
        self, 
        channel_id: int, 
        message_id: int, 
        reason: str=None
    ) -> None:
        await self.client.http.request(
            Route(f'/channels/{channel_id}/pins/{message_id}', 'PUT'),
            headears=_reason(reason)
        )

    async def channel_pins_remove(
        self, 
        channel_id: int, 
        message_id: int, 
        reason: str=None
    ) -> None:
        await self.client.http.request(
            Route(f'/channels/{channel_id}/pins/{message_id}', 'DELETE'),
            headears=_reason(reason)
        )

    async def channel_webhook_list(
        self, 
        channel_id: int, 
        limit: int=100
    ) -> typing.List["Webhook"]:
        r = await self.client.http.request(
            Route(f'/channels/{channel_id}/webhooks', 'GET'),
            params={'limit': limit}
        )
        return [Webhook(self.client, w) for w in r]

    async def channel_webhook_create(
        self, 
        channel_id: int, 
        name: str, 
        avatar: str=None, 
        reason: str=None
    ) -> "Webhook":
        r = await self.client.http.request(
            Route(f'/channels/{channel_id}/webhooks', 'POST'),
            json={
                'name': name,
                'avatar': avatar,
            },
            headears=_reason(reason)
        )
        return Webhook(self.client, r)

    async def channel_webhook_delete(
        self, 
        channel_id: int, 
        webhook_id: int, 
        reason: str=None
    ) -> None:
        await self.client.http.request(
            Route(f'/channels/{channel_id}/webhooks/{webhook_id}', 'DELETE'),
            headears=_reason(reason)
        )

    async def channel_webhook_get(
        self, 
        channel_id: int, 
        webhook_id: int
    ) -> "Webhook":
        r = await self.client.http.request(
            Route(f'/channels/{channel_id}/webhooks/{webhook_id}', 'GET')
        )
        return Webhook(self.client, r)
    
    async def guild_get(
        self, 
        guild_id: int
    ) -> "Guild":
        r = await self.client.http.request(
            Route(f'/guilds/{guild_id}', 'GET')
        )
        return Guild(self.client, r)

    async def guild_modfiy(
        self, 
        guild_id: int, 
        name: str=None, 
        region: str=None, 
        icon: str=None, 
        owner_id: int=None, 
        afk_channel_id: int=None, 
        afk_timeout: int=None, 
        verification_level: int=None, 
        default_message_notifications: int=None, 
        explicit_content_filter: int=None, 
        reason: str=None
    ) -> None:
        await self.client.http.request(
            Route(f'/guilds/{guild_id}', 'PATCH'),
            json={
                'name': name,
                'region': region,
                'icon': icon,
                'owner_id': owner_id,
                'afk_channel_id': afk_channel_id,
                'afk_timeout': afk_timeout,
                'verification_level': verification_level,
                'default_message_notifications': default_message_notifications,
                'explicit_content_filter': explicit_content_filter,
            },
            headears=_reason(reason)
        )

    async def guild_delete(
        self, 
        guild_id: int, 
        reason: str=None
    ) -> None:
        await self.client.http.request(
            Route(f'/guilds/{guild_id}', 'DELETE'),
            headears=_reason(reason)
        )

    async def guild_channels_list(
        self, 
        guild_id: int, 
        limit: int=100
    ) -> typing.List["ChannelsTypes"]:
        r = await self.client.http.request(
            Route(f'/guilds/{guild_id}/channels', 'GET'),
            params={'limit': limit}
        )
        return [deserialize_channel(self.client, c) for c in r]

    async def guild_create_channel(
        self, 
        guild_id: int, 
        name: str, 
        type: int,
        bitrate: int = None,
        user_limit: int = None,
        permission_overwrites: list = [],
        nfsw: bool = False,
        category_id: int = None,
        position: int =None,
        reason: str = None
    ) -> "ChannelsTypes":
        r = await self.client.http.request(
            Route(f'/guilds/{guild_id}/channels', 'POST'),
            json={
                'name': name,
                'type': type,
                'bitrate': bitrate,
                'user_limit': user_limit,
                'permission_overwrites': permission_overwrites,
                'nsfw': nfsw,
                'category_id': category_id,
                'position': position,
            },
            headears=_reason(reason)
        )
        return deserialize_channel(self.client, r)

    async def guild_create_role(
        self, 
        guild_id: int, 
        name: str, 
        permissions: int, 
        color: int, 
        hoist: bool, 
        mentionable: bool, 
        reason: str=None
    ) -> "Role":
        r = await self.client.http.request(
            Route(f'/guilds/{guild_id}/roles', 'POST'),
            json={
                'name': name,
                'permissions': permissions,
                'color': color,
                'hoist': hoist,
                'mentionable': mentionable,
            },
            headears=_reason(reason)
        )
        return Role(self.client, r)

    async def guild_roles_list(
        self, 
        guild_id: int
    ) -> typing.List["Role"]:
        r = await self.client.http.request(
            Route(f'/guilds/{guild_id}/roles', 'GET')
        )
        return [Role(self.client, r) for r in r]

    async def guild_role_modify(
        self, 
        guild_id: int, 
        role_id: int, 
        name: str=None, 
        permissions: int=None, 
        color: int=None, 
        hoist: bool=None, 
        mentionable: bool=None, 
        reason: str=None
    ) -> "Role":
        await self.client.http.request(
            Route(f'/guilds/{guild_id}/roles/{role_id}', 'PATCH'),
            json={
                'name': name,
                'permissions': permissions,
                'color': color,
                'hoist': hoist,
                'mentionable': mentionable,
            },
            headears=_reason(reason)
        )
        return Role(self.client, {'id': role_id})

    async def guild_delete_role(
        self, 
        guild_id: int, 
        role_id: int, 
        reason: str=None
    ) -> None:
        await self.client.http.request(
            Route(f'/guilds/{guild_id}/roles/{role_id}', 'DELETE'),
            headears=_reason(reason)
        )

    async def guild_prune_members(
        self, 
        guild_id: int, 
        days: int, 
        reason: str=None
    ) -> int:
        r = await self.client.http.request(
            Route(f'/guilds/{guild_id}/prune', 'POST'),
            json={
                'days': days,
            },
            headears=_reason(reason)
        )
        return r['pruned']

    async def guild_members_list(
        self, 
        guild_id: int, 
        limit: int=100, 
        after: int=None
    ) -> typing.List["Member"]:
        r = await self.client.http.request(
            Route(f'/guilds/{guild_id}/members', 'GET'),
            params={
                'limit': limit,
                'after': after
            }
        )
        return [Member(self.client, m) for m in r]

    async def guild_members_modfiy(
        self, 
        guild_id: int, 
        user_id: int, 
        nick: str=None, 
        roles: list=None, 
        reason: str=None
    ) -> "Member":
        r = await self.client.http.request(
            Route(f'/guilds/{guild_id}/members/{user_id}', 'PATCH'),
            json={
                'nick': nick,
                'roles': roles,
            },
            headears=_reason(reason)
        )
        return Member(self.client, r)

    async def guild_members_add_role(
        self, 
        guild_id: int, 
        user_id: int, 
        role_id: int, 
        reason: str=None
    ) -> None:
        await self.client.http.request(
            Route(f'/guilds/{guild_id}/members/{user_id}/roles/{role_id}', 'PUT'),
            headears=_reason(reason)
        )

    async def guild_members_remove_role(
        self, 
        guild_id: int, 
        user_id: int, 
        role_id: int, 
        reason: str=None
    ) -> None:
        await self.client.http.request(
            Route(f'/guilds/{guild_id}/members/{user_id}/roles/{role_id}', 'DELETE'),
            headears=_reason(reason)
        )

    async def guild_members_kick(
        self, 
        guild_id: int, 
        user_id: int, 
        reason: str=None
    ) -> None:
        await self.client.http.request(
            Route(f'/guilds/{guild_id}/members/{user_id}', 'DELETE'),
            headears=_reason(reason)
        )

    async def guild_members_ban(
        self, 
        guild_id: int, 
        user_id: int, 
        delete_message_days: int=1, 
        reason: str=None
    ) -> None:
        await self.client.http.request(
            Route(f'/guilds/{guild_id}/bans/{user_id}', 'PUT'),
            json={
                'delete-message-days': delete_message_days,
            },
            headears=_reason(reason)
        )

    async def guild_members_unban(
        self, 
        guild_id: int, 
        user_id: int, 
        reason: str=None
    ) -> None:
        await self.client.http.request(
            Route(f'/guilds/{guild_id}/bans/{user_id}', 'DELETE'),
            headears=_reason(reason)
        )

    async def guild_members_voice_state(
        self, 
        guild_id: int, 
        user_id: int, 
        channel_id: int=None, 
        mute: bool=None, 
        deaf: bool=None, 
        reason: str=None
    ) -> None:
        await self.client.http.request(
            Route(f'/guilds/{guild_id}/members/{user_id}', 'PATCH'),
            json={
                'channel_id': channel_id,
                'mute': mute,
                'deaf': deaf,
            },
            headears=_reason(reason)
        )

    async def guild_bans_list(
        self, 
        guild_id: int
    ) -> typing.List[tuple]:
        r = await self.client.http.request(
            Route(f'/guilds/{guild_id}/bans', 'GET')
        )
        return [(User(b['user']),b['reason']) for b in r]

    async def guild_invites_list(
        self, 
        guild_id: int
    ) -> typing.List["Invite"]:
        r = await self.client.http.request(
            Route(f'/guilds/{guild_id}/invites', 'GET')
        )
        return [Invite(self.client, i) for i in r]

    async def guild_webhooks_list(
        self, 
        guild_id: int
    ) -> typing.List["Webhook"]:
        r = await self.client.http.request(
            Route(f'/guilds/{guild_id}/webhooks', 'GET')
        )
        return [Webhook(self.client, w) for w in r]

    async def guild_emojis_list(
        self, 
        guild_id: int
    ) -> typing.List["Emoji"]:
        r = await self.client.http.request(
            Route(f'/guilds/{guild_id}/emojis', 'GET')
        )
        return [Emoji(self.client, e) for e in r]

    async def guild_emojis_create(
        self, 
        guild_id: int, 
        name: str, 
        image: str, 
        reason: str=None
    ) -> "Emoji":
        r = await self.client.http.request(
            Route(f'/guilds/{guild_id}/emojis', 'POST'),
            json={
                'name': name,
                'image': image,
            },
            headears=_reason(reason)
        )
        return Emoji(self.client, r)
    
    async def guild_emojis_delete(
        self, 
        guild_id: int, 
        emoji_id: int, 
        reason: str=None
    ) -> None:
        await self.client.http.request(
            Route(f'/guilds/{guild_id}/emojis/{emoji_id}', 'DELETE'),
            headears=_reason(reason)
        )
        
    async def guild_emojis_modfiy(
        self, 
        guild_id: int, 
        emoji_id: int, 
        name: str, 
        reason: str=None
    ) -> "Emoji":
        r = await self.client.http.request(
            Route(f'/guilds/{guild_id}/emojis/{emoji_id}', 'PATCH'),
            json={
                'name': name,
            },
            headears=_reason(reason)
        )
        return Emoji(self.client, r)

    async def guild_sticker_list(
        self, 
        guild_id: int
    ) -> typing.List["Sticker"]:
        r = await self.client.http.request(
            Route(f'/guilds/{guild_id}/stickers', 'GET')
        )
        return [Sticker(self.client, s) for s in r]

    async def guild_sticker_create(
        self, 
        guild_id: int, 
        name: str, 
        image: str, 
        reason: str=None
    ) -> "Sticker":
        r = await self.client.http.request(
            Route(f'/guilds/{guild_id}/stickers', 'POST'),
            json={
                'name': name,
                'image': image,
            },
            headears=_reason(reason)
        )
        return Sticker(self.client, r)

    async def guild_sticker_delete(
        self, 
        guild_id: int, 
        sticker_id: int, 
        reason: str=None
    ) -> None:
        await self.client.http.request(
            Route(f'/guilds/{guild_id}/stickers/{sticker_id}', 'DELETE'),
            headears=_reason(reason)
        )
    
    async def guild_sticker_modify(
        self, 
        guild_id: int, 
        sticker_id: int, 
        name: str, 
        reason: str=None
    ) -> "Sticker":
        r = await self.client.http.request(
            Route(f'/guilds/{guild_id}/stickers/{sticker_id}', 'PATCH'),
            json={
                'name': name,
            },
            headears=_reason(reason)
        )
        return Sticker(self.client, r)
    
    # async def guild_audit_logs(
    #     self, 
    #     guild_id: int, 
    #     limit: int=100, 
    #     before: int=None, 
    #     after: int=None
    # ) -> typing.List["AuditLogEntry"]:
    #     r = await self.client.http.request(
    #         Route(f'/guilds/{guild_id}/audit-logs', 'GET'),
    #         params={
    #             'limit': limit,
    #             'before': before,
    #             'after': after,
    #         }
    #     )
    #     return [AuditLogEntry(self.client, a) for a in r]

    async def user_me(self) -> "User":
        r = await self.client.http.request(
            Route('/users/@me', 'GET')
        )
        return User(self.client, r)
    
    async def user_patch_me(
        self, 
        username: str, 
        avatar: str, 
        reason: str=None
    ) -> "User":
        r = await self.client.http.request(
            Route('/users/@me', 'PATCH'),
            json={
                'username': username,
                'avatar': avatar,
            },
            headears=_reason(reason)
        )
        return User(self.client, r)
    
    async def user_guild_delete_me(
        self, 
        guild_id: int, 
        reason: str=None
    ) -> None:
        await self.client.http.request(
            Route(f'/users/@me/guilds/{guild_id}', 'DELETE'),
            headears=_reason(reason)
        )
    
    async def user_dm_create(
        self, 
        recipient_id: int, 
        content: str, 
        tts: bool=False, 
        reason: str=None
    ) -> "Message":
        r = await self.client.http.request(
            Route('/users/@me/channels', 'POST'),
            json={
                'recipient_id': recipient_id,
                'type': 'dm',
                'tts': tts,
                'content': content,
            },
            headears=_reason(reason)
        )
        return Message(self.client, r)

    async def invites_get(
        self, 
        guild_id: int
    ) -> typing.List["Invite"]:
        r = await self.client.http.request(
            Route(f'/guilds/{guild_id}/invites', 'GET')
        )
        return [Invite(self.client, i) for i in r]

    async def invites_delete(
        self, 
        guild_id: int, 
        code: str, 
        reason: str=None
    ) -> None:
        await self.client.http.request(
            Route(f'/guilds/{guild_id}/invites/{code}', 'DELETE'),
            headears=_reason(reason)
        )