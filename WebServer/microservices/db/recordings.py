
@routes.get('/recordings/list/camera_id')
async def list_camera_id(request):
    data = await request.json()
    f = fieldCheck(['camera_id'], data)
    if f != None : return f

    camera_id = data['camera_id']
    query = """
    SELECT *
    FROM recordings
    WHERE camera_id = %s;
    """

    result, error = executeQuery(query, camera_id)
    
    if error: return web.Response(text=str(error), status=500)
    else:
        return web.Response(text=data,status=200)


@routes.get('/recordings/list/user_id')
async def list_user_id(request):
    data = await request.json()
    f = fieldCheck(['user_id'], data)
    if f != None : return f

    user_id = data['user_id']
    query = """
    SELECT *
    FROM recordings
    WHERE user_id = %s;
    """

    result, error = executeQuery(query, user_id)
    
    test = "["
    for i in range(len(result)):
        if (i != 0):
            test += ","
        camera_id = result[i][0]
        user_id = result[i][1]
        start_time = str(result[i][2])
        recording_time = result[i][3]
        recording_intervals = result[i][4]
        temp_data = json.dumps({ "camera_id" : camera_id, "user_id" : user_id, "start_time": start_time, "recording_time": recording_time, "recording_intervals": recording_intervals })
        test += temp_data
    test += "]"

    if error: return web.Response(text=str(error), status=500)
    else:
        return web.Response(text=test,status=200)

@routes.get('/recordings/get')
async def get(request):
    data = await request.json()
    f = fieldCheck(['user_id', 'camera_id'], data)
    if f != None : return f

    user_id = data['user_id']
    camera_id = data['camera_id']
    query = """
    SELECT *
    FROM recordings
    WHERE user_id = %s
    AND camera_id = %s;
    """
    
    result, error = executeQuery(query, user_id, camera_id)
    if error: return web.Response(text=str(error), status=500)
    elif (len(result) == 1):
        camera_id = result[0][0]
        user_id = result[0][1]
        start_time = str(result[0][2])
        recording_time = result[0][3]
        recording_intervals = result[0][4]
        data = json.dumps({ "camera_id" : camera_id, "user_id" : user_id, "start_time": start_time, "recording_time": recording_time, "recording_intervals": recording_intervals })

        return web.Response(text=data,status=200)
    else :
        return web.Response(text="Recording not found", status=404)


@routes.delete('/recordings/delete')
async def delete(request):
    data = await request.json()
    f = fieldCheck(['user_id', 'camera_id'], data)
    if f != None : return f

    user_id = data['user_id']
    camera_id = data['camera_id']
    query = """
    DELETE FROM recordings
    WHERE user_id = %s
    AND camera_id = %s
    RETURNING *;
    """

    result, error = executeQuery(query, user_id, camera_id)
    if error: return web.Response(text=str(error),status=500)
    
    return hasOneResult(result, "There is no recording with this id.", 404)

@routes.post('/recordings/insert')
async def insert(request):
    data = await request.json()
    f = fieldCheck(['user_id', 'camera_id', 'recording_time', 'recording_intervals'], data)
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
    result, error = executeQuery(query,user_id, camera_id, recording_time, recording_intervals)
    if error: return web.Response(text=str(error),status=500)
    return web.Response(text=str(result), status=200)

