r"""
    :copyright: (c) 2021 by Zaid Ali (email@xarty.xyz) / Hazem Meqdad(hazemmeqdad@gmail.com).
    :license: MIT, see LICENSE for more details.
"""

import asyncio
import typing
import aiohttp
import zlib
import json

from pylemon.utils import deserialize_channel

if typing.TYPE_CHECKING:
    from pylemon.client import BaseClient

from pylemon.state import DataType, EventState
from pylemon.types import *

class Packets:
    Dispatch = 0
    Heartbeat = 1
    Identify = 2
    StatusUpdate = 3
    VoiceStateUpdate = 4
    VoiceServerPing = 5
    Resume = 6
    Reconnect = 7
    RequestGuildMembers = 8
    InvalidSession = 9
    Hello = 10
    HeartbeatACK = 11 

class Gateway:
    def __init__(
        self,
        client: "BaseClient",
    ) -> None:
        self.client = client
        self.loop = client.loop

        self.event = EventState(client)

        self.buffer = bytearray()
        self.inflator = zlib.decompressobj()

        self.gateway = "wss://gateway.discord.gg/?v=9&encoding=json&compress=zlib-stream"

        self.seq = 0
        self.session_id = None

    async def connect(self,reconnect: bool):
        self.reconnect = reconnect

        self.session = aiohttp.ClientSession(loop=self.loop)
        self.websocket = await self.session.ws_connect(self.gateway)

        await self.receiver()

    async def send(self, op: int, data: dict):
        await self.websocket.send_json({
            "op": op,
            "d": data
        })

    async def handle_ready(self, data: typing.Dict[str,typing.Any]):
        self.client.user = User(self.client, data["user"])
        self.client.unavailable_guilds = [int(guild['id']) for guild in data['guilds']]
        self.session_id = data['session_id']

        await self.client.emit('ready')

    async def receive(self, message: typing.Union[str,bytes]):
        if message['op'] == Packets.Hello:
            await self.identify(message['d']['heartbeat_interval'])

        elif message['op'] == Packets.Dispatch:
            if message['s'] > self.seq:
                self.seq = message['s']

            self.client.log.info(f"{message['t'].lower()} has been received")

            await self.dispatcher(message['t'].lower(), message['d'])

    async def dispatcher(self, event: str, data: typing.Dict[str,DataType]):
        if event in ("ready"):
            await self.handle_ready(data)
        elif event in ("message_create"):
            await self.client.emit(event, 
                Message(self.client, data))
        elif event in ("message_update"):
            before = self.client.get_message(data['id'])
            await self.client.emit(event, 
                before,Message(self.client, data))
        elif event in ("guild_create","guild_update"):
            await self.client.emit(event, 
                Guild(self.client, data))
        elif event in ("channel_create", "channel_update", "channel_delete", "thread_create", "thread_update"):
            await self.client.emit(event, 
                deserialize_channel(self.client, data.get('guild_id',None), data))
        elif event in ("guild_member_add"):
            guild = self.client.get_guild(data['guild_id'])
            await self.client.emit(event, 
                guild, Member(self.client,data['guild_id'],data['user'], data))
        elif event in ("guild_member_update"):
            guild = self.client.get_guild(data['guild_id'])
            before = guild.get_member(data['user']['id'])
            await self.client.emit(event, 
                guild, before, Member(self.client,data['guild_id'],data['user'], data))
        elif event in ("guild_role_create"):
            guild = self.client.get_guild(data['guild_id'])
            await self.client.emit(event, 
                guild,Role(self.client, data['guild_id'], data['role']))
        elif event in ("guild_role_update"):
            guild = self.client.get_guild(data['guild_id'])
            before = guild.get_role(data['role']['id'])
            await self.client.emit(event, 
                guild,before, Role(self.client, data['guild_id'], data['role']))
        elif event in ("guild_ban_add","guild_ban_remove"):
            guild = await self.client.get_guild(data['guild_id'])
            await self.client.emit(event, 
                guild, User(self.client, data['user']))
        elif event in ("voice_state_update"):
            guild = self.client.get_guild(data['guild_id'])
            await self.client.emit(event, 
                guild, VoiceServer(self.client, data))
        
        # Delete Events
        elif event in ("guild_delete"):
            guild = await self.client.get_guild(data['id'])
            await self.client.emit(event, 
                guild)
        elif event in ("channel_delete"):
            channel = await self.client.get_channel(data['id'])
            await self.client.emit(event, 
                channel)
        elif event in ("guild_member_remove"):
            guild = self.client.get_guild(data['guild_id'])
            member = guild.get_member(data['user']['id'])
            await self.client.emit(event, 
                guild, member)
        elif event in ("guild_role_delete"):
            guild = self.client.get_guild(data['guild_id'])
            role = guild.get_role(data['role_id'])
            await self.client.emit(event, 
                guild, role)
        elif event in ("message_reaction_add", "message_reaction_remove"):
            message = self.client.get_message(data['message_id'])
            await self.client.emit(event, 
                message, Reaction(self.client, data))
        else:
            await self.client.emit(event, data)
        
    async def receiver(self):
        async for msg in self.websocket:
            if msg.type == aiohttp.WSMsgType.BINARY or aiohttp.WSMsgType.TEXT:
                self.buffer.extend(msg.data)

                if len(msg.data) < 4 or msg.data[-4:] != b'\x00\x00\xff\xff':
                    return

                data = self.inflator.decompress(self.buffer)
                self.buffer.clear()

                json_data = json.loads(data.decode('utf-8'))

                await self.receive(json_data)

    async def identify(self, interval: float):
        await self.send(Packets.Identify, {
            "token": self.client.token,
            "properties": {
                "os": "linux",
                "browser": "Pylemon",
                "device": "Pylemon"
            },
            "intents": self.client.intents,
            "compress": True,
            "large_threshold": 250,
        })

        self.client.log.info(f"Identifying sent")

        asyncio.run_coroutine_threadsafe(
            self.heartbeat_task(interval/1000),self.loop
        )

    async def heartbeat_task(self, interval: float):
        while True:
            await self.send(1, self.seq)
            self.client.log.info(f"Sending heartbeat")
            await asyncio.sleep(interval)