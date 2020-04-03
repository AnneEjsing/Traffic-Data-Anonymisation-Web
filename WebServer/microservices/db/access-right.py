@routes.post('/right/update')
async def right_update(request):
    data = await request.json()
    f = fieldCheck(['camera_id', 'user_id', 'expiry'], data)
    if f != None: return f

    camera_id = data['camera_id']
    user_id = data['user_id']
    expiry = data['expiry']
    query = """
    UPDATE access_rights 
    SET expiry = %s
    WHERE camera_id = %s AND user_id = %s
    RETURNING *;
    """

    result, error = executeQuery(query, expiry, camera_id, user_id)
    if error: return web.Response(text=str(error),status=500)
    return hasOneResult(result, "There are no access rights for that user and camera.", 404)

@routes.get('/right/get')
async def right_get(request):
    data = await request.json()
    f = fieldCheck(['camera_id', 'user_id'], data)
    if f != None: return f
    
    camera_id = data['camera_id']
    user_id = data['user_id']
    query = """
    SELECT *
    FROM access_rights
    WHERE camera_id = %s AND user_id = %s;
    """

    result, error = executeQuery(query, camera_id, user_id)
    if error: return web.Response(text=str(error),status=500)
    return web.Response(text=str(result), status=200)


@routes.delete('/right/delete')
async def right_delete(request):
    data = await request.json()
    f = fieldCheck(['camera_id', 'user_id'], data)
    if f != None: return f

    camera_id = data['camera_id']
    user_id = data['user_id']
    query = """
    DELETE FROM access_rights
    WHERE camera_id = %s AND user_id = %s
    RETURNING *;
    """
    result, error = executeQuery(query, camera_id, user_id)
    if error: return web.Response(text=str(error),status=500)
    
    return hasOneResult(result, "There are no access for that user and camera.", 404)

@routes.post('/right/create')
async def right_create(request):
    data = await request.json()
    f = fieldCheck(['camera_id', 'user_id', 'expiry'], data)
    if f != None: return f
    
    camera_id = data['camera_id']    
    user_id = data['user_id']
    expiry = data['expiry']
    query = """
    INSERT INTO access_rights (camera_id,user_id,expiry)
    VALUES (
        %s, %s, %s
    )
    RETURNING *;
    """
    result, error = executeQuery(query,camera_id,user_id,expiry)
    if error: return web.Response(text=str(error),status=500)
    return web.Response(text=str(result), status=200)

@routes.get('/right/list')
def right_list(request):
    query = "SELECT * FROM access_rights;"
    result, error = executeQuery(query)
    if error: return web.Response(text=str(error),status=500)
    return web.Response(text=str(result), status=200)