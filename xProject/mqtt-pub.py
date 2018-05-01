import paho.mqtt.client as mqtt
ServerAddress='192.168.1.111'
client=mqtt.Client("Print",clean_session=False)
client.connect(ServerAddress)
js="test2"
client.loop_start()
client.publish("skaaa", payload=js,qos=2,retain=True)
print("Published flag=1 sucessfully")
client.loop_stop()
client.disconnect()