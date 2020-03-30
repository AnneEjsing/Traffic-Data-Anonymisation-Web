import argparse
from psycopg2 import connect, errors
from flask import Response, Flask, request

# Sends a query to the database and returns the response.
# Inspired by: #https://kb.objectrocket.com/postgresql/python-and-postgresql-docker-container-part-2-1063
def executeQuery(query,*inputs):
    # declare connection instance
    conn = connect(
        dbname = "traffic_annonymisation_db",
        user = "postgres",
        host = "postgres",
        password = "postgres",
        port = 5432
    )

    results = []
    error = None

    try:
        # declare a cursor object from the connection
        cursor = conn.cursor()

        # execute an SQL statement using the psycopg2 cursor object.
        # By seperating the query and the inputs, psycopg2 does sanitation.
        cursor.execute(query,inputs)
        conn.commit()

        # enumerate() over the PostgreSQL records
        for i, record in enumerate(cursor):
            results.append(record)

    except errors.InvalidTextRepresentation as e:
        error = e

    except errors.UniqueViolation as e:
        error = e.diag.message_detail 
    
    
    finally:
        # close the cursor object to avoid memory leaks
        cursor.close()

        # close the connection as well
        conn.close()

    return (results,error)

#Create the web app
app = Flask(__name__)


####### Helper functions
def fieldCheck(requiredFields, request):
    fieldsNotFound = []
    for i in requiredFields:
        if i not in request.form:
            fieldsNotFound.append(i)
    if fieldsNotFound: return Response("Field(s) " + str(fieldsNotFound) + " not found in the request to the database resolver.",500)
    return None

def hasOneResult(result, errorString, errorCode):
    if len(result) == 1:
        return Response("Success",200)
    else:
        return Response(errorString, errorCode)


####### Endpoints
exec(open("user.py").read())
exec(open("camera.py").read())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Provides different function calls to retrieve data from the database.'
    )

    args = parser.parse_args()
    app.run(host='0.0.0.0',port=1337,debug=True)
