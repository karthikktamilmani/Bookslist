from pymongo import MongoClient
from bson import json_util
from flask_cors import CORS
import logging
from flask import request, jsonify, Flask
import json
import time
import base64
from datetime import datetime
import re
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
CORS(app)
client = MongoClient('mongodb://karthi:secret@54.152.185.224/myDB')
db = client['myDB']
@app.route('/getBooks')
def getBooks():
    response_json = {}
    try:
        ##
        queryString = request.args.get("query")
        type = request.args.get("type")
        searchQuery = re.compile(".*"+queryString+".*",re.IGNORECASE)
        bookDataCursor = db.bookData.find({ type : searchQuery } , {"Title":1 , "Author":1 , "_id": 0 } )
        resultObject = json_util.dumps(bookDataCursor)
        response_json = resultObject
        if len(resultObject) > 2:
            #successful search
            writeSuccessfulResult(resultObject)

        app.logger.debug(len(resultObject))
        app.logger.debug(queryString)
        app.logger.debug(type)

    except Exception as e:
        app.logger.debug(e)
    return response_json

def writeSuccessfulResult(resultObj):
    try:
        with open("Catalogue.txt", 'a+') as f:
            f.write(resultObj)
    except Exception as e:
        app.logger.debug(e)

if __name__ == "__main__":
    app.run(debug=True,port=5002,host="0.0.0.0")

