import paho.mqtt.client as mqtt
import alchemy
import json
import datetime
from random import randint
import psycopg2

BrokerAddress="192.168.1.110"

Stage2Status=None



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("beacon/stage2/")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
		raw_data=str(msg.payload.decode("UTF-8"))
		json_data=json.loads(raw_data)
		MAC=json_data['MAC']
		MAC="'"+MAC+"'"
		print(MAC)
		cur=dbconnect()
		cur.execute("""SELECT "SerialNo","MAC","Flag","PTStamp" FROM beacon WHERE "MAC"={}""".format(MAC))
		rows=cur.fetchall()
		Stage2Status=len(rows)

		print(len(rows))

		query=[]
		column=('Serial','MAC','Flag','PrintTime')
		for row in rows:
			query.append(dict(zip(column,row)))
		data=json.dumps(query, default=DateFormatConvertor)
		print(data)
		client.publish("beacon/stage2/step1/",payload=data,qos=0)
    
def dbconnect():
	try:
		conn=psycopg2.connect("dbname='beacon' user='postgres' host='{}' port='5433' password='sid555'".format(BrokerAddress))
	except:
		print("Cannot connect to database")
	cur=conn.cursor()
	return cur

def DateFormatConvertor(x):
	if isinstance(x,datetime.datetime):
		return x.__str__()

def Main():
	client = mqtt.Client('cliet2')
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(BrokerAddress, 1883, 60)
	client.loop_forever()


if __name__ == '__main__':
	Main()