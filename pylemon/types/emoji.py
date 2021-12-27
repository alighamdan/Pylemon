r"""
    :copyright: (c) 2021 by Zaid Ali (email@xarty.xyz) / Hazem Meqdad(hazemmeqdad@gmail.com).
    :license: MIT, see LICENSE for more details.
"""

import typing
import dataclasses

if typing.TYPE_CHECKING:
    from pylemon.client import BaseClient

@dataclasses.dataclass(init=True)
class Emoji:
    """
        This is the Emoji class that is used to simplify the usage of the emoji object.
        It is used to simplify the usage of the emoji object by providing a more readable interface.

        Attributes
        ----------
        id : int
            The emoji id.
        name : str
            The name of the emoji.
        roles : list
            The roles of the emoji.
        available : bool
            Whether the emoji is available.
        animated : bool
            Whether the emoji is animated.
    """
    def __init__(
        self,
        client: "BaseClient",
        guild_id: int,
        data: typing.Dict[str, typing.Union[str,dict,list,int,float,bool]]
    ) -> None:
        self.client = client
        
        self.guild_id: int = guild_id
        self.id: int = data.get('id')
        self.name: str = data.get('name')
        self.roles: typing.Union[list,None] = data.get('roles')
        self.available: bool = data.get('available',None)
        self.animated: bool = data.get('animated',None)

    async def update(self,name: str, reason: str=None) -> "Emoji":
        """
            Updates the emoji object.

            Parameters
            ----------
            name : str
                The new name of the emoji.
            reason : str
                The reason of the update.
        """
        return await self.client.api.guild_emojis_modfiy(
            self.guild_id,
            self.id,
            name=name,
            reason=reason
        )

    async def delete(self,reason: str=None) -> "Emoji":
        """
            Deletes the emoji object.

            Parameters
            ----------
            reason : str
                The reason of the deletion.
        """
        return await self.client.api.guild_emojis_delete(
            self.guild_id,
            self.id,
            reason=reason
        )