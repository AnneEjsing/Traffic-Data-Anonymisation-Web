@routes.post('/right/update')
def right_update():
    f = fieldCheck(['camera_id', 'user_id', 'expiry'], request)
    if f: return f

    camera_id = request.form['camera_id']
    user_id = request.form['user_id']
    expiry = request.form['expiry']
    query = """
    UPDATE access_rights 
    SET expiry = %s
    WHERE camera_id = %s AND user_id = %s
    RETURNING *;
    """

    result, error = executeQuery(query, expiry, camera_id, user_id)
    if error: return Response(str(error), 500)
    return hasOneResult(result, "There are no access rights for that user and camera.", 404)

@routes.get('/right/get')
def right_get():
    f = fieldCheck(['camera_id', 'user_id'], request)
    if f: return f
    
    camera_id = request.form['camera_id']
    user_id = request.form['user_id']
    query = """
    SELECT *
    FROM access_rights
    WHERE camera_id = %s AND user_id = %s;
    """

    result, error = executeQuery(query, camera_id, user_id)
    if error: return Response(str(error), 500)
    return str(result)


@routes.delete('/right/delete')
def right_delete():
    f = fieldCheck(['camera_id', 'user_id'], request)
    if f: return f

    camera_id = request.form['camera_id']
    user_id = request.form['user_id']
    query = """
    DELETE FROM access_rights
    WHERE camera_id = %s AND user_id = %s
    RETURNING *;
    """
    result, error = executeQuery(query, camera_id, user_id)
    if error: return Response(str(error),500)
    
    return hasOneResult(result, "There are no access for that user and camera.", 404)

@routes.post('/right/create',methods=['POST'])
def right_create():
    f = fieldCheck(['camera_id', 'user_id', 'expiry'], request)
    if f: return f
    
    camera_id = request.form['camera_id']    
    user_id = request.form['user_id']
    expiry = request.form['expiry']
    query = """
    INSERT INTO access_rights (camera_id,user_id,expiry)
    VALUES (
        %s, %s, %s
    )
    RETURNING *;
    """
    result, error = executeQuery(query,camera_id,user_id,expiry)
    if error: return Response(str(error),500)
    return str(result)

@routes.get('/right/list',methods=['GET'])
def right_list():
    query = "SELECT * FROM access_rights;"
    result, error = executeQuery(query)
    if error: return Response(str(error),500)
    return str(result)