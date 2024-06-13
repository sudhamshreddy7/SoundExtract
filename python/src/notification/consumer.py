import pika,sys,os,time
from send import email
def main():
                 
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=str("rabbitmq")))
    channel = connection.channel()
    def callback(channel , method, properties, body):
        err = email.notification(body)
        if err:
            channel.basic_nack(delivery_tag = method.delivery_tag)
        else:
            channel.basic_ack(delivery_tag = method.delivery_tag)

    channel.basic_consume(
        queue=os.environ.get("MP3_QUEUE"),
        on_message_callback=callback
    )
    print("Waiting for message")
    channel.start_consuming()
if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt as key:
        print(key)
        try:
            sys.exit(0)
        except Exception:
            os._exit(0)