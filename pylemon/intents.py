r"""
    :copyright: (c) 2021 by Zaid Ali (email@xarty.xyz) / Hazem Meqdad(hazemmeqdad@gmail.com).
    :license: MIT, see LICENSE for more details.
"""

class Intents:
    GUILDS: int = 1 << 0
    GUILD_MEMBERS: int = 1 << 1
    GUILD_BANS: int = 1 << 2
    GUILD_EMOJIS_AND_STICKERS: int = 1 << 3
    GUILD_INTEGRATIONS: int = 1 << 4
    GUILD_WEBHOOKS: int = 1 << 5
    GUILD_INVITES: int = 1 << 6
    GUILD_VOICE_STATES: int = 1 << 7
    GUILD_PRESENCES: int = 1 << 8
    GUILD_MESSAGES: int = 1 << 9
    GUILD_MESSAGE_REACTIONS: int = 1 << 10
    GUILD_MESSAGE_TYPING: int = 1 << 11
    DIRECT_MESSAGES: int = 1 << 12
    DIRECT_MESSAGE_REACTIONS: int = 1 << 13
    DIRECT_MESSAGE_TYPING: int = 1 << 14

    def all():
        return sum([
            Intents.GUILDS,
            Intents.GUILD_MEMBERS,
            Intents.GUILD_BANS,
            Intents.GUILD_EMOJIS_AND_STICKERS,
            Intents.GUILD_INTEGRATIONS,
            Intents.GUILD_WEBHOOKS,
            Intents.GUILD_INVITES,
            Intents.GUILD_VOICE_STATES,
            Intents.GUILD_PRESENCES,
            Intents.GUILD_MESSAGES,
            Intents.GUILD_MESSAGE_REACTIONS,
            Intents.GUILD_MESSAGE_TYPING,
            Intents.DIRECT_MESSAGES,
            Intents.DIRECT_MESSAGE_REACTIONS,
            Intents.DIRECT_MESSAGE_TYPING,
        ])