from faker import Faker
import psycopg2
from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker

# Create random textual data
fake = Faker()
randomSentences = [fake.sentence(nb_words=50) for i in range(0,50_000)]

# Generate the vector embedding for each of the sentences created by Faker
model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')
embeddings = model.encode(randomSentences)

# Seed the database with data
conn_url = 'postgresql+psycopg2://admin:secret@postgres-db/my_database'
engine = create_engine(conn_url)

insertSql = 'INSERT INTO magazine_content (magazine_id, content, vector_representation) VALUES (:magazineId, :content, :embedding)'
with engine.connect() as con:
        for content, embedding in zip(randomSentences, embeddings):
                con.execute(text(insertSql), {'magazineId': 'efb0d7a0-b52a-4b94-ba26-30367d641d6a', 'content': content, 'embedding': embedding.tolist()})

con.close()