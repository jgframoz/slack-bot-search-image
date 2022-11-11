from services.db import session
from migrations.entities.query_metrics import QueryMetric

class QueryMetricsService:
    @staticmethod
    def get(id) -> QueryMetric:
        return session.query(QueryMetric).filter(QueryMetric.id == id).one()


    @staticmethod
    def get_current_image_metadata_id(query_metric: QueryMetric) -> int:
        # We save index from 1..n, needs to be normalized to 0..n-1
        index = query_metric.last_image_index - 1

        return query_metric.query_result_ids[index]

    @staticmethod
    def get_next_image_metadata_id(query_metric: QueryMetric) -> int:
        # We save index from 1..n, needs to be normalized to 0..n-1
        index = query_metric.last_image_index

        return query_metric.query_result_ids[index]

    @staticmethod
    def is_last_image(query_metric: QueryMetric) -> bool:
        """
        Returns true if the current image is the 
        last image available from the query
        """
        return query_metric.last_image_index == len(query_metric.query_result_ids) - 1
