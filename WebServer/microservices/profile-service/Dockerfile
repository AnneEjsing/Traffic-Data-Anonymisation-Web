FROM python:jessie 
#python version is 3.6.6

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD ./ /app

WORKDIR /app

ENTRYPOINT [ "python3", "-u", "profile-service.py"]
