from aiohttp import web
import json
import dbresolver

routes = web.RouteTableDef()

@routes.put('/camera/updateLSOL')
async def camera_updatelsol(request):
    data = await request.json()
    f = dbresolver.field_check(['id'], data)
    if f != None: return f

    id = data['id']
    query = """
    UPDATE cameras 
    SET last_sign_of_life = NOW()
    WHERE camera_id = %s
    RETURNING last_sign_of_life;
    """

    result, error = dbresolver.execute_query(query, id)
    if error: return web.Response(text=str(error), status=500)
    return dbresolver.has_one_result(result, "There is no camera with that id.", 404)


@routes.put('/camera/updateInfo')
async def camera_update(request):
    data = await request.json()
    f = dbresolver.field_check(['camera_id', 'description', 'ip', 'label', 'source'], data)
    if f != None: return f

    id = data['camera_id']
    source = data['source']
    description = data['description']
    ip = data['ip']
    label = data['label']
    query = """
    UPDATE cameras 
    SET description = %s, ip = %s, label = %s, source = %s
    WHERE camera_id = %s
    RETURNING *;
    """

    result, error = dbresolver.execute_query(query, description, ip, label, source, id)
    if error: return web.Response(text=str(error), status=500)
    return dbresolver.has_one_result(result, "There is no camera with that id.", 404)

@routes.get('/camera/get')
async def camera_get(request):
    data = await request.json()
    f = dbresolver.field_check(['id'], data)
    if f != None: return f
    
    id = data['id']
    query = """
    SELECT *
    FROM cameras
    WHERE camera_id = %s;
    """

    result, error = dbresolver.execute_query(query, id)
    if error: return web.Response(text=str(error), status=500)
    return dbresolver.has_one_result(result, "Multiple or no cameras returned from the database, when expecting exactly one.", 404)


@routes.delete('/camera/delete')
async def camera_delete(request):
    f = dbresolver.field_check(['id'], request.query)
    if f != None: return f
    id = request.query['id']
    query = """
    DELETE FROM cameras
    WHERE camera_id = %s
    RETURNING *;
    """
    result, error = dbresolver.execute_query(query, id)
    if error: return web.Response(text=str(error),status=500)
    
    return dbresolver.has_one_result(result, "There is no camera with this id.", 404)

@routes.post('/camera/create')
async def camera_create(request):
    data = await request.json()

    f = dbresolver.field_check(['owner', 'description', 'ip', 'label', 'source'], data)
    if f != None: return f
    
    owner = data['owner']
    description = data['description']
    ip = data['ip']
    label = data['label']
    source = data['source']
    query = """
    INSERT INTO cameras (owner,description,ip,label,source)
    VALUES (
        %s, %s, %s, %s, %s
    )
    RETURNING *;
    """
    result, error = dbresolver.execute_query(query,owner,description,ip,label,source)
    if error: return web.Response(text=str(error),status=500)
    return web.Response(text=json.dumps(result, default=str),status=200)

@routes.get('/camera/adminlist')
def camera_list(request):
    query = "SELECT source, description, label, camera_id FROM cameras;"
    result, error = dbresolver.execute_query(query)
    if error: return web.Response(text=str(error),status=500)
    return web.Response(text=json.dumps(result, default=str),status=200)

@routes.get('/camera/userlist')
async def camera_userlist(request):
    data = await request.json()
    f = dbresolver.field_check(['id'], data)
    if f != None: return f
    
    user = data['id']
    query = """
    SELECT source, description, label, cameras.camera_id
    FROM cameras
    JOIN access_rights ON cameras.camera_id = access_rights.camera_id
    WHERE access_rights.user_id = %s;
    """
    result, error = dbresolver.execute_query(query,user)
    if error: return web.Response(text=error,status=500)
    return web.Response(text=json.dumps(result, default=str), status=200)
