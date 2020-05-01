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

@app.route('/getNotes')
def getNotes():
    response_json = {}
    try:
        ##
        queryString = request.args.get("query")
        response_json = getNotesFromFromFile(queryString)
        # app.logger.debug(len(resultObject))
        app.logger.debug(queryString)
        app.logger.debug(type)

    except Exception as e:
        app.logger.debug(e)
    return json.dumps(response_json)

@app.route('/submitNotes')
def submitNotes():
    response_json = {}
    response_json["status"] = "error"
    try:
        ##
        queryString = request.args.get("query")
        notes = request.args.get("notes")
        #
        writeNotes(queryString,notes)
        response_json["status"] = "ok"
    except Exception as e:
        app.logger.debug(e)
    return response_json

def getNotesFromFromFile(searchQuery):
    result = []
    try:
        with open("User_Notes.txt", 'r+') as f:
            app.logger.debug("read")
            # app.logger.debug(f.read())
            dummyEntry = f.read()
            if len(dummyEntry) > 2:
                # app.logger.debug(f.read())
                entireFile = json.loads(dummyEntry)
                result = entireFile[searchQuery]
    except Exception as e:
        app.logger.debug(e)
    return result

def writeNotes(searchQuery,notes):
    try:
        with open("User_Notes.txt", 'r+') as f:
            app.logger.debug("read")
            # app.logger.debug(f.read())
            dummyEntry = f.read()
            if len(dummyEntry) > 2:
                # app.logger.debug(f.read())
                entireFile = json.loads(dummyEntry)
            else:
                entireFile = {}
        with open("User_Notes.txt", 'a+') as f:
            app.logger.debug("before")
            app.logger.debug(entireFile)
            if searchQuery in entireFile:
                timeList = entireFile[searchQuery]
                timeList.append(notes)
            else:
                timeList = []
                timeList.append(notes)
                entireFile[searchQuery] = timeList
            f.truncate(0)
            app.logger.debug(entireFile)
            f.write(json.dumps(entireFile))
    except Exception as e:
        app.logger.debug("Exception:")
        app.logger.debug(e)

if __name__ == "__main__":
    app.run(debug=True,port=5004,host='0.0.0.0')

