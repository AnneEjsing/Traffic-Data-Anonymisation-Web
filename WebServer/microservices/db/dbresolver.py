from psycopg2 import connect, errors
from psycopg2.extras import RealDictCursor
import access_right, camera, recordings, user, video_settings, video
from aiohttp import web
import asyncio
import json
import os


# Sends a query to the database and returns the response.
# Inspired by: #https://kb.objectrocket.com/postgresql/python-and-postgresql-docker-container-part-2-1063
def execute_query(query,*inputs):
    # declare connection instance
    conn = connect(
        dbname = os.getenv('POSTGRES_DB'),
        user = os.getenv('POSTGRES_USER'),
        host = os.getenv('POSTGRES_HOST'),
        password = os.getenv('POSTGRES_PASSWORD'),
        port = os.getenv('POSTGRES_PORT')
    )

    results = []
    error = None

    try:
        # declare a cursor object from the connection
        # The cursor_factory=RealDictCursor makes everything go json!
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # execute an SQL statement using the psycopg2 cursor object.
        # By seperating the query and the inputs, psycopg2 does sanitation.
        cursor.execute(query,inputs)
        conn.commit()

        # enumerate() over the PostgreSQL records
        results = cursor.fetchall()

    except errors.InvalidTextRepresentation as e:
        print("Invalid")
        print("Invavlid: "+ query)
        print("Invalid: "+ e.diag.message_detail)
        error = e.diag.message_detail

    except errors.UniqueViolation as e:
        error = e.diag.message_detail 

    except errors.InvalidDatetimeFormat as e:
        error = "The data time format is invalid. An example of a correct date is: '2020-04-30 11:06:50'."
    
    except errors.ForeignKeyViolation as e:
        error = e.diag.message_detail
    
    except errors.UndefinedFunction as e:
        print("Undefined")
        print("Undefined: " + query)
        print("Undefined: " + e.diag.message_detail)
        error = e.diag.message_detail
    
    
    finally:
        # close the cursor object to avoid memory leaks
        cursor.close()

        # close the connection as well
        conn.close()

    return (results,error)

#Create the web app
routes = web.RouteTableDef()

####### Helper functions
def field_check(required_fields, data):
    fields_not_found = []
    for i in required_fields:
        if i not in data:
            fields_not_found.append(i)
    if fields_not_found: return web.Response(text="Field(s) " + str(fields_not_found) + " not found in the request to the database resolver.",status=500)
    return None

def has_one_result(result, error_string, error_code):
    if len(result) == 1:
        return web.Response(text=json.dumps(result[0], default=str),status=200)
    else:
        return web.Response(text=error_string, status=error_code)

if __name__ == "__main__":
    app = web.Application()
    for route_list in [routes,access_right.routes,camera.routes,recordings.routes,user.routes,video_settings.routes,video.routes]:
        app.add_routes(route_list)
    web.run_app(app, host='0.0.0.0', port=1337)

