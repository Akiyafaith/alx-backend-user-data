#!/usr/bin/env python3
"""a function called filter_datum"""
import re


def filter_datum(fields, redaction, message, separator):
    """returns the log message obfuscated"""
    regex = f'({separator}|^)({"|".join(fields)}=.+?)(?={separator}|$)'
    return re.sub(regex, f'\\1{redaction}', message)
