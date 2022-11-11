from services.db import session
from migrations.entities.image_metadata import ImageMetadata


class ImageMetadataService:
    @staticmethod
    def get(id) -> ImageMetadata:
        return session.query(ImageMetadata).filter(ImageMetadata.id == id).one()