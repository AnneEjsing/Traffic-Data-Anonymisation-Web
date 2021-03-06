from aiohttp import web
import json
import dbresolver

routes = web.RouteTableDef()


@routes.get('/user/login')
async def user_login(request):
    data = await request.json()
    f = dbresolver.field_check(['email','password'], data)
    if f != None: return f
    
    email = data['email']    
    password = data['password']
    query = """
    SELECT * 
    FROM users 
    WHERE email = %s AND password = crypt(%s,password);
    """
    result, error = dbresolver.execute_query(query,email,password)
    if error: return web.Response(text=str(error),status=500)
    return dbresolver.has_one_result(result, "Login credentials are not valid.", 401)


@routes.post('/user/update')
async def user_update(request):
    data = await request.json()
    f = dbresolver.field_check(['id', 'email', 'password', 'rights'], data)
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

    result, error = dbresolver.execute_query(query, email, password, role, id)
    if error: return web.Response(text=str(error), status=500)
    return dbresolver.has_one_result(result, "There is no user with that id.", 404)

@routes.get('/user/get')
async def user_get_id(request):
    data = await request.json()
    f = dbresolver.field_check(['id'], data)
    if f != None: return f
    
    id = data['id']
    query = """
    SELECT *
    FROM users
    WHERE user_id = %s;
    """

    result, error = dbresolver.execute_query(query, id)
    if error: return web.Response(text=str(error), status=500)
    return dbresolver.has_one_result(result, "No user with that id.", 404)

@routes.get('/user/get/email')
async def user_get_email(request):
    data = await request.json()
    f = dbresolver.field_check(['email'], data)
    if f != None: return f
    
    email = data['email']
    query = """
    SELECT *
    FROM users
    WHERE email = %s;
    """

    result, error = dbresolver.execute_query(query, email)
    if error: return web.Response(text=str(error), status=500)
    return dbresolver.has_one_result(result, "No user with that email.", 404)

@routes.delete('/user/delete')
async def user_delete(request):
    data = await request.json()
    f = dbresolver.field_check(['id'], data)
    if f != None: return f

    id = data['id']
    query = """
    DELETE FROM users
    WHERE user_id = %s
    RETURNING user_id;
    """
    result, error = dbresolver.execute_query(query, id)
    if error: return web.Response(text=str(error),status=500)
    
    return dbresolver.has_one_result(result, "There is no user with this id.", 404)

@routes.post('/user/signup')
async def user_signup(request):
    data = await request.json()
    f = dbresolver.field_check(['email', 'password', 'rights'], data)
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
    result, error = dbresolver.execute_query(query,email,rights,password)
    if error: return web.Response(text=str(error),status=500)
    return dbresolver.has_one_result(result, "None or too many results are returned from the database to the database handler.", 500)

@routes.get('/user/list')
def user_list(request):
    query = "SELECT * FROM users;"
    result, error = dbresolver.execute_query(query)
    if error: return web.Response(text=str(error),status=500)
    return web.Response(text=json.dumps(result, default=str), status=200)
