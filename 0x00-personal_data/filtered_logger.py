#!/usr/bin/env python3
"""a function called filter_datum"""
import logging
import re


def filter_datum(fields: list[str], redaction: str, message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    regex = f'({separator}|^)({"|".join(fields)}=.+?)(?={separator}|$)'
    return re.sub(regex, f'\\1{redaction}', message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"

    def __init__(self, fields=None):
        """initialize a class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        if self.fields:
            for field in self.fields:
                record.msg = re.sub(f'{field}=.+?;', f'{field}={self.REDACTION};',
                                    record.msg)
        return super(RedactingFormatter, self).format(record)
