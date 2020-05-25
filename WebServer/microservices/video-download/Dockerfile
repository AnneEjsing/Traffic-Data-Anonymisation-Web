FROM borda/docker_python-opencv-ffmpeg

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install -y ffmpeg

ADD ./*.py /app/

WORKDIR /app

ENTRYPOINT [ "python3", "-u", "video_file_saver.py"]