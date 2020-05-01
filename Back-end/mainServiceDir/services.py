from pymongo import MongoClient
from bson import json_util
from flask_cors import CORS
import logging
from flask import request, jsonify, Flask
import requests
import json
import time
import base64
from datetime import datetime
import re
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
CORS(app)
# client = MongoClient(port=27017)
# db = client['myDB']
@app.route('/getBooks')
def getBooks():
    response_json = {}
    try:
        data = request.get_json()
        ##
        queryString = request.args.get("query")
        type = request.args.get("type")
        requests.get("http://search-service:5003/writeLog?query="+queryString)
        #app.logger.debug(response.json())
        search_response = requests.get("http://catalogue-service:5002/getBooks?query=" + queryString + "&type=" + type)
        notes_response = requests.get("http://notes-service:5004/getNotes?query=" + queryString)
        response_json["books"] = search_response.json()
        response_json["notes"] = notes_response.json()
        #
        # searchQuery = re.compile(".*"+queryString+".*",re.IGNORECASE)
        # bookDataCursor = db.bookData.find({ type : searchQuery } , {"Title":1 , "Author":1 , "_id": 0 } )
        # resultObject = json_util.dumps(bookDataCursor)
        # response_json["books"] = json.loads(resultObject)
        # writeSearchLog(queryString)
        # if len(resultObject) > 2:
        #     #successful search
        #     writeSuccessfulResult(resultObject)
        # response_json["notes"] = getNotes(queryString)
        # app.logger.debug(len(resultObject))
        # app.logger.debug(queryString)
        # app.logger.debug(type)

    except Exception as e:
        app.logger.debug(e)
    return response_json

@app.route('/submitNotes')
def submitNotes():
    response_json = {}
    response_json["status"] = "error"
    try:
        data = request.get_json()
        ##
        queryString = request.args.get("query")
        notes = request.args.get("notes")
        #
        notes_response = requests.get("http://notes-service:5004/submitNotes?query=" + queryString + "&notes=" + notes)
        response_json = notes_response.json()
        #
        # writeNotes(queryString,notes)
        # response_json["status"] = "ok"
    except Exception as e:
        app.logger.debug(e)
    return response_json


if __name__ == "__main__":
    app.run(debug=True,port=5001,host='0.0.0.0')

