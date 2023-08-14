import os
from flask import Flask, render_template, send_from_directory, request
from bson.objectid import ObjectId
from dotenv import load_dotenv
load_dotenv()

from database import getCollection
from controller import getOpenAIEmbedding

app = Flask(__name__)

@app.route("/search", methods=['GET', 'POST'])
def search():
    docs = []
    searchInput = request.form['searchInput']
    searchOptions = request.form['searchOptions']

    if (searchOptions == 'relevance' )
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

    elif (searchOptions == 'similarText' )
        embedding = getOpenAIEmbedding(searchInput)
        coll = getCollection()
        docs = coll.aggregate([
            {
                "$search": {
                    "knnBeta": {
                        "vector": embedding,
                        "path": "plot_embedding",
                        "k": 20
                    }
                }
            }
        ])

    return render_template("home.html",movies=docs, searchInput=searchInput, searchOptions=searchOptions)

@app.route("/similar/<movieId>")
def findSimilarMoviesTos(movieId):
    coll = getCollection()

    doc = coll.find_one({"_id" : ObjectId(movieId)})

    docs = coll.aggregate([
        {
            "$search": {
                "index": "default",
                "knnBeta": {
                    "vector": doc["poster_embedding"],
                    "path": "poster_embedding",
                    "k": 20
                }
            }
        }
    ])
    return render_template("home.html",movies=docs,similarto=doc,searchOptions='similarImage')

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