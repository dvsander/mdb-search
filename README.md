# mdb-search

Atlas Vector search adds vector database capabilities to MongoDB Atlas.

MongoDB is a very popular document database giving you powerful transactional and analytical capabilities on structured and semi-structured data in a JSON-like structure, with a plethora of database indexing capabilities and aggregation/analytics.

Atlas Search was added, embedding relevance search and scoring capabilities based on open-source Lucene indexes.

This year, Atlas Vector Search allows you to store and manage unstructured data, such as text, images, or audio, in vector embeddings (high-dimensional vectors) to make it easy to find and retrieve similar objects quickly.

In this project I combine operational data about movies, with a search bar for relevance search, together with Vector Search allowing to find similar movies based on the movie poster. For this, I use the `clip-ViT-B-32` model on the images and store the embeddings, as well as the picture inside my database. I choose to store everything inside the same document: the metadata, the pictures as base64, the embeddings. This is an excellent use of a document store and does not need additional query languages or services to operate. Everything is accessible with one API.

Some hilarious results I must say. Some would call it artificial intelligence AI, I call it clever use of statistics.

## Set-up

Create a free cluster on MongoDB Atlas. Note this has 512MB data size limitation and will host around 2924 movies. Currently there are 3483 movie documents in the embedded_movies collection in the sample_mflix database and 21k+ movies in movies. You could run this example on the either collection if you want. If you have some credits feel free to run a paid cluster tier with larger disks.

Ensure database access and network access allow you to make a connection to the database. Note down the connection string.

## Environment variables

Create a file `.env` in the project structure and put the connection string in:

    MDB_CONN="mongodb+srv://..."

when you plan on using OpenAI embedding for similar text search, add your API key:

    OPENAI_API_KEY=



## Install Python

You need Python3 and pip.
After installing python3, run

    pip install -r requirements

### Option 1: Just load the mongodump

From the project directory, run the `mongorestore` to restore the `sample_mflix and `embedded_movies collection:

    mongorestore --uri="mongodb+srv://..."

### Option 2: Create the vector search embeddings yourself on any collection

Load the sample dataset from MongoDB Atlas. Run the `util.py` utility with command line. It will download pictures for movies and for those pictures create the embeddings using the `clip-ViT-B-32` model. This might take a while. Could be optimized with multithreading locally and batch insert_manys. The logic will only process documents without embedding, this process can be resumed.

    python util.py

### Enable the relevance search and vector search in MongoDB Atlas

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

## Run the App

This is a Flask Python3 web-app.

Start the Flask app

    flask --app app run

You can access the web app at `http://localhost:5000`.

You can then use the full text search from the input field to find 'any' random set of movies.
To use the vector based search 'similar movie posters', click the button next to each picture and see what happens :)

Trust the ML and the model. Can you guess why these pictures are similar?

Cosine is recommended by the model authors. What happens when using other knn similarity?
