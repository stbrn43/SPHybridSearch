-- Enable the uuid-ossp extension (needed to generate UUIDs)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- Enable the pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Ideally would use an ORM for this that allows us to run migrations against the DB to initialise the entities, will 
-- get round to this if I have time!
CREATE TABLE magazine
(
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255),
    author VARCHAR(255),
    publication_date DATE,
    category VARCHAR(255)
);

CREATE TABLE magazine_content
(
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    magazine_id UUID REFERENCES magazine(id) ON DELETE SET NULL,
    content VARCHAR(4000),
    vector_representation vector(384)
);

-- Function for calculating the Reciprocal Ranked Fusion Score
-- Approach borrowed from https://jkatz05.com/post/postgres/hybrid-search-postgres-pgvector/
-- The smaller the value of rrf_k, the higher it scores higher-ranked results
CREATE OR REPLACE FUNCTION rrf_score(rank int, rrf_k int DEFAULT 20)
RETURNS numeric
LANGUAGE SQL
IMMUTABLE PARALLEL SAFE
AS $$
    SELECT COALESCE(1.0 / ($1 + $2), 0.0);
$$ ;

--Seed the magazine table with some initial data - The magazine_content table will be seeded elsewhere
INSERT INTO magazine (id, title, author, publication_date, category) 
VALUES ('efb0d7a0-b52a-4b94-ba26-30367d641d6a', 'Vectors Monthly', 'Croc', '2025-04-15', 'Science'),
       ('3cd6d147-ef9c-4440-9eb3-6692f97f6ee0', 'Charmed Items', 'Bee Group', '2025-04-13', 'Paranormal'), 
       ('adc7f630-00dc-4f9e-8b90-2725672b9dae', 'Espionage', 'KamelEON', '2025-04-03', 'True Crime');