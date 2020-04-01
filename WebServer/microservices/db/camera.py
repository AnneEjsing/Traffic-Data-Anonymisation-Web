@routes.post('/camera/updateLSOL')
def camera_updatelsoĺ(request):
    f = fieldCheck(['id'], request)
    if f: return f

    id = request['id']
    query = """
    UPDATE cameras 
    SET last_sign_of_life = NOW()
    WHERE camera_id = %s
    RETURNING last_sign_of_life;
    """

    result, error = executeQuery(query, id)
    if error: return web.Response(str(error), 500)
    return hasOneResult(result, "There is no camera with that id.", 404)


@routes.post('/camera/updateInfo')
def camera_update(request):
    f = fieldCheck(['id', 'owner', 'description', 'ip'], request)
    if f: return f

    id = request['id']
    owner = request['owner']
    description = request['description']
    ip = request['ip']
    query = """
    UPDATE cameras 
    SET owner = %s, description = %s, ip = %s
    WHERE camera_id = %s
    RETURNING *;
    """

    result, error = executeQuery(query, owner, description, ip, id)
    if error: return web.Response(str(error), 500)
    return hasOneResult(result, "There is no camera with that id.", 404)

@routes.get('/camera/get', methods=['GET'])
def camera_get(request):
    f = fieldCheck(['id'], request)
    if f: return f
    
    id = request['id']
    query = """
    SELECT *
    FROM cameras
    WHERE camera_id = %s;
    """

    result, error = executeQuery(query, id)
    if error: return web.Response(str(error), 500)
    return str(result)


@routes.delete('/camera/delete', methods=['DELETE'])
def camera_delete(request):
    f = fieldCheck(['id'], request)
    if f: return f

    id = request['id']
    query = """
    DELETE FROM cameras
    WHERE camera_id = %s
    RETURNING *;
    """
    result, error = executeQuery(query, id)
    if error: return web.Response(str(error),500)
    
    return hasOneResult(result, "There is no camera with this id.", 404)

@routes.post('/camera/create')
def camera_create(request):
    f = fieldCheck(['owner', 'description', 'ip'], request)
    if f: return f
    
    owner = request['owner']    
    description = request['description']
    ip = request['ip']
    query = """
    INSERT INTO cameras (owner,description,ip)
    VALUES (
        %s, %s, %s
    )
    RETURNING *;
    """
    result, error = executeQuery(query,owner,description,ip)
    if error: return web.Response(str(error),500)
    return str(result)

@routes.get('/camera/list')
def camera_list():
    query = "SELECT * FROM cameras;"
    result, error = executeQuery(query)
    if error: return web.Response(str(error),500)
    return str(result)