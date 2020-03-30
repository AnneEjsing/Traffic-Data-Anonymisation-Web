@app.route('/camera/updateLSOL', methods=['POST'])
def camera_updatelsoĺ():
    f = fieldCheck(['id'], request)
    if f: return f

    id = request.form['id']
    query = """
    UPDATE cameras 
    SET last_sign_of_life = NOW()
    WHERE camera_id = %s
    RETURNING last_sign_of_life;
    """

    result, error = executeQuery(query, id)
    if error: return Response(str(error), 500)
    return hasOneResult(result, "There is no camera with that id.", 404)


@app.route('/camera/updateInfo', methods=['POST'])
def camera_update():
    f = fieldCheck(['id', 'owner', 'description', 'ip'], request)
    if f: return f

    id = request.form['id']
    owner = request.form['owner']
    description = request.form['description']
    ip = request.form['ip']
    query = """
    UPDATE cameras 
    SET owner = %s, description = %s, ip = %s
    WHERE camera_id = %s
    RETURNING *;
    """

    result, error = executeQuery(query, owner, description, ip, id)
    if error: return Response(str(error), 500)
    return hasOneResult(result, "There is no camera with that id.", 404)

@app.route('/camera/get', methods=['GET'])
def camera_get():
    f = fieldCheck(['id'], request)
    if f: return f
    
    id = request.form['id']
    query = """
    SELECT *
    FROM cameras
    WHERE camera_id = %s;
    """

    result, error = executeQuery(query, id)
    if error: return Response(str(error), 500)
    return str(result)


@app.route('/camera/delete', methods=['DELETE'])
def camera_delete():
    f = fieldCheck(['id'], request)
    if f: return f

    id = request.form['id']
    query = """
    DELETE FROM cameras
    WHERE camera_id = %s
    RETURNING *;
    """
    result, error = executeQuery(query, id)
    if error: return Response(str(error),500)
    
    return hasOneResult(result, "There is no camera with this id.", 404)

@app.route('/camera/create',methods=['POST'])
def camera_create():
    f = fieldCheck(['owner', 'description', 'ip'], request)
    if f: return f
    
    owner = request.form['owner']    
    description = request.form['description']
    ip = request.form['ip']
    query = """
    INSERT INTO cameras (owner,description,ip)
    VALUES (
        %s, %s, %s
    )
    RETURNING *;
    """
    result, error = executeQuery(query,owner,description,ip)
    if error: return Response(str(error),500)
    return str(result)

@app.route('/camera/list',methods=['GET'])
def camera_list():
    query = "SELECT * FROM cameras;"
    result, error =executeQuery(query)
    if error: return Response(str(error),500)
    return str(result)