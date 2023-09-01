#!/usr/bin/env python3
"""
Main file
"""
from typing import List
import re, logging, mysql.connector, os


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')
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

def get_logger() -> logging.Logger:
    """ get logger"""
    logger = logging.getLogger("user_data")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger

def get_db() -> mysql.connector.connection.MySQLConnection:
    """create database """
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    
    connection = mysql.connector.connect(
        host=host,
        port=3306,
        user=user,
        password=pwd,
        database=name        
    )
    return connection

def main():
    """ main """
    query = "SELECT {} FROM users;".format(PII_FIELDS)
    info = get_logger()
    db_conn = get_db()
    with db_conn.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = map(
                lambda x: '{}={}'.format(x[0], x[1]),
                zip(PII_FIELDS, row)
            )
            msg = '{};'.format('; '.join(list(record)))
            args = ("user_data", logging.INFO, None, None, msg, None, None)
            log_record = logging.LogRecord(*args)
            info.handle(log_record)
