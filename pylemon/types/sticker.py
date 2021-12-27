r"""
    :copyright: (c) 2021 by Zaid Ali (email@xarty.xyz) / Hazem Meqdad(hazemmeqdad@gmail.com).
    :license: MIT, see LICENSE for more details.
"""

import typing
import dataclasses

if typing.TYPE_CHECKING:
    from pylemon.client import BaseClient

@dataclasses.dataclass(init=True)
class Sticker:
    def __init__(
        self,
        client: "BaseClient",
        guild_id: int,
        data: typing.Dict[str, typing.Union[str,dict,list,int,float,bool]]
        ) -> None:
        self.client = client

        self.guild_id: int = guild_id
        self.id = data.get('id',None)
        self.pack_id = data.get('pack_id',None)
        self.name = data.get('name',None)
        self.description = data.get('description',None)
        self.tags = data.get('tags',None)
        self.type = data.get('type',None)
        self.format_type = data.get('format_type',None)
        self.available = data.get('available',None)
        self.user = data.get('user',None)
        self.sort_value = data.get('sort_value')

    async def edit(self, name: str, reason:str=None) -> None:
        """
        Edit the sticker.

        Parameters
        ----------
        name: str
            The new name of the sticker.
        description: str
            The new description of the sticker.
        tags: list
            The new tags of the sticker.
        """
        await self.client.api.guild_sticker_modify(
            self.guild_id,
            self.id,
            name,
            reason
        )

    async def delete(self, reason:str=None) -> None:
        """
        Delete the sticker.

        Parameters
        ----------
        reason: str
            The reason for deleting the sticker.
        """
        await self.client.api.guild_sticker_delete(
            self.guild_id,
            self.id,
            reason
        )
        