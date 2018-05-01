import os
from subprocess import Popen
import paho.mqtt.client as mqtt
import datetime
import psycopg2
import time

ServerAddress='192.168.1.111'

class Printbar():
	broker_address="192.168.1.111"
	client=mqtt.Client("Print",clean_session=False)
	text2 = None
	def __init__(self,text):
		self.client.connect(self.broker_address)
		self.client.loop_start()
		self.text2 = text;
		self.text="'"+text+"'"
		js="{\"MAC\":\""+self.text2+"\",\"Status\":1}"
		try:
			conn=psycopg2.connect("dbname='beacon' user='postgres' host='{}' port='5433' password='sid555'".format(ServerAddress))
		except:
			print("Cannot connect to database")
		cur=conn.cursor()
		cur.execute("""UPDATE beacon SET "Flag"='1' WHERE "MAC"='{}' """.format(text))
		conn.commit()
		conn.close()
		print("Database")
		self.client.publish("beacon/stage2/step2/", payload=js,qos=2,retain=True)
		print("Published flag=1 sucessfully")
		files = os.listdir("C:\Windows\System32\spool\PRINTERS")
		for f in files:
			try:
				os.remove("C:\Windows\System32\spool\PRINTERS\{}".format(f))
			except:
				print(f)


	def Main(self):
		print("Inside Printer", self.text)
		ar=["<xpml><page quantity='0' pitch='15.0 mm'></xpml>SIZE 60 mm, 15 mm\r\n", 'GAP 3 mm, 0 mm\r\n', 'SPEED 3\r\n', 'DENSITY 15\r\n', 'SET RIBBON ON\r\n', 'DIRECTION 0,0\r\n', 'REFERENCE 0,0\r\n', 'OFFSET 0 mm\r\n', 'SET PEEL OFF\r\n', 'SET CUTTER OFF\r\n', 'SET PARTIAL_CUTTER OFF\r\n', "<xpml></page></xpml><xpml><page quantity='1' pitch='15.0 mm'></xpml>SET TEAR ON\r\n", 'CLS\r\n', 'BARCODE 470,86,"128",46,0,180,1,2,"{}"\r\n', 'CODEPAGE 1252\r\n', 'TEXT 455,34,"ROMAN.TTF",180,1,8,"{}"\r\n', 'BARCODE 230,86,"128",46,0,180,1,2,"{}"\r\n', 'TEXT 215,34,"ROMAN.TTF",180,1,8,"{}"\r\n', 'PRINT 1,1\r\n', '<xpml></page></xpml><xpml><end/></xpml>']
		ar[13]=ar[13].format(self.text2)
		ar[15]=ar[15].format(self.text2)
		ar[16]=ar[16].format(self.text2)
		ar[17]=ar[17].format(self.text2)

		with open("dumy.txt", "w") as text_file:
			for ro in ar:
				st=str(ro)
				text_file.write(st)

		p = Popen("testp.bat", cwd=r"C:\Users\Distronix\xProject")
		stdout, stderr = p.communicate()
		time.sleep(0.5)

		try:
			conn=psycopg2.connect("dbname='beacon' user='postgres' host='{}' port='5433' password='sid555'".format(ServerAddress))
		except:
			print("Cannot connect to database")
		cur=conn.cursor()
		# cur=self.dbconnect()
		

		if (len(os.listdir("C:\Windows\System32\spool\PRINTERS"))>1):
			js="{\"MAC\":\""+self.text2+"\",\"Status\":2}"
			self.client.publish("beacon/stage2/step2/", payload=js,qos=2,retain=True)
			cur.execute("""UPDATE beacon SET "Flag"='2' WHERE "MAC"={} """.format(self.text))
		elif(len(os.listdir("C:\Windows\System32\spool\PRINTERS"))<=1):
			js="{\"MAC\":\""+self.text2+"\",\"Status\":3}"
			self.client.publish("beacon/stage2/step2/", payload=js,qos=2,retain=True)
			cur.execute("""UPDATE beacon SET "Flag"='3',"PTStamp"='{}' WHERE "MAC"={} """.format(datetime.datetime.now(),self.text))

		conn.commit()
		conn.close()
		self.client.loop_stop()
		self.client.disconnect()

		files = os.listdir("C:\Windows\System32\spool\PRINTERS")

		for f in files:
			try:
				os.remove("C:\Windows\System32\spool\PRINTERS\{}".format(f))
			except:
				print(f)
