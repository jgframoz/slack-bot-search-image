from services.query_metrics import QueryMetricsService
from services.image_metadata import ImageMetadataService
from services.slack import SlackService
from services.db import session


def next_image(ack, body, client):
    ack()

    query_metric_id = body['view']['private_metadata']
    query_metric = QueryMetricsService.get(query_metric_id)

    image_metadata_id = QueryMetricsService.get_next_image_metadata_id(query_metric)
    image_metadata = ImageMetadataService.get(image_metadata_id)

    current_view_id = body["view"]["id"]
    current_view_hash = body["view"]["hash"]

    is_last_image = QueryMetricsService.is_last_image(query_metric)

    # Update modal
    client.views_update(
        view_id=current_view_id,
        hash=current_view_hash,
        view=SlackService.get_image_preview_view(image_metadata.__dict__, query_metric_id, is_last_image)
    )

    # Update last image index used
    query_metric.last_image_index = query_metric.last_image_index + 1
    session.commit()