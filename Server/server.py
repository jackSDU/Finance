import time
import tempfile
import subprocess
from multiprocessing import Process,Pipe

import requests

from flask import Flask,request

CLIENT_HOST="127.0.0.1"
CLIENT_PORT=80

PORT=2333

cmd_read,cmd_write=Pipe(False)
stop_read,stop_write=Pipe(False)

def worker_daemon(cmd,stop):
    dict={}
    result_dict={}
    while True:
        while cmd.poll():
            c=cmd.recv()
            if c[0] in dict:
                continue
            of=tempfile.TemporaryFile()
            ef=tempfile.TemporaryFile()
            try:
                dict[c[0]]=subprocess.Popen(c[1].split(),stdout=of,stderr=ef)
                result_dict[c[0]]=(of,ef,)
                requests.post("http://"+CLIENT_HOST+":"+str(CLIENT_PORT)+'/started/'+str(c[0]))
            except Exception as ex:
                of.close()
                ef.close()
                requests.post("http://"+CLIENT_HOST+":"+str(CLIENT_PORT)+'/wrong/'+str(c[0]),{"err":str(ex)})
        while stop.poll():
            id=stop.recv()
            try:
                dict.pop(id).terminate()
                of,ef=result_dict.pop(id)
                of.close()
                ef.close()
                requests.post("http://"+CLIENT_HOST+":"+str(CLIENT_PORT)+'/stopped/'+str(id))
            except:
                pass
        todel=[]
        for id,p in dict:
            ret=p.poll()
            if ret==None:
                continue
            todel.append(id)
            of,ef=result_dict.pop(id)
            requests.post("http://"+CLIENT_HOST+":"+str(CLIENT_PORT)+("/right/" if ret==0 else "/wrong/")+str(id),
                          {"out":of.read(),"err":ef.read(),"ret":ret})
            of.close()
            ef.close()
        for id in todel:
            dict.pop(id)
        time.sleep(5)

app=Flask('Server')

@app.route('/start/<int:id>',methods=['POST'])
def start(id):
    cmd_write.send([id,request.form["cmd"]])
    return ''

@app.route('/stop/<int:id>',methods=['POST'])
def stop(id):
    stop_write.send(id)
    return ''

if __name__ == '__main__':
    app.run(port=PORT)