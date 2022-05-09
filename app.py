from flask import Flask, render_template, request
from flask_serial import Serial
from flask_socketio import SocketIO
from flask_cors import CORS
import datetime as dt

import mysql.connector
#import MySQLdb.cursors

import json
from flask import jsonify

import sys

import eventlet
eventlet.monkey_patch()

app = Flask(__name__)
app.config['SERIAL_TIMEOUT'] = 0.1
app.config['SERIAL_PORT'] = 'COM8'
app.config['SERIAL_BAUDRATE'] = 9600
app.config['SERIAL_BYTESIZE'] = 8
app.config['SERIAL_PARITY'] = 'N'
app.config['SERIAL_STOPBITS'] = 1

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'poit'

ser = Serial(app)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="poit"
)
mycursor = mydb.cursor(buffered=True)

@socketio.on('send')
def handle_send(json_str):
    data = json.loads(json_str)
    ser.on_send(data['message'])
    print("send to serial: %s"%data['message'])

@ser.on_message()
def handle_message(msg):
    socketio.emit("serial_message", data={"message":(str(msg.decode()))})
    data = json.loads(msg.decode())
    #print ("""Insert Into poit (temperature, humidity) Values(%s, %s)""") %(data["temperature"],data["humidity"])
    save_data(data["temperature"], data["humidity"])

@ser.on_log()
def handle_logging(level, info):
    print(level, info)
    
@app.route('/led', methods = ['POST'])
def changeLedStatus():
    data = request.get_json()
    #print(data)
    ser.on_send(json.dumps(data).encode())
    return "OK";

@socketio.on('connect')
def test_connect(auth):
    socketio.emit('connect', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
    
@app.route('/data', methods=['GET'])
def get_data_from_db():    
    if request.method == 'GET':
        mycursor.execute("""SELECT * FROM data""")
        results = mycursor.fetchall()
        return jsonify(results)
    return jsonify([])
        
    #if request.method == 'POST':
        #cursor.execute('Insert Into poit (temperature, humidity) Values( %s, %s )', (n,))

def save_data(temperature, humidity):
    try:
        res = mycursor.execute("""Insert Into data (temperature, humidity) Values(%s, %s)""", (temperature, humidity))
        mydb.commit()
    except:
        print(sys.exc_info())
    #try:
        #res = cursor.execute("Insert Into data (temperature, humidity) Values(%s, %s)", (temperature, humidity))
        #mysql.connection.commit()
    #except Exception as e:
        #print(e)
    #print(res)
    #print(cursor.rowcount)
    return "ok"

if __name__ == '__main__':
    # Warning!!!
    # this must use `debug=False`
    # if you use `debug=True`,it will open serial twice, it will open serial failed!!!
    socketio.run(app, debug=False)