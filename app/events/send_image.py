from services.query_metrics import QueryMetricsService
from services.slack import SlackService, BlockType
from services.image_metadata import ImageMetadataService
from services.db import session


def send_image(ack, body, say):
    ack(response_action="clear")

    # Get the query metric row
    query_metric_id = body['view']['private_metadata']
    query_metric = QueryMetricsService.get(query_metric_id)

    # Set user query as successful
    query_metric.successful = True

    session.commit()

    # Get URL of current image being displayed
    image_metadata_id = QueryMetricsService.get_current_image_metadata_id(query_metric)
    image_metadata = ImageMetadataService.get(image_metadata_id)

    blocks = [
        SlackService.get_message_block(BlockType.IMAGE, {
            'title': "Here's your image!",
            'image_url': image_metadata.image_url,
            'alt_text': 'your image'
        })
    ]

    say(
        channel=query_metric.channel,
        blocks=blocks
    )