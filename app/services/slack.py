from enum import Enum
import os

from slack_sdk import WebClient

from migrations.entities.image_metadata import ImageMetadata
from migrations.entities.query_metrics import QueryMetric


client = WebClient(token=os.environ.get('SLACK_BOT_TOKEN'))

class BlockType(Enum):
    IMAGE = 'image'
    SECTION = 'section'
    ACTIONS = 'actions'

class SlackService:
    @staticmethod
    def get_message_block(type, params):
        if type == BlockType.IMAGE:
            return {
                "type": "image",
                "image_url": params['image_url'],
                "alt_text": params['alt_text']
            }

        elif type == BlockType.SECTION:
            return {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": params['text']
                }
            }
            
        elif type == BlockType.ACTIONS:
            elements = []
            for param in params['buttons']:
                elements.append({
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": param['text']
                    },
                    "style": param['style'],
                    "action_id": param['value']
                })

            return {
                "type": "actions",
                "elements": elements
            }

        return {}

    # Url will be like https://files.slack.com/files-pri/<workspaceId>-<fileId>/<file_name>
    @staticmethod
    def extract_workspace_from_image_url(url: str):
        return url.split('/')[-2].split('-')[0]

    def get_image_preview_view(image_metadata: dict, query_metrics_id, is_last_image: bool):
        image_url = image_metadata['image_url']
        username = client.users_info(user=image_metadata['user_id'])['user']['name']
        channel_name = client.conversations_info(channel=image_metadata['channel'])['channel']['name']
        image_submition_ts = image_metadata['created_at'].date()

        blocks = [
            SlackService.get_message_block(BlockType.SECTION, {'text': f'@{username} shared this image on #{channel_name} on {image_submition_ts}'}),
            SlackService.get_message_block(BlockType.IMAGE, {
                'image_url': image_url,
                'alt_text': 'your image'
            })
        ]

        # Don't show "next" button if there's no more images
        if not is_last_image:
            blocks.append(
                SlackService.get_message_block(
                    BlockType.ACTIONS, {
                    'buttons': [
                        {
                            'text': 'Next',
                            'style': 'danger',
                            'value': 'next'
                        }
                    ]
            }))

        return {
            "type": "modal",
            "callback_id": "image_share",
            "title": {
                "type": "plain_text",
                "text": "Is this your image?",
            },
            "submit": {
                "type": "plain_text",
                "text": "Send"
            },
            # Use this field to save the id of the query metrics entry
            "private_metadata": str(query_metrics_id),
            "blocks": blocks,
        }
