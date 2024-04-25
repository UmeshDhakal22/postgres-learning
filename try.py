from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Field

load_dotenv()


class Nepal(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    population: int
    capital: str


db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")

database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(database_url)

SQLModel.metadata.create_all(engine)

Session = sessionmaker(engine)

with Session() as session:
    nepal = Nepal(name="Nepal", population=30000000, capital="Kathmandu")
    session.add(nepal)
    session.commit()

    nepal_records = session.query(Nepal).all()
    for record in nepal_records:
        print(record)
