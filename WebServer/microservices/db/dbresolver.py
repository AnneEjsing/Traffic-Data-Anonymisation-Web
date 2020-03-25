import argparse
from psycopg2 import connect
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

    try:
        # declare a cursor object from the connection
        cursor = conn.cursor()

        # execute an SQL statement using the psycopg2 cursor object.
        # By seperating the query and the inputs, psycopg2 does sanitation.
        cursor.execute(query,inputs)

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

def sanitise(input):
    return input

#Create the web app
app = Flask(__name__)

@app.route('/login',methods=['POST'])
def login():
    username = request.form['username']    
    password = request.form['password']
    query = """
    SELECT * 
    FROM users 
    WHERE users.email = %s
        AND users.password = md5(CONCAT(%s,users.salt));
    """
    if len(executeQuery(query,username,password)) == 1:
        return Response("success",200)
    else:
        return Response("Not success", 401)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Provides different function calls to retrieve data from the database.'
    )

    args = parser.parse_args()
    app.run(host='0.0.0.0',port=1337,debug=True)