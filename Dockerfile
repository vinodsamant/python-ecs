FROM python:3.7

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /usr/src/app
COPY . .

RUN pip install -r requirements/server.txt
RUN apt update
RUN apt install -y gdal-bin python3-gdal
RUN apt install -y python-pip

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
