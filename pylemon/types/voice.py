r"""
    :copyright: (c) 2021 by Zaid Ali (email@xarty.xyz) / Hazem Meqdad(hazemmeqdad@gmail.com).
    :license: MIT, see LICENSE for more details.
"""

import typing
import dataclasses

if typing.TYPE_CHECKING:
    from pylemon.client import BaseClient

from .types import snowflake

@dataclasses.dataclass(init=True)
class VoiceState:
    def __init__(
        self,
        client: "BaseClient",
        guild_id: int,
        data: typing.Dict[str, typing.Union[str,dict,list,int,float,bool]],
    ) -> None:
        self.client = client

        self.guild_id: int = snowflake(guild_id)
        self.channel_id = snowflake(data.get('channel_id',None))
        self.user_id = snowflake(data.get('user_id',None))

        self.session_id: int = data.get('session_id',None)
        self.deaf: bool = data.get('deaf',None)
        self.mute: bool = data.get('mute',None)
        self.self_deaf: bool = data.get('self_deaf',None)
        self.self_mute: bool = data.get('self_mute',None)
        self.suppress: bool = data.get('suppress',None)
        self.self_stream: bool = data.get('self_stream',None)
        self.self_video: bool = data.get('self_video',None)
        self.stream: bool = data.get('stream',None)
        self.video: bool = data.get('video',None)

@dataclasses.dataclass(init=True)
class VoiceServer:
    def __init__(
        self,
        client: "BaseClient",
        data: typing.Dict[str, typing.Union[str,dict,list,int,float,bool]],
    ) -> None:
        self.client = client

        self.endpoint: str = data.get('endpoint')
        self.token: str = data.get('token')
        self.guild_id: int = snowflake(data.get('guild_id'))