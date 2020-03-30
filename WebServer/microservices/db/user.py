
@app.route('/user/login',methods=['POST'])
def user_login():
    f = fieldCheck(['email','password'], request)
    if f: return f
    
    email = request.form['email']    
    password = request.form['password']
    query = """
    SELECT * 
    FROM users 
    WHERE email = %s AND password = crypt(%s,password);
    """
    result, error = executeQuery(query,email,password)
    if error: return Response(str(error),500)
    return hasOneResult(result,"Login credentials are not valid", 401)

@app.route('/user/update', methods=['POST'])
def user_update():
    f = fieldCheck(['id', 'email', 'password', 'rights'], request)
    if f: return f

    id = request.form['id']
    email = request.form['email']
    password = request.form['password']
    role = request.form['rights']
    query = """
    UPDATE users 
    SET email = %s, password = crypt(%s,gen_salt('bf')), role = %s
    WHERE user_id = %s
    RETURNING *;
    """

    result, error = executeQuery(query, email, password, role, id)
    if error: return Response(str(error), 500)
    return hasOneResult(result, "There is no user with that id.", 404)

@app.route('/user/get', methods=['GET'])
def user_get():
    f = fieldCheck(['id'], request)
    if f: return f
    
    id = request.form['id']
    query = """
    SELECT *
    FROM users
    WHERE user_id = %s;
    """

    result, error = executeQuery(query, id)
    if error: return Response(str(error), 500)
    return hasOneResult(result, "There are no user with that id.", 404)


@app.route('/user/delete', methods=['DELETE'])
def user_delete():
    f = fieldCheck(['id'], request)
    if f: return f

    id = request.form['id']
    query = """
    DELETE FROM users
    WHERE user_id = %s
    RETURNING user_id;
    """
    result, error = executeQuery(query, id)
    if error: return Response(str(error),500)
    
    return hasOneResult(result, "There is no user with this id.", 404)

@app.route('/user/signup',methods=['POST'])
def user_signup():
    f = fieldCheck(['email', 'password', 'rights'], request)
    if f: return f
    
    email = request.form['email']    
    password = request.form['password']
    rights = request.form['rights']
    query = """
    INSERT INTO users (email,role,password)
    VALUES (
        %s, %s, crypt(%s, gen_salt('bf'))
    )
    RETURNING *;
    """
    result, error = executeQuery(query,email,rights,password)
    if error: return Response(str(error),500)
    return str(result)

@app.route('/user/list',methods=['GET'])
def user_list():
    query = "SELECT * FROM users;"
    result, error =executeQuery(query)
    if error: return Response(str(error),500)
    return str(result)