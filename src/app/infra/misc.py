import psycopg2
import sys

# TODO: read these params from env variables
_conn = {
    "host": "35.233.0.181",
    "user": "reference_api",
    "password": "Vyyj3r7P49s7vpf5eYJCuqv2"
}


def __connect_pgsql(database: str):
    """ Connect to the PostgreSQL database server """
    params = _conn
    params.update({'database': database})
    try:
        # connect to the PostgreSQL
        conn = psycopg2.connect(**params)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1)
    print("Connection successful")
    return conn


def query_pgsql(query: str, database: str):
    conn = __connect_pgsql(database)
    with conn.cursor() as c:
        print('executing query')
        c.execute(query)
        d = c.fetchall()
    conn.close()
    return d
