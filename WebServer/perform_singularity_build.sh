#!/bin/bash

WD=$(pwd)

camera(){
    echo ""
    echo "Building camera service..."
    cd microservices/camera-service
    singularity build -F ../../singularity_containers/camera-service/camera-service.sif camera.def
}

dbresolver(){
    echo ""
    echo "Building dbresolver..."
    cd microservices/db
    singularity build -F ../../singularity_containers/dbresolver/dbresolver.sif dbresolver.def
}

database(){
    echo ""
    echo "Building database..."
    cd microservices/db
    singularity build -F ../../singularity_containers/postgres/db.sif postgres.def
}

dispatcher(){
    echo ""
    echo "Building dispatcher..."
    cd microservices/dispatcher
    singularity build -F ../../singularity_containers/dispatcher/dispatcher.sif dispatcher.def
}

model-changer(){
    echo ""
    echo "Building model-changer..."
    cd microservices/model-changer
    singularity build -F ../../singularity_containers/model-changer/model-changer.sif model-changer.def
}

profile(){
    echo ""
    echo "Building profile-service..."
    cd microservices/profile-service
    singularity build -F ../../singularity_containers/profile-service/profile-service.sif profile-service.def
}

streamer(){
    echo ""
    echo "Building streamer..."
    cd microservices/streamer
    singularity build -F ../../singularity_containers/streamer/streamer.sif streamer.def
}

video-deleter(){
    echo ""
    echo "Building video-deleter..."
    cd microservices/video-deleter
    singularity build -F ../../singularity_containers/video-deleter/video-deleter.sif video-deleter.def
}

video-saver(){
    echo ""
    echo "Building video-file-saver..."
    cd microservices/video-download
    singularity build -F ../../singularity_containers/video-file-saver/video-file-saver.sif video-file-saver.def
}

video-service(){
    echo ""
    echo "Building video-service..."
    cd microservices/video-service
    singularity build -F ../../singularity_containers/video-service/video-service.sif video-service.def
}

frontend(){
    echo ""
    echo "Building frontend..."
    cd frontend
    singularity build -F ../singularity_containers/frontend/frontend.sif frontend.def
}


camera && \
cd $WD && \

dbresolver && \
cd $WD && \

database && \
cd $WD && \

dispatcher &&  \
cd $WD && \

model-changer && \
cd $WD && \

profile && \
cd $WD && \

streamer && \
cd $WD && \

video-deleter && \
cd $WD && \

video-saver && \
cd $WD && \

video-service && \
cd $WD && \

frontend && \
cd $WD
