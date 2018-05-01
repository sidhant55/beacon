from flask import Flask
from flask_sqlalchemy import SQLAlchemy

ServerAddress='192.168.1.110:5433'

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="postgresql://postgres:sid555@{}/beacon".format(ServerAddress)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class beacon(db.Model):
	__tablename__='beacon'
	MAC=db.Column('MAC',db.String(225))
	RSSI=db.Column('RSSI',db.String(255))
	SerialNo=db.Column('SerialNo',db.Integer, primary_key=True)
	UTStamp=db.Column('UTStamp',db.TIMESTAMP)
	Flag=db.Column('Flag',db.Integer)
	PTStamp=db.Column('PTStamp',db.TIMESTAMP)

	def __init__(self,MAC,RSSI,TimeStamp,Flag):
		self.MAC=MAC
		self.RSSI=RSSI
		self.UTStamp=TimeStamp
		self.Flag=Flag
		self.PTStamp=None