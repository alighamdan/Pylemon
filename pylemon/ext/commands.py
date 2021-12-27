r"""
    :copyright: (c) 2021 by Zaid Ali (email@xarty.xyz) / Hazem Meqdad(hazemmeqdad@gmail.com).
    :license: MIT, see LICENSE for more details.
"""
import typing

def has_permission(permission: typing.List[str]) -> typing.Callable:
    def deco(func: typing.Callable):
        func.required_permission = permission
        return func
    return deco

def before_command(before: typing.Awaitable):
    def deco(func: typing.Awaitable):
        func.before_command = before
        return func
    return deco