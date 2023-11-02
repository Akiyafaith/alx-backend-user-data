#!/usr/bin/env python3
"""a function called filter_datum"""
import logging
import re
from typing import List
import os
import mysql.connector

PII_FIELDS = ("name", "email", "ssn", "phone", "address")


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


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connector to the database"""
    connector = mysql.connector.connect(
        user=os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.environ.get('PERSONAL_DATA_DB_PASSWORD', ''),
        host=os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.environ.get('PERSONAL_DATA_DB_NAME'))
    return connector


def main():
    """reads and filters data"""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()
    for row in cursor:
        log_msg = ' '.join([f"{key}={row[key]}" for key in row])
        logger.info(log_msg)
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
