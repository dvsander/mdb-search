import base64
import requests
from sentence_transformers import SentenceTransformer
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

from io import BytesIO
from pymongoarrow.monkey import patch_all
patch_all()

from database import getCollection

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
model = SentenceTransformer('clip-ViT-B-32')

def encodeAndFix(base64img):
   return model.encode(Image.open(BytesIO(base64.b64decode(base64img))),convert_to_numpy=True);

def downloadImageAsBase64(url):
   httpRequest = requests.get(url,headers=headers);
   if (httpRequest.status_code == 200):
       return base64.b64encode(httpRequest.content).decode('ascii');
   return None;

def enrich():

    coll = getCollection()

    # Base images
    default_poster_base64 = downloadImageAsBase64("https://www.csaff.org/wp-content/uploads/csaff-no-poster.jpg");
    default_poster_embeddings = encodeAndFix(default_poster_base64);

    filter = { "poster_blob" : { "$exists": False} }
    for doc in coll.find(filter):

        print("Enriching={}".format(doc["_id"]))
        base64image = default_poster_base64;
        img_encoding = default_poster_embeddings;
        if ("poster" in doc and doc["poster"]) :
            attemptDownloadSuccessful = downloadImageAsBase64(doc["poster"]);
            if (attemptDownloadSuccessful):
                base64image = attemptDownloadSuccessful;
                img_encoding = encodeAndFix(attemptDownloadSuccessful);
        
        coll.update_one({"_id" : doc["_id"]}, {"$set" : { "poster_blob" : base64image, "poster_embedding": img_encoding.tolist()}})
    
    print("Enrichment completed successfully!!!")
