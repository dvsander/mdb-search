import os
import pymongo

secret = os.getenv('MDB_CONN',default="Please provide secret.")

class Repository:

    # Initializing
    def __init__(self):
        self.client = pymongo.MongoClient(secret)
 
    # Deleting (Calling destructor)
    def __del__(self):
        self.client.close()

repository = Repository()

def getCollection():
     return repository.client.get_database("sample_mflix").get_collection("embedded_movies");
