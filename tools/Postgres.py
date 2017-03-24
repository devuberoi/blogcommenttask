import config
import psycopg2 as db
import psycopg2.extras as extras
import sys

def init(encoding=config.POSTGRES_CREDS["ENCODING"]):
    reload(sys)
    sys.setdefaultencoding(encoding)
    creds = config.POSTGRES_CREDS
    connection = db.connect(host=creds['HOST'], user=creds['USER'],
                            password=creds['PASSWORD'], database=creds['DATABASE'])
    connection.set_client_encoding(encoding)
    return connection

def get_cursor(db_object, structure="default"):
    if structure == "default":
        cursor = db_object.cursor()
    elif structure == "dict":
        cursor = db_object.cursor(cursor_factory=extras.DictCursor)
    elif structure == "realdict":
        cursor = db_object.cursor(cursor_factory=extras.RealDictCursor)
    return cursor
