r"""
    :copyright: (c) 2021 by Zaid Ali (email@xarty.xyz) / Hazem Meqdad(hazemmeqdad@gmail.com).
    :license: MIT, see LICENSE for more details.
"""

import typing
import dataclasses

if typing.TYPE_CHECKING:
    from pylemon.client import BaseClient
    from pylemon.types import (
        Guild,
        Role,
    )

from .user import User

@dataclasses.dataclass(init=True)
class Member(User):
    """
        This is the Member class that is used to simplify the usage of the member object.
        It is used to simplify the usage of the member object by providing a more readable interface.

        Attributes
        ----------
        guild_id : int
            The guild id.
        nick : str
            The nick of the member.
        roles : list
            The roles of the member.
        joined_at : str
            The joined at of the member.
        premium_since : str
            The premium since of the member.
    """
    def __init__(
        self,
        client: "BaseClient",
        guild_id: int,
        user: typing.Dict[str, typing.Union[str,dict,list,int,float,bool]],
        data: typing.Dict[str, typing.Union[str,dict,list,int,float,bool]],
    ) -> None:
        self.client = client

        self.guild_id: int = guild_id
        self.nick: typing.Union[str,None] = data.get('nick')
        self.roles_id: typing.Union[list,None] = data.get('roles')
        self.joined_at: typing.Union[str,None] = data.get('joined_at')
        self.premium_since: typing.Union[str,None] = data.get('premium_since')

        super().__init__(client, user)

    @property
    def guild(self) -> "Guild":
        """
            This is the guild of the member.
            Returns
            -------
            Guild
                The guild of the member.
        """
        return self.client.get_guild(self.guild_id)

    @property
    def roles(self) -> typing.Union[typing.List["Role"],None]:
        """
            This is a property that returns the roles of the member.
        """
        if self.roles_id:
            return [role for role in self.guild.roles if str(role.id) in self.roles_id]

    @property
    def highest_role(self) -> typing.Union["Role",None]:
        """
            This is a property that returns the highest role of the member.
        """
        if self.roles:
            return max(self.roles, key=lambda x: x.position and x.name != "@everyone")

    @property
    def permissions(self) -> typing.Union[str,None]:
        """
            This is a property that returns the permissions of the member.
        """
        permissions = []
        for role in self.roles:
            for permission in role.permissions:
                if permission not in permissions:
                    permissions.append(permission)
        return permissions

    async def kick(self,reason: str=None) -> None:
        """
            Kicks the member from the guild.

            Parameters
            ----------
            reason : str
                The reason of the kick.
        """
        await self.client.api.guild_members_kick(
            self.guild_id,
            self.id,
            reason=reason
        )

    async def ban(self,reason: str=None) -> None:
        """
            Bans the member from the guild.

            Parameters
            ----------
            reason : str
                The reason of the ban.
        """
        await self.client.api.guild_members_ban(
            self.guild_id,
            self.id,
            reason=reason
        )

    async def unban(self,reason: str=None) -> None:
        """
            Unbans the member from the guild.

            Parameters
            ----------
            reason : str
                The reason of the unban.
        """
        await self.client.api.guild_members_unban(
            self.guild_id,
            self.id,
            reason=reason
        )

    async def edit(self,nick: str=None,roles: typing.List[int]=None,reason: str=None) -> None:
        """
            Edits the member.

            Parameters
            ----------
            nick : str
                The nick of the member.
            roles : list
                The roles of the member.
        """
        await self.client.api.guild_members_modfiy(
            self.guild_id,
            self.id,
            nick=nick,
            roles=[str(role.id) for role in roles],
            reason=reason
        )

    async def add_role(self,role: "Role",reason: str=None) -> None:
        """
            Adds a role to the member.

            Parameters
            ----------
            role : Role
                The role to add.
            reason : str
                The reason of the add.
        """
        await self.client.api.guild_members_add_role(
            self.guild_id,
            self.id,
            role.id,
            reason=reason
        )

    async def remove_role(self,role: "Role",reason: str=None) -> None:
        """
            Removes a role from the member.

            Parameters
            ----------
            role : Role
                The role to remove.
            reason : str
                The reason of the remove.
        """
        await self.client.api.guild_members_remove_role(
            self.guild_id,
            self.id,
            role.id,
            reason=reason
        )

    async def mute(self,reason: str=None) -> None:
        """
            Mutes the member.

            Parameters
            ----------
            reason : str
                The reason of the mute.
        """
        await self.client.api.guild_members_voice_state(
            self.guild_id,
            self.id,
            reason=reason
        )


    def __str__(self) -> str:
        """
            This is the string representation of the member object.
            Returns
            -------
            str
                The string representation of the member object.
        """
        return f'<Member {self.id}>'

