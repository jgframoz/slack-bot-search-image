from sqlalchemy import Column, DateTime, String, Integer, UniqueConstraint
from migrations.models import Base

class Workspace(Base):
    __tablename__ = 'workspaces'

    id = Column(Integer, primary_key=True)

    workspace_identifier = Column(String)

    created_at = Column(DateTime, nullable=True)

    __table_args__ = (UniqueConstraint('workspace_identifier'),)


    def __repr__(self):
        return f"{self.id} | {self.created_at}"

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "id" : self.id,
            "created_at" : self.created_at,
            "workspace_identifier": self.workspace_identifier,
        }