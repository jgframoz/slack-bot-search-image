from sqlalchemy import Column, Integer, DateTime, Boolean, ARRAY, String
from migrations.models import Base

class QueryMetric(Base):
    __tablename__ = 'query_metrics'

    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime, nullable=True)

    last_image_index = Column(Integer, nullable=False, default=1)

    successful = Column(Boolean, nullable=False, default=False)

    channel = Column(String, nullable=True)

    workspace = Column(String, nullable=True)

    query_result_ids = Column(ARRAY(Integer), nullable=False, default=[])

    query_string = Column(String, nullable=True)

    def __repr__(self):
        return f"{self.id} | {self.created_at}"

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "id" : self.id,
            "created_at" : self.created_at,
        }