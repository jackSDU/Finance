from multiprocessing import Process,Pipe
from subprocess import Popen

import requests

from flask import Flask,request,make_response

CLIENT_HOST="127.0.0.1"
CLIENT_PORT=8000

PORT=2333

def daemon():

    pass

app=Flask('Server')

@app.route('/start/<int:id>',methods=['POST'])
def start(id):
    pass

@app.route('/stop/<int:id>',methods=['POST'])
def stop(id):
    pass

app.run(port=PORT,debug=True)