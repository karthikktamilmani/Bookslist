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

@app.route('/writeLog')
def writeLog():
    response_json = {}
    response_json["status"] = "error"
    try:
        ##
        queryString = request.args.get("query")
        writeSearchLog(queryString)
        response_json["status"] = "ok"


    except Exception as e:
        app.logger.debug(e)
    return response_json

def writeSearchLog(searchQuery):
    try:
        with open("Search_Log.txt", 'r+') as f:
            app.logger.debug("read")
            # app.logger.debug(f.read())
            dummyEntry = f.read()
            if len(dummyEntry) > 2:
                # app.logger.debug(f.read())
                entireFile = json.loads(dummyEntry)
            else:
                entireFile = {}
        with open("Search_Log.txt", 'a+') as f:
            app.logger.debug("before")
            app.logger.debug(entireFile)
            now = datetime.now()
            current_time = now.strftime("%d/%m/%Y %H:%M:%S")
            if searchQuery in entireFile:
                keyLog = entireFile[searchQuery]
                timeList = keyLog["time"]
                timeList.append(current_time)
                keyLog["count"] = len(timeList)
            else:
                timeList = []
                keyLog = {}
                timeList.append(current_time)
                keyLog["count"] = len(timeList)
                keyLog["time"] = timeList
                entireFile[searchQuery] = keyLog
            f.truncate(0)
            app.logger.debug("ssss")
            app.logger.debug(entireFile)
            f.write(json.dumps(entireFile))
    except Exception as e:
        app.logger.debug("Exception:")
        app.logger.debug(e)



if __name__ == "__main__":
    app.run(debug=True,port=5003,host='0.0.0.0')

