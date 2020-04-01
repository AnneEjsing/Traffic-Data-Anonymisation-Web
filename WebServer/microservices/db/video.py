@routes.post('/video/update')
def video_update(request):
    f = fieldCheck(['video_id', 'user_id', 'camera_id', 'file_path', 'video_thumbnail'], request)
    if f: return f

    video_id = request['video_id']
    user_id = request['user_id']
    camera_id = request['camera_id']
    file_path = request['file_path']
    video_thumbnail = request['video_thumbnail']
    query = """
    UPDATE recorded_videos 
    SET user_id = %s, camera_id = %s, video_file= %s, video_thumbnail = %s
    WHERE video_id = %s
    RETURNING *;
    """

    result, error = executeQuery(query, user_id, camera_id, file_path, video_thumbnail, video_id)
    if error: return web.Response(str(error), 500)
    return hasOneResult(result, "There is no video with that id.", 404)

@routes.get('/video/get')
def video_get(request):
    f = fieldCheck(['video_id'], request)
    if f: return f
    
    video_id = request['video_id']
    query = """
    SELECT *
    FROM recorded_videos
    WHERE video_id = %s;
    """

    result, error = executeQuery(query, video_id)
    if error: return web.Response(str(error), 500)
    return str(result)


@routes.delete('/video/delete')
def video_delete(request):
    f = fieldCheck(['video_id'], request)
    if f: return f

    video_id = request.form['video_id']
    query = """
    DELETE FROM recorded_videos
    WHERE video_id = %s
    RETURNING *;
    """
    result, error = executeQuery(query, video_id)
    if error: return Response(str(error),500)
    
    return hasOneResult(result, "There is no video with this id.", 404)

@routes.post('/video/create')
def video_create(request):
    f = fieldCheck(['user_id', 'camera_id', 'file_path', 'video_thumbnail'], request)
    if f: return f
    
    user_id = request['user_id']
    camera_id = request['camera_id']
    file_path = request['file_path']
    video_thumbnail = request['video_thumbnail']

    query = """
    INSERT INTO recorded_videos (user_id, camera_id, video_file, video_thumbnail, save_time)
    VALUES (
        %s, %s, %s, %s, NOW()
    )
    RETURNING *;
    """
    result, error = executeQuery(query, user_id, camera_id, file_path, video_thumbnail)
    if error: return web.Response(str(error),500)
    return str(result)

@routes.get('/video/list')
def video_list(request):
    query = "SELECT * FROM recorded_videos;"
    result, error = executeQuery(query)
    if error: return web.Response(str(error),500)
    return str(result)