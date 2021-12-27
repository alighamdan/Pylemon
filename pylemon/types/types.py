r"""
    :copyright: (c) 2021 by Zaid Ali (email@xarty.xyz) / Hazem Meqdad(hazemmeqdad@gmail.com).
    :license: MIT, see LICENSE for more details.
"""


def snowflake(id: str) -> int:
    """
        Converts a string to a snowflake.
    """
    if id is None:
        return None
    if type(id) is int:
        return id
    return int(id if id.isdigit() else None)