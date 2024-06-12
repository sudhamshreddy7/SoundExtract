import pika,json

import pika.spec

def upload(f,fs,channel,access):
    try:
        print(str(f))
        print(str(fs))
        fid = fs.put(f)
        print(str(fid))
    except Exception as err:
        print("hi")
        print(err)
        return "internal error",500
    message = {
        "video_fid":str(fid),
        "mp3_fid":None,
        "username":access["username"],
    }
    try:
        print("trying to upload in storage util/n")
        channel.basic_publish(
            exchange = "",
            routing_key = "video",
            body = json.dumps(message),
            #python object to json
            properties = pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
                #to remain in queue if a pods going reset

            )
        )
    except Exception as err:
        print(err)
        fs.delete(fid)
        return "internal queue error", 500
    
