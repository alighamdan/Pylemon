r"""
    :copyright: (c) 2021 by Zaid Ali (email@xarty.xyz) / Hazem Meqdad(hazemmeqdad@gmail.com).
    :license: MIT, see LICENSE for more details.
"""

import logging
import sys

def logger(debug: bool):
    logger = logging.Logger("Pylemon", level=logging.CRITICAL if debug != True else logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("%(levelname)s - %(asctime)s - %(message)s")
    )
    logger.addHandler(handler)
    return logger