import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


load_dotenv()

# TODO: Delete, this should go on an Alembic migration
def run_inital_queries():
    engine.execute('ALTER TABLE images_metadata ADD COLUMN IF NOT EXISTS search_vector tsvector;')
    engine.execute('CREATE INDEX IF NOT EXISTS ix_search_vector ON images_metadata USING GIN (search_vector);')
    engine.execute("CREATE OR REPLACE FUNCTION update_image_metadata_content() RETURNS trigger AS $$ BEGIN new.search_vector := setweight(to_tsvector(coalesce(new.message_text, '')), 'A') || setweight(to_tsvector(coalesce(new.image_text, '')), 'B'); return new; END $$ LANGUAGE plpgsql;")
    engine.execute("DO $$ BEGIN IF NOT EXISTS(SELECT * FROM information_schema.triggers WHERE event_object_table = 'images_metadata' AND trigger_name = 'image_search_vector_update') THEN CREATE TRIGGER image_search_vector_update BEFORE INSERT OR UPDATE ON images_metadata FOR EACH ROW EXECUTE PROCEDURE update_image_metadata_content(); END IF ; END; $$")

def get_db_connection_string() -> str:
    DB_USER     = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST     = os.environ.get('DB_HOST')
    DB_PORT     = os.environ.get('DB_PORT')
    DB_NAME     = os.environ.get('DB_NAME')

    return f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(get_db_connection_string())

session_factory = sessionmaker(bind=engine)
session = scoped_session(session_factory)
# or make it a Tornado Application property

session.begin()

