import pika,sys,os,time
import pika.connection
from pymongo import MongoClient
import gridfs
from convert import to_mp3

def main():
    client = MongoClient("host.minikube.internal",27017)
    db_videos = client.videos
    db_mp3 = client.mp3s
    #gridfs
    fs_videos = gridfs.GridFS(db_videos)
    fs_mp3s = gridfs.GridFS(db_mp3)
    #rabbitmq
    connection = pika.BaseConnection(
        pika.ConnectionParameters(host="rabbitmq")
    )
    channel = connection.channel()
    def callback(channel , method, properties, body):
        err = to_mp3.start(body,fs_videos,fs_mp3s,channel)
        if err:
            channel.basic_nack(delivery)

    channel.basic_consume(
        queue=os.environ.get("VIDOE_QUEUE"),
        on_message_callback=callback
    )