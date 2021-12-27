r"""
    :copyright: (c) 2021 by Zaid Ali (email@xarty.xyz) / Hazem Meqdad(hazemmeqdad@gmail.com).
    :license: MIT, see LICENSE for more details.
"""

import typing
import dataclasses

if typing.TYPE_CHECKING:
    from pylemon.client import BaseClient

@dataclasses.dataclass(init=True)
class Webhook:
    """
        This is the webhook object. It is used to interact with webhooks.
        
        Attributes
        ----------
        code : str
            The code of the webhook.
    """
    def __init__(
        self,
        client: "BaseClient",
        data: typing.Dict[str, typing.Union[str,dict,list,int,float,bool]]
    ) -> None:
        self.client = client

        self.code: str = data.get('code')