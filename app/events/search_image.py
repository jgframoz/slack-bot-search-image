from typing import Tuple
from sqlalchemy import text
from services.db import engine
from migrations.entities.image_metadata import ImageMetadata
from migrations.entities.query_metrics import QueryMetric
from services.db import session

from datetime import datetime

N_RECORDS = 3

def search_image(query_string, channel, workspace) -> Tuple[ImageMetadata, QueryMetric]:
    sql_text = text(f"SELECT *, ts_rank(search_vector, websearch_to_tsquery('{query_string}')) as rank FROM images_metadata WHERE workspace = '{workspace}' ORDER BY rank desc LIMIT {N_RECORDS};")
    results = engine.execute(sql_text)

    result_list = []

    for r in results:
        result_list.append(dict(r))

    query_metric = QueryMetric(
        created_at = datetime.now(),
        query_result_ids = map(lambda r: r['id'], result_list),
        channel = channel,
        workspace=workspace,
        query_string=query_string
    )

    session.add(query_metric)
    session.commit()

    return result_list[0], query_metric