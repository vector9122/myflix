FROM python:3.10.4

EXPOSE 9000

COPY ./requirements.txt /flix_go/requirements.txt
WORKDIR /flix_go
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /flix_go