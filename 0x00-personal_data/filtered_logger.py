#!/usr/bin/env python3
"""
Main file
"""
from typing import List
import re
import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ format """
        record.msg = filter_datum(self.fields,
                                  self.REDACTION, record.msg, self.SEPARATOR)
        return super().format(record)

def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str :
    """ filter datum"""
    return re.sub(r'(?P<field>{})=[^{}]*'.format('|'.join(fields), separator),
                   r'\g<field>={}'.format(redaction), message)
