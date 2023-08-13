from dotenv import load_dotenv
load_dotenv()
from database import getCollection
from controller import enrich

if __name__ == "__main__":
    enrich()
    
    print("Press ctrl-c to exit.")