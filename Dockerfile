# start by pulling the python image
FROM python:3.9-slim

ARG APP=app.py
ARG ENV=production

RUN apt-get update && apt-get -y install libgl1 libgtk2.0-dev

RUN apt install -y tesseract-ocr

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install --upgrade pip
RUN pip install --no-cache-dir numpy==1.23.0
RUN pip install --no-cache-dir slack_bolt
RUN pip install --no-cache-dir pytesseract
RUN pip install --no-cache-dir alembic
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY app /app
COPY .env.production .env

ENV FLASK_APP=$APP
ENV FLASK_ENV=$ENV

RUN alembic upgrade heads

CMD ["flask", "run", "-p", "3000", "-h", "0.0.0.0"]
