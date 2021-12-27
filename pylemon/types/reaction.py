r"""
    :copyright: (c) 2021 by Zaid Ali (email@xarty.xyz) / Hazem Meqdad(hazemmeqdad@gmail.com).
    :license: MIT, see LICENSE for more details.
"""

import typing
import dataclasses

if typing.TYPE_CHECKING:
    from pylemon.client import BaseClient

from pylemon.types import Emoji

@dataclasses.dataclass(init=True)
class Reaction:
    def __init__(
        self,
        client: "BaseClient",
        data: typing.Dict[str, typing.Union[str,dict,list,int,float,bool]],
    ) -> None:
        self.client = client

        self.guild_id: int = (int(data.get('guild_id')) 
            if data.get('guild_id') else None)
        self.channel_id = (int(data.get('channel_id')) 
            if data.get('channel_id') else None)
        self.message_id = (int(data.get('message_id')) 
            if data.get('message_id') else None)
        self.user_id = (int(data.get('user_id')) 
            if data.get('user_id') else None)
        self.emoji = Emoji(
            self.client,
            self.guild_id,
            (data.get('emoji') if data.get('emoji') else data)
        )
