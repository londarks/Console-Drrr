import requests
import time
import json
import re
import os
import threading
import sys



class Module(object):
    def __init__(self, name):
        self.session = requests.session()
        self.name = name
        self.file = open('cache/drrr.cookie', 'r')
        self.session.cookies.update(eval(self.file.read()))
        self.file.close()

    def post(self, message, url='', to=''):
        post_body = {
            'message': message,
            'url': url,
            'to': to
        }
        p = self.session.post(
            url='https://drrr.com/room/?ajax=1', data=post_body)
        p.close()


    def load_cookie(self, file_name):
        f = open(file_name, 'r')
        self.session.cookies.update(eval(f.read()))
        f.close()

    def room_enter(self, url_room):
        re = self.session.get(url_room,headers={'User-Agent': 'Bot'})
        re.close()
        #room = self.session.get('https://drrr.com/json.php?fast=1')
        #return room.json()

    def room_update(self):
        #inicializando bot
        sendResponse  = self.session.get("https://drrr.com/json.php?fast=1")
        response = sendResponse.json()
        #condição para  ver se esta na sala ou não
        checkUpdate = response['update']
        while True:
            #time.sleep(1)
            sendResponse  = self.session.get("https://drrr.com/json.php?fast=1")
            response = sendResponse.json()
            if checkUpdate != response['update']:
                try:
                    url_room_update = "https://drrr.com/json.php?update={}".format(response['update'])
                    msgApi = self.session.get(url_room_update).json()

                    checkEnterRoom = msgApi['talks'][0]['type']
                    
                    if checkEnterRoom == 'join':
                        name_sender = msgApi['talks'][0]['user']['name']
                        try:
                            tripcode = msgApi['talks'][0]['user']['tripcode']
                        except Exception:
                            tripcode = None 
                        print("---- @{}#{} -- Enter The room ----".format(name_sender,tripcode))
                    
                    if checkEnterRoom == 'leave':
                        name_sender = msgApi['talks'][0]['user']['name']
                        try:
                            tripcode = msgApi['talks'][0]['user']['tripcode']
                        except Exception:
                            tripcode = None 
                        print("---- @{}#{} -- leave The room ----".format(name_sender,tripcode)) 

                    #pegando dados dos usuarios que estao conversando
                    name_sender = msgApi['talks'][0]['from']['name']
                    id_sender  = msgApi['talks'][0]['from']['id']
                    try:
                        tripcode = msgApi['talks'][0]['from']['tripcode']
                    except Exception:
                        tripcode = None 
                    message = msgApi['talks'][0]['message']
                    try:
                        checkPM = msgApi['talks'][0]['secret']
                        if checkPM == True:
                            name_sender = msgApi['talks'][0]['from']['name']
                            id_sender  = msgApi['talks'][0]['from']['id']
                            try:
                                tripcode = msgApi['talks'][0]['from']['tripcode']
                            except Exception:
                                tripcode = None
                            #menssagem privado
                            print("@{}#{}: {}".format(name_sender,tripcode,message))
                    except Exception:
                        #menssagem normal
                        print("@{}#{}: {}".format(name_sender,tripcode,message))
                    #fim do loop
                    checkUpdate = response['update']
                except Exception as e:
                    pass
                    #print(Fore.MAGENTA + "{}".format(e))