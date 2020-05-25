#!/bin/bash
#This script builds all singularity containers and puts all images in folder singularity_containers

#Making folders
mkdir -p singularity_containers
mkdir -p singularity_containers/camera-service
mkdir -p singularity_containers/dbresolver
mkdir -p singularity_containers/postgres
mkdir -p singularity_containers/dispatcher
mkdir -p singularity_containers/model-changer
mkdir -p singularity_containers/profile-service
mkdir -p singularity_containers/streamer
mkdir -p singularity_containers/video-deleter
mkdir -p singularity_containers/video-file-saver
mkdir -p singularity_containers/video-service
mkdir -p singularity_containers/frontend


echo "Performing build process as root"
sudo bash perform_singularity_build.sh
