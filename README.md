run a slack app using slack-bolt:
https://github.com/slackapi/bolt-python

# Search image bot

## How to run

### install tesseract
`brew install tesseract`

### install postgres
`brew install postgres`

1. Run database

`docker-compose up -d database`

2. Configure the virtual env

`virtualenv venv`
`source venv/bin/activate`

3. Install requirements

`pip install -r requirements.txt`

4. Run the app
`python app.py`

### test image to text
`python test.py -i test.jpeg`

## ORM

### Create new DB migration

`alembic revision --autogenerate -m "a description"`

## Run the migrations

`alembic upgrade heads`

## Local URL

You need a local public URL for slack to call

1. Install localtunnel
`npm install -g localtunnel`

2. Create a tunnel to your localhost
`lt --port 3000 --subdomain search-image-<name>`

3. You'll get a domain like

` https://search-image-<name>.loca.lt`