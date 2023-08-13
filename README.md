# mdb-search

## Set-up

Spin up a MongoDB Atlas cluster and load the sample dataset.
Ensure database access and network access allow you to make a connection to the database.
Note down the connection string.

Create a file `.env` in the project structure and put the connection string in:

    MDB_CONN="mongodb+srv://..."


In Atlas, in the cluster view "Search" tab, enter the following JSON configuration. Use the 'default' index name and ensure to make it on the `embedded_movies` collection. It will enable dynamic full text search on fields, as well as enable the vector search indexes.

    {
    "mappings": {
        "dynamic": true,
        "fields": {
        "plot_embedding": {
            "dimensions": 1536,
            "similarity": "cosine",
            "type": "knnVector"
        },
        "poster_embedding": {
            "dimensions": 512,
            "similarity": "cosine",
            "type": "knnVector"
        }
        }
    }
    }

This is a Flask Python3 web-app.
You need Python3 and pip.
After installing python3, run

    pip install -r requirements

## The vector search embeddings

Currently there are 3483 movie documents in the embedded_movies collection in the sample_mflix database.

Run the `util.py` utility with command line. It will download pictures for movies and for those pictures create the embeddings using the `clip-ViT-B-32` model. This might take a while. Could be optimized with multithreading locally and batch insert_manys. The logic will only process documents without embedding, this process can be resumed.

    python util.py

You could also download a `mongoexport` of this collection and `mongoimport` it into yours.

## Run the app

Start the Flask app

    python app.py

You can access the web app at `http://localhost:5000`.
You can then use the full text search from the input field to find 'any' random set of movies.
To use the vector based search 'similar movie posters', click the button next to each picture and see what happens :)

Trust the ML and the model. Can you guess why these pictures are similar?

Cosine is recommended by the model authors. What happens when using other knn similarity?
