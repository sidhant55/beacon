import paho.mqtt.client as mqtt
import alchemy
import json
import datetime
from random import randint
import psycopg2

ServerAddress='192.168.1.111'
BrokerAddress="192.168.1.111"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("beacon/stage1/", qos=2)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
		raw_data=str(msg.payload.decode("UTF-8"))
		json_data=json.loads(raw_data)
		# bea=alchemy.beacon(json_data['MAC'],json_data['RSSI'],datetime.datetime.now(),0)
		# try:
		# 	alchemy.db.session.add(bea)
		# 	alchemy.db.session.commit()
		# 	print("Success")
		# except:
		# 	print("MAC already existing")

		try:
			conn=psycopg2.connect("dbname='beacon' user='postgres' host='{}' port='5433' password='sid555'".format(ServerAddress))
		except:
			print("Cannot connect to database")
		cur=conn.cursor()
		# cur=self.dbconnect()
		try:
			cur.execute("""INSERT INTO beacon ("MAC","RSSI","UTStamp","Flag") VALUES ('{}','{}','{}','0')""".format(json_data['MAC'],json_data['RSSI'],datetime.datetime.now()))
			print("Inserted into database")
		except:
			print("Already in database")
		conn.commit()
		conn.close()
    

def Main():
	client = mqtt.Client('cliet1',clean_session=False)
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(BrokerAddress, 1883, 60)
	client.loop_forever()


if __name__ == '__main__':
	Main()