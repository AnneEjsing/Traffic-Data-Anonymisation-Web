
# import the connect library from psycopg2
from psycopg2 import connect

#Exampe query: f"SELECT * FROM {table_name};"

# Sends a query to the database and returns the response.
# Inspired by: #https://kb.objectrocket.com/postgresql/python-and-postgresql-docker-container-part-2-1063
def executeQuery(query):
    # declare connection instance
    conn = connect(
        dbname = "Traffic_Annonymisation_DB",
        user = "postgres",
        host = "172.28.1.4",
        password = "postgres"
    )

    results = []

    try:
        # declare a cursor object from the connection
        cursor = conn.cursor()

        # execute an SQL statement using the psycopg2 cursor object
        cursor.execute(query)

        # enumerate() over the PostgreSQL records
        for i, record in enumerate(cursor):
            results.append(record)

    except Error as e:
        eprint("Error when connecting to Postgresql: ", e)

    finally:
        # close the cursor object to avoid memory leaks
        cursor.close()

        # close the connection as well
        conn.close()

    return results