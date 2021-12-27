r"""
    :copyright: (c) 2021 by Zaid Ali (email@xarty.xyz) / Hazem Meqdad(hazemmeqdad@gmail.com).
    :license: MIT, see LICENSE for more details.
"""

import typing
import aiohttp
import asyncio

if typing.TYPE_CHECKING:
    from pylemon.client import BaseClient

class Route:
    def __init__(
        self,
        url: str,
        method: str,
    ) -> None:
        self.url =  f'https://discord.com/api/v9{url}'
        self.method = method

class HTTP:
    def __init__(
        self,
        client: "BaseClient",
    ) -> None:
        self.client = client
        self.session = aiohttp.ClientSession(loop=self.client.loop)
        self.headers = {
            'Authorization': self.client.token,
        }

    async def request(
        self,
        route: Route,
        **kwargs,
    ) -> typing.Any:
        if 'headers' in kwargs and kwargs['headers']:
            for k, v in kwargs['headers'].items():
                self.headers[k] = v

        async with self.session.request(
            url=route.url,
            method=route.method,
            headers=self.headers,
            **kwargs,
        ) as response:
            if response.status == 429:
                await self.ratelimit(response.headers['Retry-After'])
            return await response.json()

    async def ratelimit(
        self,
        retry_after: float,
        route: Route,
        *,
        params: typing.Optional[typing.Dict[str, str]] = {},
        data: typing.Optional[typing.Dict[str, str]] = {},
        json: typing.Optional[typing.Dict[str, str]] = {},
    ):
        await asyncio.sleep(retry_after if type(retry_after) == float else float(retry_after))
        return await self.request(
            route,
            params=params,
            data=data,
            json=json,
        )



    