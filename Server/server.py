from multiprocessing import Process,Pipe,Queue
from subprocess import Popen

import requests
import time
import shlex
import subprocess
import tempfile
from flask import Flask,request,make_response
####p = subprocess.Popen(args,stdout=subprocess.DEVNULL)
####poll([timeout])
####Popen.poll()   running--None    success,finish--0  wrong finish--1     WINDOWS


CLIENT_HOST="127.0.0.1"
CLIENT_PORT=8000

PORT=2333


def worker_daemon(cmd,stop):
    dict={}#id--popen
    result_dict={}#id--tem_out--temp_err--ret
    while True:
        #recv poll
        while cmd.poll() == True:
            c=cmd.recv()#id--cmd
            args=c[1].split(' ')#args = shlex.split(c[1])#
            print("exec cmd"+c[1])
            outfile=tempfile.TemporaryFile()
            errfile=tempfile.TemporaryFile()
            p = subprocess.Popen(args,stdout=outfile,stderr=errfile)
            dict[c[0]]=p
            result_dict.update({c[0]:(outfile,errfile,)})

        while stop.poll() == True:
            id =stop.recv()#id
            p=dict.get(id)
            if(p!=None):
                dict.get(id).terminate()
            dict.get(id).terminate()
            dict.pop(id)
            result_dict.pop(id)
        for id,popen in dict.items():
            ret=popen.poll()
            if ret==0:
                dict.pop(id)
                files=result_dict.pop(id)
                requests.post("http://"+CLIENT_HOST+":"+str(CLIENT_PORT)+"/right/"+str(id),
                              {"out":files[0].read(),"err":files[1].read(),"ret":ret})
            elif ret!=0:
                dict.pop(id)
                files=result_dict.pop(id)
                requests.post("http://"+CLIENT_HOST+":"+str(CLIENT_PORT)+"/wrong/"+str(id),
                              {"out":files[0].read(),"err":files[1].read(),"ret":ret})

        time.sleep(4)
        print("helo")
    pass
app=Flask('Server')

@app.route('/start/<int:id>',methods=['POST'])#
def start(id):
    if request.method == 'POST':
        cmd_write.send([id,request.form["cmd"]])
        return "cmd added"
    else:
        return "helloworld"

@app.route('/stop/<int:id>',methods=['POST'])
def stop(id):
    if request.method == 'POST':
        stop_write.send(id)
        return "stop added"
    else:
        return "hellowoeld"

if __name__ == '__main__':
    cmd_read,cmd_write=Pipe(False)
    stop_read,stop_write=Pipe(False)
    w=Process(target = worker_daemon, args=(cmd_read,stop_read),daemon=True)
    w.start()
    app.run(port=PORT,debug=True)