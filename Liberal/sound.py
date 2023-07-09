import os
import kivy
import random
from pygame import mixer
from Liberal.tinytag.tinytag import TinyTag
from getpass import getuser
import json


class init_SoundManager_and_scaning_mp3():
	def __init__(self):
		self.paths = {
			"posix":["Documents",'Download','Music'],
			"nt":["Documents",'Music','Downloads']
		}

		self.dict_s = {}
		self.list_s = [] 
		self.x = 0
		
		for element in self.paths[os.name]:
			self.scan(element)

		self.SoundsManager = SoundsManager(_dict_=self.dict_s,_list_=self.list_s)


	def scan(self,cureent_path,root_path=''):
		if root_path == '':
			if os.name == 'nt':
				path = f'C:/Users/{getuser()}/{cureent_path}'
			elif os.name == 'posix':
				path = f'/storage/emulated/0/{cureent_path}'
		else:
			path = root_path+"/"+cureent_path
		try:
			for element in os.listdir(path):
				if '.ini' in element:
					pass
				elif '.mp3' in element:
					tag = TinyTag.get(f"{path}/{element}",image=True)
					if tag.title == None:
						pass
					else:
						self.dict_s.update({
							f'{tag.title}_+_{tag.artist}':{
								'path':f"{path}/{element}",
								"lenght":round(tag.duration),
								"title":tag.title,
								"artist":tag.artist,
								'path_to_img':'Image/Chas_icon/local/icon_'+str(self.x)+'.png',
								"index":self.x
								}
							}
						)
						self.list_s.append(f'{tag.title}_+_{tag.artist}')
						with open(f'Image/Chas_icon/local/icon_{self.x}.png','wb') as f:
							f.write(tag._image_data)
						f.close()
						self.x += 1
				elif not '.' in element:
					self.scan(root_path=path,cureent_path=element)
		except Exception as e:
			if '[WinError 267]' in str(e):
				print('Неверно задано имя папки')
			elif '[WinError 5]' in str(e):
				print('Отказано в доступе')
			elif "a bytes-like object is required, not 'NoneType'" in element:
				with open("Image/crahs-image.png",'rb') as f:
					_image_data = f.read()
				f.close()

				with open(f'Image/Chas_icon/local/icon_{self.x}.png','wb') as f:
					f.write(_image_data)
				f.close()
				self.x += 1
			else:
				print(e)

class sound_control():
	"""Класс нужный для легкого обращения к mixer из pygame
	для функции play могут быть дополнительные настроики запуска"""
	def __init__(self,**kwargs):
		mixer.init()

	def play(self,**kwargs):
		if kwargs == {}:
			mixer.music.play()
		else:
			mixer.music.play(loops=kwargs['loops'],start=kwargs['start'])

	def unpause(self):
		mixer.music.unpause()

	def pause(self):
		mixer.music.pause()

	def load(self,path):
		mixer.music.load(path)

	def set_time(self,time):
		mixer.music.play(start=time)

class SoundsManager():
	"""Класс отвечаюший за порядковое воиспроизведение музыки"""
	def __init__(self,**kwargs):
		self.dict_ = kwargs["_dict_"]
		self.list_manager_defult = kwargs["_list_"]
		self.list_manager_random = self.list_mixer(kwargs["_list_"])


	def list_mixer(self,_list_):
		l_d = _list_
		l_r_n = []

		for qwerty in range(len(l_d)):		
			if l_d != []:
				r_e = random.randrange(0,len(l_d))
				l_r_n.append(l_d[r_e])
				l_d.pop(r_e)

		return l_r_n
