
@routes.get('/user/login')
async def user_login(request):
    data = await request.json()
    f = fieldCheck(['email','password'], data)
    if f != None: return f
    
    email = data['email']    
    password = data['password']
    query = """
    SELECT * 
    FROM users 
    WHERE email = %s AND password = crypt(%s,password);
    """
    result, error = executeQuery(query,email,password)

    if error: return web.Response(text=str(error),status=500)

    if (len(result) != 0):
        id = result[0]['user_id']
        rights = result[0]['role']
        data = json.dumps({ "id" : id, "rights": rights })

        return web.Response(text=data,status=200)
    else: 
        return web.Response(text="Login credentials are not valid", status=401)

@routes.post('/user/update')
async def user_update(request):
    data = await request.json()
    f = fieldCheck(['id', 'email', 'password', 'rights'], data)
    if f != None: return f

    id = data['id']
    email = data['email']
    password = data['password']
    role = data['rights']
    query = """
    UPDATE users 
    SET email = %s, password = crypt(%s,gen_salt('bf')), role = %s
    WHERE user_id = %s
    RETURNING *;
    """

    result, error = executeQuery(query, email, password, role, id)
    if error: return web.Response(text=str(error), status=500)
    return hasOneResult(result, "There is no user with that id.", 404)

@routes.get('/user/get')
async def user_get(request):
    data = await request.json()
    f = fieldCheck(['id'], data)
    if f != None: return f
    
    id = data['id']
    query = """
    SELECT *
    FROM users
    WHERE user_id = %s;
    """

    result, error = executeQuery(query, id)
    if error: return web.Response(text=str(error), status=500)
    return web.Response(text=json.dumps(result, default=str), status=200)


@routes.delete('/user/delete')
async def user_delete(request):
    data = await request.json()
    f = fieldCheck(['id'], data)
    if f != None: return f

    id = data['id']
    query = """
    DELETE FROM users
    WHERE user_id = %s
    RETURNING user_id;
    """
    result, error = executeQuery(query, id)
    if error: return web.Response(text=str(error),status=500)
    
    return hasOneResult(result, "There is no user with this id.", 404)

@routes.post('/user/signup')
async def user_signup(request):
    data = await request.json()
    f = fieldCheck(['email', 'password', 'rights'], data)
    if f != None: return f
    
    email = data['email']    
    password = data['password']
    rights = data['rights']
    query = """
    INSERT INTO users (email,role,password)
    VALUES (
        %s, %s, crypt(%s, gen_salt('bf'))
    )
    RETURNING *;
    """
    result, error = executeQuery(query,email,rights,password)
    if error: return web.Response(text=str(error),status=500)
    return web.Response(text=json.dumps(result, default=str), status=200)

@routes.get('/user/list')
def user_list(request):
    query = "SELECT * FROM users;"
    result, error = executeQuery(query)
    if error: return web.Response(text=str(error),status=500)
    return web.Response(text=json.dumps(result, default=str), status=200)