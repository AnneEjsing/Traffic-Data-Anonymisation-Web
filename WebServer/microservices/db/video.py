@routes.post('/video/update')
async def video_update(request):
    data = await request.json()
    f = field_check(['video_id', 'user_id', 'camera_id', 'video_thumbnail'], data)
    if f != None: return f

    video_id = data['video_id']
    user_id = data['user_id']
    camera_id = data['camera_id']
    video_thumbnail = data['video_thumbnail']
    query = """
    UPDATE recorded_videos 
    SET user_id = %s, camera_id = %s, video_thumbnail = %s
    WHERE video_id = %s
    RETURNING *;
    """

    result, error = execute_query(query, user_id, camera_id, video_thumbnail, video_id)
    if error: return web.Response(text=str(error), status=500)
    return has_one_result(result, "There is no video with that id.", 404)

@routes.get('/video/get')
async def video_get(request):
    data = await request.json()
    f = field_check(['video_id'], data)
    if f != None: return f
    
    video_id = data['video_id']
    query = """
    SELECT *
    FROM recorded_videos
    WHERE video_id = %s;
    """

    result, error = execute_query(query, video_id)
    if error: return web.Response(text=str(error), status=500)
    return has_one_result(result, "There is no video with that id.", 404)


@routes.delete('/video/delete')
async def video_delete(request):
    data = await request.json()
    f = field_check(['video_id'], data)
    if f != None: return f

    video_id = data['video_id']
    query = """
    DELETE FROM recorded_videos
    WHERE video_id = %s
    RETURNING *;
    """
    result, error = execute_query(query, video_id)
    if error: return web.Response(text=str(error),status=500)
    
    return has_one_result(result, "There is no video with this id.", 404)

@routes.post('/video/create')
async def video_create(request):
    data = await request.json()
    f = field_check(['user_id', 'camera_id', 'video_thumbnail'], data)
    if f != None: return f
    
    user_id = data['user_id']
    camera_id = data['camera_id']
    video_thumbnail = data['video_thumbnail']

    query = """
    INSERT INTO recorded_videos (user_id, camera_id, video_thumbnail, save_time)
    VALUES (
        %s, %s, %s, NOW()
    )
    RETURNING *;
    """
    result, error = execute_query(query, user_id, camera_id, video_thumbnail)
    if error: return web.Response(text=str(error),status=500)
    return web.Response(text=json.dumps(result, default=str), status=200)

@routes.get('/video/list')
def video_list(request):
    query = "SELECT * FROM recorded_videos;"
    result, error = execute_query(query)
    if error: return web.Response(text=str(error),status=500)
    return web.Response(text=json.dumps(result, default=str),status=200)
