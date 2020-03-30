@app.route('/video/update', methods=['POST'])
def video_update():
    f = fieldCheck(['video_id', 'user_id', 'camera_id', 'file_path', 'video_thumbnail'], request)
    if f: return f

    video_id = request.form['video_id']
    user_id = request.form['user_id']
    camera_id = request.form['camera_id']
    file_path = request.form['file_path']
    video_thumbnail = request.form['video_thumbnail']
    query = """
    UPDATE recorded_videos 
    SET user_id = %s, camera_id = %s, video_file= %s, video_thumbnail = %s
    WHERE video_id = %s
    RETURNING *;
    """

    result, error = executeQuery(query, user_id, camera_id, file_path, video_thumbnail, video_id)
    if error: return Response(str(error), 500)
    return hasOneResult(result, "There is no video with that id.", 404)

@app.route('/video/get', methods=['GET'])
def video_get():
    f = fieldCheck(['video_id'], request)
    if f: return f
    
    video_id = request.form['video_id']
    query = """
    SELECT *
    FROM recorded_videos
    WHERE video_id = %s;
    """

    result, error = executeQuery(query, video_id)
    if error: return Response(str(error), 500)
    return hasOneResult(result, "There is no video with that id.", 404)


@app.route('/video/delete', methods=['DELETE'])
def video_delete():
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

@app.route('/video/create',methods=['POST'])
def video_create():
    f = fieldCheck(['user_id', 'camera_id', 'file_path', 'video_thumbnail'], request)
    if f: return f
    
    user_id = request.form['user_id']
    camera_id = request.form['camera_id']
    file_path = request.form['file_path']
    video_thumbnail = request.form['video_thumbnail']

    query = """
    INSERT INTO recorded_videos (user_id, camera_id, video_file, video_thumbnail, save_time)
    VALUES (
        %s, %s, %s, %s, NOW()
    )
    RETURNING *;
    """
    result, error = executeQuery(query, user_id, camera_id, file_path, video_thumbnail)
    if error: return Response(str(error),500)
    return str(result)

@app.route('/video/list',methods=['GET'])
def video_list():
    query = "SELECT * FROM recorded_videos;"
    result, error =executeQuery(query)
    if error: return Response(str(error),500)
    return str(result)