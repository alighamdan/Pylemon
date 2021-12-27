r"""
    :copyright: (c) 2021 by Zaid Ali (email@xarty.xyz) / Hazem Meqdad(hazemmeqdad@gmail.com).
    :license: MIT, see LICENSE for more details.
"""

import typing
import dataclasses

if typing.TYPE_CHECKING:
    from pylemon.client import BaseClient

@dataclasses.dataclass(init=True)
class User:
    r"""
        The User class is a wrapper around the user object.
        It is used to simplify the usage of the user object by providing a more readable interface.

        Parameters
        ----------
        client : BaseClient
            The client that the user is from.
        data : dict
            The user data.

        Attributes
        ----------
        id : int
            The user id.
        username : str
            The username of the user.
        discriminator : str
            The discriminator of the user.
        avatar : str
            The avatar of the user.
        banner : str
            The banner of the user.
        banner_color : str
            The banner color of the user.
        accent_color : int
            The accent color of the user.
        bot : bool
            Whether the user is a bot.
        system : bool
            Whether the user is a system user.
        mfa_enabled : bool
            Whether the user has MFA enabled.
        locale : str
            The locale of the user.
        verified : bool
            Whether the user is verified.
        premium_type : int
            The premium type of the user.
        public_flags : int
            The public flags of the user.
        flags : list
            The list of flags the user has.

        Methods
        -------
        has_flag : bool
            Checks if the user has the specified flag.
    """
    def __init__(
        self,
        client: "BaseClient",
        data: typing.Dict[str, typing.Union[str,dict,list,int,float,bool]],
    ) -> None:
        self.client = client

        self.id: int = int(data.get("id"))
        self.username: str = data.get("username")
        self.discriminator: str = data.get("discriminator")
        self.avatar: typing.Union[str, None] = data.get("avatar")
        self.banner: typing.Union[str, None] = data.get("banner")
        self.banner_color: typing.Union[str, None] = data.get("banner_color")
        self.accent_color: typing.Union[int, None] = data.get("accent_color")
        self.bot: bool = data.get("bot", False)
        self.system: typing.Union[bool, None] = data.get("system")
        self.mfa_enabled: typing.Union[bool, None] = data.get("mfa_enabled")
        self.locale: typing.Union[str, None] = data.get("locale")
        self.verified: typing.Union[bool, None] = data.get("verified")
        self.premium_type: typing.Union[int, None] = data.get("premium_type")
        self.public_flags: typing.Union[int, None] = data.get("public_flags")


        self.flags_dict: typing.Dict[str,int] = {
            "DISCORD_EMPLOYEE": 1 << 0,
            "DISCORD_PARTNER": 1 << 1,
            "HYPESQUAD_EVENTS": 1 << 2,
            "BUGHUNTER_LEVEL_1": 1 << 3,
            "HOUSE_BRAVERY": 1 << 6,
            "HOUSE_BRILLIANCE": 1 << 7,
            "HOUSE_BALANCE": 1 << 8,
            "EARLY_SUPPORTER": 1 << 9,
            "TEAM_USER": 1 << 10,
            "SYSTEM": 1 << 12,
            "BUGHUNTER_LEVEL_2": 1 << 14,
            "VERIFIED_BOT": 1 << 16,
            "VERIFIED_DEVELOPER": 1 << 17,
            "DISCORD_CERTIFIED_MODERATOR": 1 << 18
        }
        
    def has_flag(self, flag: str) -> bool:
        """
            Checks if the user has the specified flag.

            Parameters
            ----------
            flag : str
                The flag to check.
        """
        if self.public_flags is None:
            return False

        return self.public_flags & self.flags_dict[flag] != 0

    @property
    def flags(self):
        """
            Returns a list of flags the user has.
        """
        if self.public_flags is None:
            return []

        return [
            flag for flag, value in self.flags_dict.items() if self.public_flags & value != 0
        ]
    