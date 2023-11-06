from email import header
import os
import tornado

import logging
from logging.handlers import RotatingFileHandler

from tornado.websocket import WebSocketHandler
from tornado.web import RequestHandler
from tornado.web import StaticFileHandler

import json
import requests
import time
import base64
import hmac

log_file_path = "/home/fpgaol2/cedit/log/cedit.log"
#logging.basicConfig(
#    format='%(asctime)s line:%(lineno)s,  %(message)s', level=logging.INFO)

# 设置日志的格式
log_format = logging.Formatter('%(asctime)s line:%(lineno)s,  %(message)s')

# 创建一个日志处理器，用于写入日志文件
file_handler = RotatingFileHandler(log_file_path, maxBytes=10*1024*1024, backupCount=30)
file_handler.setFormatter(log_format)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

#todo: need to verify the time
def verify(token):
    data = {"result":False,"username":""}
    token_str = base64.urlsafe_b64decode(token).decode('utf-8')
    token_list = token_str.split(':')
    if len(token_list) != 3:
        return(data)
    ts_str = token_list[0]
    name = token_list[2]
    name_key = name+'fpgaol_key'
    known_sha1_tsstr = token_list[1]
    sha1 = hmac.new(name_key.encode("utf-8"),ts_str.encode('utf-8'),'sha1')
    calc_sha1_tsstr = sha1.hexdigest()
    if calc_sha1_tsstr != known_sha1_tsstr:
        return(data)
    else:
        data['result']=True
        data['username']=name
        return(data)


class MainHandler(RequestHandler):
    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.write("hhh")
    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.write("hhh")

class LoginHandler(RequestHandler):
    def post(self):
        logger.info('this is the def login in cedit')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        body_arguments = self.request.body_arguments
        ticket = bytes.decode(body_arguments['ticket'][0], encoding='utf-8')
        logger.info(ticket)
        #API_URL = "http://cdacount.cdinfotech.top/sso/getUserInfo"
        API_URL = "http://202.38.79.96:9003/sso/getUserInfo"
        if ticket=="":
            self.write({"code": 4})
        else:
            data={"ticket":ticket,'ssoLogoutCall':'http://202.38.79.96:9001/sso/logout'}
            headers={"Content-Type":"application/json"}
            logger.info(json.dumps(data))
            #s=requests.Session()
            #s.get("http://cdacount.cdinfotech.top/admin/login?redirect=http://202.38.79.96:9001")
            r = requests.post(API_URL,data=json.dumps(data),headers=headers)
            rjson = r.json()
            logger.info("rjson: %s",rjson)
            bbb=rjson
            #bbb['code']=1
            #bbb['data']={}
            #bbb['data']['username']='hexu'
            if bbb['code']==1:
                key=bbb['data']['username']+'fpgaol_key'
                username=bbb['data']['username']
                ts_str = str(time.time())
                ts_byte = ts_str.encode("utf-8")
                sha1_tshexstr  = hmac.new(key.encode("utf-8"),ts_byte,'sha1').hexdigest()
                token_1 = ts_str+':'+sha1_tshexstr+':'+username
                b64_token = base64.urlsafe_b64encode(token_1.encode("utf-8"))
                token=b64_token.decode("utf-8")
                data=bbb
                data['token']=token
                
                logger.info("token: %s",token)
                ver = verify(token)
                if ver['result']==False:
                    logger.warning("login defeat")
                else:
                    logger.warning("login success")
                self.write(data)
            else:
                logger.warning("uniauth login defeat")
                logger.info("defeat rjson %s",rjson)
                self.write(rjson)

class ProfileHandler(RequestHandler):
    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        body_arguments = self.request.body_arguments
        token = bytes.decode(body_arguments['token'][0], encoding='utf-8')
        ver = verify(token)
        if ver['result']==False:
            self.write({"code":0,"msg":"error"});
        else:
            name = ver['username']
            data={"code":1,"msg":"success"}
            data['username']=name
            if myprofile.get(name):
                data['age']=myprofile[name]['age']
                data['photos']=myprofile[name]['photos']
                data['school']=myprofile[name]['school']
                data['job']=myprofile[name]['job']
                data['belief']=myprofile[name]['belief']
            else:
                data['age']=myprofile["hexu"]['age']
                data['photos']=myprofile["hexu"]['photos']
                data['school']=myprofile["hexu"]['school']
                data['job']=myprofile["hexu"]['job']
                data['belief']=myprofile["hexu"]['belief']
            self.write(data)

class LogoutHandler(RequestHandler):
    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.write({"code":1})
    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.write({"code":1})

class CodeHandler(RequestHandler):
    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        
        filePath = './code'
        data = []
        count=0;
        for i,j,k in os.walk(filePath):
            if count==0:
                m=0
                for dir in j:
                    data.append({})
                    data[m]['label']=dir
                    data[m]['id']=(m+1)*100
                    m+=1
                count+=1
            else:
                if k:
                    data[count-1]['children']=[]
                m=0
                for file in k:
                    data[count-1]['children'].append({})
                    data[count-1]['children'][m]['label']=file
                    data[count-1]['children'][m]['id']=count*100+m+1
                    with open("./code/"+data[count-1]['label']+'/'+file, 'r') as f:
                        data[count-1]['children'][m]['text']=f.read()
                    m+=1
                count+=1
        self.write({'data':data})

class SavecodeHandler(RequestHandler):
    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        body_arguments = self.request.body_arguments
        data = bytes.decode(body_arguments['data'][0], encoding='utf-8')
        data = json.loads(data)
        for temp in data:
            path = "./code/"+temp['path']
            if os.path.exists(path):
                 with open(path, 'w') as f:
                     f.write(temp['text'])
        self.write({"msg": "save successfully"})

class AppendfileHandler(RequestHandler):
    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        body_arguments = self.request.body_arguments
        path = bytes.decode(body_arguments['path'][0], encoding='utf-8')
        path = "./code/"+path
        with open(path, 'w') as f:
            f.write('')
        self.write({"msg": "append file successfully"})

class DeletefileHandler(RequestHandler):
    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        body_arguments = self.request.body_arguments
        path = bytes.decode(body_arguments['path'][0], encoding='utf-8')
        path = "./code/"+path
        os.remove(path)
        self.write({"msg": "delete file successfully"})

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/login", LoginHandler),
    (r"/profile", ProfileHandler),
    (r'/code',CodeHandler),
    (r'/savecode',SavecodeHandler),
    (r'/appendfile',AppendfileHandler),
    (r'/deletefile',DeletefileHandler),
    (r"/sso/logout", LogoutHandler),
    
])

if __name__ == '__main__':
    myprofile = {"hexu": {"id": 1,"age":22,"photos":11, \
        "school":"University of Science and Technology of China","job":"Student",\
        "belief":"where there is a will, there is a way"}}
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(9001)

    logger.info('Server started')
    tornado.ioloop.IOLoop.current().start()
