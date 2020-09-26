import os
import time
import json
import requests
from module import module
from network import connect
import threading

class DrrrConsole(object):
	def __init__(self, name,room):
		self.name = name
		self.icon = ""
		self.file_name = 'cache/drrr.cookie'
		self.id = room
		self.login()
		self.enter_room = module.Module(self.name)

	def login(self):
		bot = connect.Connect(name=self.name, icon=self.icon)
		if not os.path.isfile(self.file_name):
			bot.login()
			bot.save_cookie(file_name=self.file_name)

	def start(self):
		try:
			#sala para entrar
			url_room =f'https://drrr.com/room/?id={self.id}'
			self.enter_room.load_cookie(file_name=self.file_name)
			e_room = self.enter_room.room_enter(url_room=url_room)
			is_leave = self.enter_room.room_update()
		except Exception as e:
			print(e)

	def sendMenssagem(self,message):
		self.enter_room.post(message)

	def loop(self):
		while True:
			msg = input('')
			self.sendMenssagem(msg)


if __name__=='__main__':
	clear = lambda: os.system('cls')
	username = input('Digite o Seu usuario: ')
	idRoom = input('Digite o id da sala: ')
	Console = DrrrConsole(username,idRoom)
	clear()
	t_loopmsg = threading.Thread(target=Console.loop)
	t_loopmsg.start()
	Console.start()


# k5Nb0uomag