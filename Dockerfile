FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /usr/src/
WORKDIR /usr/src/
COPY . .
RUN pip install -r requirements/server.txt
RUN apt update
RUN apt install -y gdal-bin python3-gdal
RUN apt install -y python-pip

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
