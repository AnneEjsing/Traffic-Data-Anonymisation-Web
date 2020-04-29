from aiohttp import web
import json
import dbresolver

routes = web.RouteTableDef()

@routes.get('/recordings/list/camera_id')
async def list_camera_id(request):
    data = await request.json()
    f = dbresolver.field_check(['camera_id'], data)
    if f != None : return f

    camera_id = data['camera_id']
    query = """
    SELECT *
    FROM recordings
    WHERE camera_id = %s;
    """

    result, error = dbresolver.execute_query(query, camera_id)
    
    if error: return web.Response(text=str(error), status=500)
    else:
        return web.Response(text=json.dumps(result, default=str),status=200)


@routes.get('/recordings/list/user_id')
async def list_user_id(request):
    data = await request.json()
    f = dbresolver.field_check(['user_id'], data)
    if f != None : return f

    user_id = data['user_id']
    query = """
    SELECT *
    FROM recordings
    WHERE user_id = %s;
    """

    result, error = dbresolver.execute_query(query, user_id)
    if error: return web.Response(text=str(error), status=500)
    else:
        return web.Response(text=json.dumps(result, default=str),status=200)

@routes.get('/recordings/get')
async def get(request):
    data = await request.json()
    f = dbresolver.field_check(['user_id', 'camera_id'], data)
    if f != None : return f

    user_id = data['user_id']
    camera_id = data['camera_id']
    query = """
    SELECT *
    FROM recordings
    WHERE user_id = %s
    AND camera_id = %s;
    """
    
    result, error = dbresolver.execute_query(query, user_id, camera_id)
    if error: return web.Response(text=str(error), status=500)
    return dbresolver.has_one_result(result, "No such recording found", 404)


@routes.delete('/recordings/delete')
async def delete(request):
    data = await request.json()
    f = dbresolver.field_check(['user_id', 'camera_id'], data)
    if f != None : return f

    user_id = data['user_id']
    camera_id = data['camera_id']
    query = """
    DELETE FROM recordings
    WHERE user_id = %s
    AND camera_id = %s
    RETURNING *;
    """

    result, error = dbresolver.execute_query(query, user_id, camera_id)
    if error: return web.Response(text=str(error),status=500)
    return dbresolver.has_one_result(result, "There is no recording with this id.", 404)

@routes.post('/recordings/insert')
async def insert(request):
    data = await request.json()
    f = dbresolver.field_check(['user_id', 'camera_id', 'recording_time', 'recording_intervals'], data)
    if f != None : return f

    user_id = data['user_id']
    camera_id = data['camera_id']
    recording_time = data['recording_time']
    recording_intervals = data['recording_intervals']
    
    query = """
    INSERT INTO recordings (user_id, camera_id, start_time, recording_time, recording_intervals)
    VALUES (
        %s, %s,  NOW(), %s, %s
    )
    RETURNING *;
    """

    result, error = dbresolver.execute_query(query,user_id, camera_id, recording_time, recording_intervals)
    if error: return web.Response(text=str(error),status=500)
    return web.Response(text=json.dumps(result, default=str), status=200)

