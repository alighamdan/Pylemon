r"""
    :copyright: (c) 2021 by Zaid Ali (email@xarty.xyz) / Hazem Meqdad(hazemmeqdad@gmail.com).
    :license: MIT, see LICENSE for more details.
"""

import typing


class Permission:
    def __init__(self, bit: str) -> None:
        self.bit: int = int(bit)
        self.permissions: dict = {
            "CREATE_INSTANT_INVITE": 1 << 0,
            "KICK_MEMBERS": 1 << 1,
            "BAN_MEMBERS": 1 << 2,
            "ADMINISTRATOR": 1 << 3,
            "MANAGE_CHANNELS": 1 << 4,
            "MANAGE_GUILD": 1 << 5,
            "ADD_REACTIONS": 1 << 6,
            "VIEW_AUDIT_LOG": 1 << 7,
            "VIEW_CHANNEL": 1 << 10,
            "SEND_MESSAGES": 1 << 11,
            "SEND_TTS_MESSAGES": 1 << 12,
            "MANAGE_MESSAGES": 1 << 13,
            "EMBED_LINKS": 1 << 14,
            "ATTACH_FILES": 1 << 15,
            "READ_MESSAGE_HISTORY": 1 << 16,
            "MENTION_EVERYONE": 1 << 17,
            "USE_EXTERNAL_EMOJIS": 1 << 18,
            "CONNECT": 1 << 20,
            "SPEAK": 1 << 21,
            "MUTE_MEMBERS": 1 << 22,
            "DEAFEN_MEMBERS": 1 << 23,
            "MOVE_MEMBERS": 1 << 24,
            "USE_VAD": 1 << 25,
            "CHANGE_NICKNAME": 1 << 26,
            "MANAGE_NICKNAMES": 1 << 27,
            "MANAGE_ROLES": 1 << 28,
            "MANAGE_WEBHOOKS": 1 << 29,
            "MANAGE_EMOJIS": 1 << 30,
        }
    
    def has_permission(self, perm: str) -> bool:
        if perm in self.perms:
            return self.bit & self.permissions[perm] == self.permissions[perm]

    def compute_permissions(self) -> typing.List[str]:
        result = []
        for key, val in self.permissions.items():
            if val & self.bit == val:
                result.append(key)
        return result