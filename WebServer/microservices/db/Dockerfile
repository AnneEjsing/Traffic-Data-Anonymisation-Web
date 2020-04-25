FROM python:jessie 
#python version is 3.6.6

COPY requirements.txt requirements.txt

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

ADD ./*.py /app/

WORKDIR /app

ENTRYPOINT [ "python3", "-u", "dbresolver.py"]