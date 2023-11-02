#!/usr/bin/env python3
"""a function called filter_datum"""
import logging
import re


def filter_datum(fields: list[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    regex = f'({separator}|^)({"|".join(fields)}=.+?)(?={separator}|$)'
    return re.sub(regex, f'\\1{redaction}', message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields=None):
        """initialize a class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter incoming log records"""
        if self.fields:
            for field in self.fields:
                record.msg = re.sub(f'{field}=.+?;',
                                    f'{field}={self.REDACTION};', record.msg)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """returns a logging.Logger object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger