#!/usr/bin/env python

"""
Copyright (c) 2006-2012 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""

from re import finditer

from lib.core.common import randomRange
from lib.core.data import kb
from lib.core.enums import PRIORITY

__priority__ = PRIORITY.LOW

def tamper(payload, **kwargs):
    """
    Add random comments to SQL keywords
    Example: 'INSERT' becomes 'IN/**/S/**/ERT'
    """

    retVal = payload

    if payload:
        for match in finditer(r"[A-Za-z_]+", payload):
            word = match.group()

            if len(word) < 2:
                continue

            if word.upper() in kb.keywords:
                _ = word[0]

                for i in xrange(1, len(word) - 1):
                    _ += "%s%s" % ("/**/" if randomRange(0, 1) else "", word[i])

                _ += word[-1]
                retVal = retVal.replace(word, _)

    return retVal
