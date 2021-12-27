r"""
    :copyright: (c) 2021 by Zaid Ali (email@xarty.xyz) / Hazem Meqdad(hazemmeqdad@gmail.com).
    :license: MIT, see LICENSE for more details.
"""

import typing
import dataclasses

if typing.TYPE_CHECKING:
    from pylemon.client import BaseClient
    from pylemon.types import Guild

from .permissions import Permission

@dataclasses.dataclass(init=True)
class Role:
    """
        This is the Role class that is used to simplify the usage of the role object.
        It is used to simplify the usage of the role object by providing a more readable interface.

        Attributes
        ----------
        id : int
            The role id.
        name : str
            The name of the role.
        color : str
            The color of the role.
        hoist : str
            Whether the role is hoisted.
        position : str
            The position of the role.
        permissions : str
            The permissions of the role.
        managed : bool
            Whether the role is managed.
        mentionable : str
            Whether the role is mentionable.
        created_at : str
            The created at of the role.
    """
    def __init__(
        self,
        client: "BaseClient",
        guild_id: int,
        data: typing.Dict[str, typing.Union[str,dict,list,int,float,bool]]
    ) -> None:
        self.client = client

        self.guild_id: int = guild_id
        self.id: int = int(data.get('id'))
        self.name: typing.Union[str,None] = data.get('name')
        self.color: typing.Union[str,None] = data.get('color')
        self.hoist: typing.Union[str,None] = data.get('hoist')
        self.position: typing.Union[str,None] = data.get('position')
        self.permissions: typing.Union[str,None] = Permission(data.get('permissions')).compute_permissions()
        self.managed: typing.Union[bool,None] = data.get('managed')
        self.mentionable: typing.Union[str,None] = data.get('mentionable')
        self.created_at: typing.Union[str,None] = data.get('created_at')

        

    @property
    def guild(self) -> "Guild":
        """
            Returns the guild of the role.
        """
        return self.client.get_guild(self.guild_id)
        
    def __repr__(self) -> str:
        return f'<Role id={self.id} name={self.name}>'