#!/bin/bash

WD=$(pwd)

camera(){
    echo "Building camera service..."
    cd microservices/camera-service
    singularity build -F ../../singularity_containers/camera-service/camera-service.sif camera.def
    cd $WD
    echo ""
}

dbresolver(){
    echo "Building dbresolver..."
    cd microservices/db
    singularity build -F ../../singularity_containers/dbresolver/dbresolver.sif dbresolver.def
    cd $WD
    echo ""
}

database(){
    echo "Building database..."
    cd microservices/db
    singularity build -F ../../singularity_containers/postgres/db.sif postgres.def
    cd $WD
    echo ""
}

dispatcher(){
    echo "Building dispatcher..."
    cd microservices/dispatcher
    singularity build -F ../../singularity_containers/dispatcher/dispatcher.sif dispatcher.def
    cd $WD
    echo ""
}

model-changer(){
    echo "Building model-changer..."
    cd microservices/model-changer
    singularity build -F ../../singularity_containers/model-changer/model-changer.sif model-changer.def
    cd $WD
    echo ""
}

profile(){
    echo "Building profile-service..."
    cd microservices/profile-service
    singularity build -F ../../singularity_containers/profile-service/profile-service.sif profile-service.def
    cd $WD
    echo ""
}

streamer(){
    echo "Building streamer..."
    cd microservices/streamer
    singularity build -F ../../singularity_containers/streamer/streamer.sif streamer.def
    cd $WD
    echo ""
}

video-deleter(){
    echo "Building video-deleter..."
    cd microservices/video-deleter
    singularity build -F ../../singularity_containers/video-deleter/video-deleter.sif video-deleter.sif
    cd $WD
    echo ""
}

video-saver(){
    echo "Building video-file-saver..."
    cd microservices/video-downloader
    singularity build -F ../../singularity_containers/video-file-saver/video-file-saver.sif video-file-saver.def
    cd $WD
    echo ""
}

video-service(){
    echo "Building video-service..."
    cd microservices/video-service
    singularity build -F ../../singularity_containers/video-service/video-service.sif video-service.def
    cd $WD
    echo ""
}

frontend(){
    echo "Building frontend..."
    cd frontend
    singularity build -F ../singularity_containers/frontend/frontend.sif frontend.def
    cd $WD
    echo ""
}


camera && \
dbresolver && \
database && \
dispatcher &&  \
model-changer && \
profile && \
streamer && \
video-deleter && \
video-saver && \
video-service && \
frontend
