import os

from slack_bolt import App
from dotenv import load_dotenv
from flask import Flask, request
from slack_bolt.adapter.flask import SlackRequestHandler

from events.next_image import next_image
from events.file_share import file_share
from events.send_image import send_image
from events.search_image import search_image
from events.init import init

from services.log import LogService
from services.slack import SlackService
from services.db import run_inital_queries

load_dotenv()

app = App(
    token=os.environ.get('SLACK_BOT_TOKEN'),
    signing_secret=os.environ.get('SLACK_SIGNING_SECRET')
)

token = os.environ['SLACK_BOT_TOKEN']

search_image_command = os.environ.get('SEARCH_IMAGE_COMMAND')

@app.event({
    'type': 'message',
    'subtype': 'file_share'
})
def file_share_event(logger, event):
    LogService.log('EVENT: new message with a file')

    file_share(app, logger, event, token)

@app.event({'type': 'member_joined_channel'})
def file_share_event(logger, event):
    LogService.log('EVENT: init channel')

    init(event)


@app.command(f'/{search_image_command}')
def search_image_event(ack, client, command):
    LogService.log('EVENT: new search event')
    ack()

    workspace = command['team_id']
    channel = command['channel_id']
    image_metadata, query_metric = search_image(command['text'], channel, workspace)

    client.views_open(
        trigger_id=command["trigger_id"],
        view=SlackService.get_image_preview_view(image_metadata, query_metric.id, len(query_metric.query_result_ids) == 1),
    )

@app.action("next")
def next_image_event(ack, body, client):
    LogService.log('EVENT: next')

    next_image(ack, body, client)

@app.view("image_share")
def send_image_event(ack, body, say):
    LogService.log('EVENT: send')

    send_image(ack, body, say)

# TODO: Integrate this queries in sqlalchemy
run_inital_queries()

# Create Flask app
flask_app = Flask(__name__)

# Flask handler
handler = SlackRequestHandler(app)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

@flask_app.route("/healthcheck", methods=["GET"])
def healthcheck():
    return {'statusCode': 200}
