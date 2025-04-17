# Introduction
- This is an (incomplete) solution to perform a Hybrid Search of Magazine Content, using the pgvector extension for Postgres. Postgres was chosen
- because it is a strongly-established relational database with additional vector capabilities available through extension, making it a strong contender
- for the "Hybrid" solution required here. FastAPI is used to provide an endpoint to perform a new search.

- The implementation of the Hybrid Search itself is incomplete, but I was following the implementation at https://jkatz05.com/post/postgres/hybrid-search-postgres-pgvector/ as
- guidance, with the aim of fine tuning it once I got the basic implementation working

# Step 1 - Prerequisites
- A bash terminal (i.e, GitBash)
- VSCode (Not technically essential but was used for development)
- Postman (and Postman account)
- Docker (Docker must be running)

# Step 2 - Initialising the Database
- Build the DB Container with              > docker-compose build db
- Then deploy the DB to the container with > docker-compose up db -d
- Connect to DB in terminal with           > docker exec -it postgres-db psql -U admin -d my_database  (i.e, docker exec -it [container-name] psql -U [username] -d [db-name])
- List Databases     -   #my_database-# \l
- List Tables        -   #my_database-# \dt;
- Verify data exists -   #my-database-# SELECT * FROM magazine;

# Step 3 - Build and Run the API
- Build the API Container with             > docker-compose build api 
                                             [Important] (Packages are fairly large, first build can take around 20 minutes!)                                      
- Deploy the API to the container with     > docker-compose up api -d
- Don't forget the -d (detached) flag from the above command or it won't run on the container properly
- Seed the Magazine Content DB Table by running   > docker exec -it api python ./seedDatabase.py
                                                    [Important] This step does not currently work - the script runs but does not insert anything
- Navigate to localhost:8000 in your browser, ensure that the API can actually be reached

# Step 4 - Executing 
- Ensure you have Postman installed locally
- Create a new POST Request in Postman, pointed at http://localhost:8000/hybrid
- In the request body, choose "raw", and enter a JSON object of:
  {
     "keyword": "YOUR_SEARCH_TERM_HERE",
  }

# Troubleshooting
- If you need to reinitialise the database entirely so that the init.sql script gets re-run, run the following
   - docker-compose down db -v
   - docker-compose build db
   - docker-compose up db -d
