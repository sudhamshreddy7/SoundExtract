import os, gridfs, pika, json
from flask import Flask, request, send_file
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util
from bson.objectid import ObjectId
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
server = Flask(__name__)

mongo_video = PyMongo(server, uri="mongodb://host.minikube.internal:27017/videos")

mongo_mp3 = PyMongo(server, uri="mongodb://host.minikube.internal:27017/mp3s")

fs_videos = gridfs.GridFS(mongo_video.db)
fs_mp3s = gridfs.GridFS(mongo_mp3.db)

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()


@server.route("/login", methods=["POST"])
def login():
    logger.info(str(fs_videos))
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err


@server.route("/upload", methods=["POST"])
def upload():
    try:
        access, err = validate.token(request)
        if err:
            return err

        access = json.loads(access)

        if access["admin"]:
            if len(request.files) != 1:
                return "Exactly 1 file required", 400
            
            logger.info(str("Hello")+str(fs_videos))
            for _, f in request.files.items():
                err = util.upload(f, fs_videos, channel, access)
                if err:
                    return err

            return "success!", 200
        else:
            return "Not authorized", 401
    except Exception as e:
        logger.error(f"Error during file upload: {e}")
        return "Internal Server Error", 500

@server.route("/download", methods=["GET"])
def download():
    pass

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)