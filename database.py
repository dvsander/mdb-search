import os
import pymongo

CONN = os.getenv('MDB_CONN',default="Please provide connection string MDB_CONN.")
DB = os.getenv('DB',default="Please provide DB.")
COLL = os.getenv('COLL',default="Please provide COLL.")

class Repository:

    # Initializing
    def __init__(self):
        self.client = pymongo.MongoClient(CONN)
 
    # Deleting (Calling destructor)
    def __del__(self):
        self.client.close()

repository = Repository()

def getCollection():
     return repository.client.get_database(DB).get_collection(COLL);
