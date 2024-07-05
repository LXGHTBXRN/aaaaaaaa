from sqlalchemy import create_engine
from main import Base, DATABASE_URL

def create_db_and_tables():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_db_and_tables()
