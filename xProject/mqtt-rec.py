import paho.mqtt.client as mqtt
import time
Broker="192.168.1.111"

def on_connect(client,userdata,flags,rc):
	print("cnnected")

	client.subscribe("ska", qos=2)

def on_message(client, userdata,msg):
	r=str(msg.payload.decode("UTF-8"))
	print(r)

client=mqtt.Client('dsf',clean_session=False)
client.on_connect=on_connect
client.on_message=on_message
client.connect(Broker,1883,60)
client.loop_forever()

