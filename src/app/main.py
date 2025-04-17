from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from sentence_transformers import SentenceTransformer

class Request(BaseModel):
    keyword: str

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/hybrid/")
def hybrid_search(req: Request):

    # Request cleaning
    if req.keyword == "":
        return {"Invalid Request - A non-empty keyword must be specified"}
       
    #  Create the representation of the search term provided - will be used to compare against the vector representations
    model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')
    embedding = model.encode(req.keyword)

    # Establish connection to the database
    conn_url = 'postgresql+psycopg2://admin:secret@postgres-db/my_database'
    engine = create_engine(conn_url)

    ## [IMPLEMENTATION NOT FINISHED] - Execute the combined Vector and semantic searches
    # with engine.connect() as con:
    #     hybridQuery = """SELECT
    #     searches.id,
    #     searches.description,
    #     sum(rrf_score(searches.rank)) AS score
    #     FROM ((SELECT id, content, rank() OVER (ORDER BY $1 <=> vector_representation) AS rank FROM magazine_content ORDER BY $1 <=> vector_representation LIMIT 40
	#     )
	#     UNION ALL
	#     (SELECT id, content, rank() OVER (ORDER BY ts_rank_cd(to_tsvector(content), plainto_tsquery('req.keyword')) DESC) AS rank
	# 	FROM magazine_content
	# 	WHERE
	# 	plainto_tsquery('english', 'req.keyword') @@ to_tsvector('english', content)
	# 	ORDER BY rank
	# 	LIMIT 40
	#     )
    #     ) searches
    #     GROUP BY searches.id, searches.description
    #     ORDER BY score DESC
    #     LIMIT 10;"""

    #     results = con.execute(text(hybridQuery))

    return {"You searched for": req.keyword}