import MySQLdb
from environment import *

def connection():
    conn = MySQLdb.connect(host=environment_db_host,
                           user=environment_db_user,
                           passwd=environment_db_passwd,
                           db=environment_db)
    c = conn.cursor()

    return c, conn
