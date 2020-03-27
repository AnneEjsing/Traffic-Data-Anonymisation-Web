FROM python:jessie 
#python version is 3.6.6

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

ADD ./ /app

WORKDIR /app

ENTRYPOINT [ "python", "-u", "video_download.py", "--urls", "http://*:5001"]