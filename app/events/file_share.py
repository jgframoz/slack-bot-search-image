import requests
from datetime import datetime
import os
from services.log import LogService

from migrations.entities.image_metadata import ImageMetadata
from ProcessImage import ProcessImage as pi
from services.slack import SlackService
from services.aws import AwsService
from services.image import ImageService
from services.db import session

token = os.environ['SLACK_BOT_TOKEN']

def file_share(app, logger, event, token):
    user, text = event['user'], event['text']
    logger.info(f'The user {user} changed the message to {text}')
    
    upload_files(event)
    

def upload_files(message, is_init=False, c_id=''):
    files = message['files']
    workspace_id = SlackService.extract_workspace_from_image_url(message['files'][0]['url_private'])
    channel_id = c_id or message['channel']
    user_id = message['user']

    for file in files:
        if file['filetype'] not in ['jpg', 'png']:
            LogService.log(f'LOG: can\'t use file of type {file["filetype"]}')
            continue

        message_text = message['text']
        image_id = file['id']
        timestamp = file['timestamp']
        image_name = file['name']
        user_id = message['user']
        is_public = file['is_public']
        public_url_shared = file['public_url_shared']
        image_url = file['url_private_download']
        slack_link = file['permalink']
        channel_id = message['channel'] if not is_init else c_id
        channel_type = message['channel_type']

        # download file
        r = requests.get(image_url, headers={'Authorization': 'Bearer %s' % token})
        file_data = r.content   # get binary content

        # save file to disk
        ImageService.save_image(image_name, file_data)

        # Make image public with slack API
        # TODO: remove to use slack images without S3
        s3_image_url = AwsService.upload_image(workspace_id, channel_id, image_name)

        text = pi.image_to_text(image_name)

        image = ImageMetadata(
            created_at = datetime.fromtimestamp(timestamp),
            image_url = s3_image_url,
            channel = channel_id,
            workspace=workspace_id,
            channel_type = channel_type,
            image_text = text,
            message_text = message_text,
            user_id = user_id
        )

        session.add(image)

        os.remove(image_name)
    
    session.commit()