FROM python:jessie 
#python version is 3.6.6

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

ADD ./ /app

WORKDIR /app

ENTRYPOINT [ "python", "-u", "change_ml.py", "--urls", "http://*:5000"]