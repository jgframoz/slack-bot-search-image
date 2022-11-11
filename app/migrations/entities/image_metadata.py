from sqlalchemy import Column, Integer, DateTime, String
from migrations.models import Base


class ImageMetadata(Base):
    __tablename__ = 'images_metadata'

    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime, nullable=True)

    image_url = Column(String, nullable=True)

    channel = Column(String, nullable=True)

    workspace = Column(String, nullable=True)

    channel_type = Column(String, nullable=True)

    image_text = Column(String, nullable=True)

    user_id = Column(String, nullable=True)

    message_text = Column(String)

    def __repr__(self):
        return f"{self.id} | {self.created_at} | {self.image_url} | {self.channel} | {self.channel_type} | {self.image_text} | {self.message_text}"

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "id" : self.id,
            "created_at" : self.created_at,
            "image_url" : self.image_url,
            "channel" : self.channel,
            "channel_type" : self.channel_type,
            "image_text" : self.image_text,
            "message_text" : self.message_text 
        }