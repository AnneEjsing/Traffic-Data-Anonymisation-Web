
@routes.post('/user/login')
def user_login(request):
    f = fieldCheck(['email','password'], request)
    if f: return f
    
    email = request['email']    
    password = request['password']
    query = """
    SELECT * 
    FROM users 
    WHERE email = %s AND password = crypt(%s,password);
    """
    result, error = executeQuery(query,email,password)
    if error: return web.Response(str(error),500)
    return hasOneResult(result,"Login credentials are not valid", 401)

@routes.post('/user/update')
def user_update(request):
    f = fieldCheck(['id', 'email', 'password', 'rights'], request)
    if f: return f

    id = request['id']
    email = request['email']
    password = request['password']
    role = request['rights']
    query = """
    UPDATE users 
    SET email = %s, password = crypt(%s,gen_salt('bf')), role = %s
    WHERE user_id = %s
    RETURNING *;
    """

    result, error = executeQuery(query, email, password, role, id)
    if error: return web.Response(str(error), 500)
    return hasOneResult(result, "There is no user with that id.", 404)

@routes.get('/user/get')
def user_get(request):
    f = fieldCheck(['id'], request)
    if f: return f
    
    id = request['id']
    query = """
    SELECT *
    FROM users
    WHERE user_id = %s;
    """

    result, error = executeQuery(query, id)
    if error: return web.Response(str(error), 500)
    return str(result)


@routes.delete('/user/delete')
def user_delete(request):
    f = fieldCheck(['id'], request)
    if f: return f

    id = request['id']
    query = """
    DELETE FROM users
    WHERE user_id = %s
    RETURNING user_id;
    """
    result, error = executeQuery(query, id)
    if error: return web.Response(str(error),500)
    
    return hasOneResult(result, "There is no user with this id.", 404)

@routes.post('/user/signup')
def user_signup(request):
    f = fieldCheck(['email', 'password', 'rights'], request)
    if f: return f
    
    email = request['email']    
    password = request['password']
    rights = request['rights']
    query = """
    INSERT INTO users (email,role,password)
    VALUES (
        %s, %s, crypt(%s, gen_salt('bf'))
    )
    RETURNING *;
    """
    result, error = executeQuery(query,email,rights,password)
    if error: return web.Response(str(error),500)
    return str(result)

@routes.get('/user/list')
def user_list(request):
    query = "SELECT * FROM users;"
    result, error = executeQuery(query)
    if error: return web.Response(str(error),500)
    return str(result)