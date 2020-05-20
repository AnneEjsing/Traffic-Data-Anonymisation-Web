
# How build and run Singularity containers

## Building all Singularity containers in the project
Run the following command
```
bash build_singularity.sh
```
All containers will be places in subfolders in the folder "singularity_containers"

## Running containers

### Postgres database

```
mkdir -p singularity_containers/postgres/pgData
sudo singularity run -B singularity_containers/postgres/pgData/:/var/lib/postgresql/data,/var/run/postgresql singularity_containers/postgres/db.sif
```


### DB Resolver 
```
singularity run --no-home singularity_containers/dbresolver/dbresolver.sif
```

### Dispatcher
```
sudo singularity run --no-home singularity_containers/dispatcher/dispatcher.sif
```

### Frontend
```
mkdir -p singularity_containers/frontend/nginx
singularity run --fakeroot -B singularity_containers/frontend/nginx:/var singularity_containers/frontend/frontend.sif
```

### Camera service
```
singularity run --no-home singularity_containers/camera-service/camera-service.sif
```

### Model-changer
```
singularity run --no-home singularity_containers/model-changer/model-changer.sif
```

### Profile service
```
singularity run --no-home singularity_containers/profile-service/profile-service.sif
```

### Streamer
```
mkdir -p singularity_containers/streamer/nginx/var
mkdir -p singularity_containers/streamer/nginx/hls 
mkdir -p singularity_containers/streamer/nginx/nginx
singularity run --fakeroot -B singularity_containers/streamer/nginx/var:/var,singularity_containers/streamer/nginx/hls:/etc/nginx/tmp/hls,singularity_containers/streamer/nginx/nginx:/usr/local/nginx singularity_containers/streamer/streamer.sif
```

### Video-deleter
```
touch singularity_containers/video-deleter/error.log
singularity run --no-home -B singularity_containers/video-deleter/error.log:/error.log singularity_containers/video-deleter/video-deleter.sif
```

### Video-saver
```
touch singularity_containers/video-file-saver/error.log
singularity run --no-home -B singularity_containers/video-file-saver/error.log:/error.log singularity_containers/video-file-saver/video-file-saver.sif
```

### Video-service
```
singularity run --no-home singularity_containers/video-service/video-service.sif
```
