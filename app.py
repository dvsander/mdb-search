import os
from flask import Flask, render_template, send_from_directory, request, redirect
from bson.objectid import ObjectId
from dotenv import load_dotenv
load_dotenv()

from database import getCollection
from controller import getOpenAIEmbedding
import requests
import base64
from sentence_transformers import SentenceTransformer
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from io import BytesIO
import openai

app = Flask(__name__)

model = SentenceTransformer('clip-ViT-B-32')
openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route("/search", methods=['GET', 'POST'])
def search():
    docs = []
    searchInput = request.form['searchInput']
    searchOptions = request.form['searchOptions']
    generateDescription = request.form.get("generateDescription")
    
    print(generateDescription)

    if (searchOptions == 'relevance' ):
        coll = getCollection()
        docs = coll.aggregate([
            {
                "$search": {
                    "text": {
                        "query": searchInput,
                        "path": ["plot", "full_plot", "title"],
                        "fuzzy": {
                            "maxEdits" : 2
                        }
                    }
                }
            },{
                "$limit": 20
            }
        ])
        return render_template("home.html",movies=docs, searchInput=searchInput, searchOptions=searchOptions)

    elif (searchOptions == 'semanticText' ):
        embedding = getOpenAIEmbedding(searchInput)
        coll = getCollection()

        docs = coll.aggregate([
            { "$vectorSearch": {
                "index": "default",
                "queryVector": embedding,
                "path": "plot_embedding",
                "numCandidates": 100,
                "limit": 21
            }}
        ])


        docs = [d for d in docs]

        if generateDescription is not None:
            first_three = docs[0:3]
            ctx = [ {"role": "system", "content": "Film %d // Title: %s // Plot: %s" % (i, d["title"], d["plot"])} for i, d in enumerate(first_three) ]

            messages = [{"role": "system", "content": "You are a movie selection assistant. Every query you get is about finding movies. You will be given a question and a list of movies that match. Answer by giving a short paragraph recapitulating the question, then suggesting each of the provided movies by paraphrasing the provided plot and highlighting how it corresponds to the question. Very important: mention all the movies listed below. Do not, under any circumstance, mention any movie that is not in the following list. It is critically important that you do not answer questions not related to movies."}]
            messages = messages + ctx
            messages = messages + [ {"role": "user", "content": "Question: %s" % searchInput} ]
            completion = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            desc = completion.choices[0].message.content
        else:
            desc = None
        return render_template("home.html",movies=docs, searchInput=searchInput, searchOptions=searchOptions, desc=desc)

    

@app.route("/new", methods=["POST"])
def new():
    title = request.form["title"]
    plot = request.form["plot"]
    poster = request.form["poster"]

    poster_b64 = downloadImageAsBase64(poster)
    poster_embedding = model.encode(Image.open(BytesIO(base64.b64decode(poster_b64))), convert_to_numpy=True)

    doc = {
        "title": title,
        "plot": plot,
        "demoAdded": True,
        "poster_blob": poster_b64,
        "poster_embedding": poster_embedding.tolist()
    }

    getCollection().insert_one(doc)
    
    return redirect("/", code=302)

def downloadImageAsBase64(url):
   headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
   httpRequest = requests.get(url,headers=headers)
   if (httpRequest.status_code == 200):
       return base64.b64encode(httpRequest.content).decode('ascii')
   return None

@app.route("/similarImage/<movieId>")
def findSimilarPostersTos(movieId):
    coll = getCollection()

    doc = coll.find_one({"_id" : ObjectId(movieId)})

    docs = coll.aggregate([
        {"$vectorSearch": {
            "index": "default",
            "path": "poster_embedding",
            "queryVector": doc["poster_embedding"],
            "numCandidates": 200,
            "limit": 21
        }}
    ])
    return render_template("home.html",movies=docs,similarto=doc,searchOptions='similarImage')

@app.route("/similarText/<movieId>")
def findSimilarMoviesTos(movieId):
    coll = getCollection()

    doc = coll.find_one({"_id" : ObjectId(movieId)})

    docs = coll.aggregate([
        {"$vectorSearch": {
            "index": "default",
            "path": "plot_embedding",
            "queryVector": doc["plot_embedding"],
            "numCandidates": 200,
            "limit": 21
        }}
    ])
    return render_template("home.html",movies=docs,similarto=doc,searchOptions='similarText')

@app.route("/")
def hello_world():
    coll = getCollection()
    docs = coll.find({}, limit=20)

    return render_template("home.html",movies=docs)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)