import pika,os,json, tempfile
from bson.objectid import ObjectId
import pika.spec
import moviepy.editor

def start(message,fs_videos,fs_mp3s,channel):
    message = json.loads(message)
    tf = tempfile.NamedTemporaryFile()
    output = fs_videos.get(ObjectId(message["video_fid"]))
    #add viedo to empty file
    tf.write(output.read())
    audio = moviepy.editor.VideoFileClip(tf.name).audio
    tf.close()
    path = tempfile.gettempdir() + f"/{message['video_fid']}".mp3
    audio.write_audiofile(path)
    file = open(path,"rb")
    fid = fs_mp3s.put(file.read())
    file.close()
    os.remove(path)
    message["mp3_fid"]=str(fid)
    try:
        channel.basic_publish(
            exchange="",
            routing_key = os.environ.get("MP#_QUEUE"),
            body = json.dumps(message),
            properties = pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    except Exception as ex:
        print(ex)
        fs_mp3s.delete(fid)
        return "failed to push into queue mp3"