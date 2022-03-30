FROM ubuntu:21.10
RUN apt-get update -y
RUN apt-get install -y pymol
WORKDIR /code
COPY requirements.txt .
RUN apt-get -y install python3-pip
RUN pip install -r requirements.txt
COPY . .


