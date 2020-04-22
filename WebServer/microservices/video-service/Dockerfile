FROM python:jessie 
#python version is 3.6.6

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

ADD ./*.py /app/

WORKDIR /app

ENTRYPOINT [ "python3", "-u", "video-service.py"]
