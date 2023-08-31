#!/usr/bin/env python3
"""
Main file
"""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str :
    """ filter datum"""
    return re.sub(r'(?P<field>{})=[^{}]*'.format('|'.join(fields), separator),
                   r'\g<field>={}'.format(redaction), message)
    