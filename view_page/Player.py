from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from Liberal.sound import init_SoundManager_and_scaning_mp3, TinyTag, sound_control
import time
from kivy.clock import Clock
import json
from threading import Thread

class Player(MDBottomNavigationItem):
	def __init__(self,**kwargs):
		super(Player,self).__init__(**kwargs)
		self.ids_dict = {
			'play_button':self.ids.playning_control,
			'time_c':self.ids.current_time,
			'time_t':self.ids.total_time,
			"progress":self.ids.progress,
			'Title':self.ids.title,
			'Artist':self.ids.Artist,
			'Image_treack':self.ids.albom,
			"Like":self.ids.like,
			'dislike':self.ids.dislike
		}
		self.icon = 'motion-play'
		self.name = 'screen 1'
		self.text = 'Плеер'
		self.SouMan = init_SoundManager_and_scaning_mp3().SoundsManager
		self.sound = sound_control()
		self.list_manager_defult = [] 
		self.status_p = False
		self.frist_start = True
		self.status_r = False
		self.status_rep = "List"
		for element in self.SouMan.dict_:
			self.list_manager_defult.append(element)
		self.max_index = len(self.SouMan.list_manager_random) - 1
		self.not_random_list = self.list_manager_defult
		self.async_def()

	def like(self,*args):
		if self.ids_dict['Like'].icon == 'cards-heart-outline':
			self.ids_dict['Like'].icon = 'cards-heart'
			self.ids_dict['dislike'].icon = 'cards-heart-outline'
			self.update_favorite('Like')
		else:
			self.ids_dict['Like'].icon = 'cards-heart-outline'

	def dislike(self,*args):
		if self.ids_dict['dislike'].icon == 'cards-heart-outline':
			self.ids_dict['dislike'].icon = 'heart-broken-outline'
			self.ids_dict['Like'].icon = 'cards-heart-outline'
			self.update_favorite('Dislike')
		else:
			self.ids_dict['dislike'].icon = 'cards-heart-outline'

	def update_favorite(self,status):
		with open('database.json','r',encoding='utf-8') as f:
			data = json.load(f)
		f.close()

		data['Favorite'].update({self.ids_dict['Title'].text+"_+_"+self.ids_dict['Artist'].text:{"status":status}})

		with open('database.json','w',encoding='utf-8') as f:
			f.write(json.dumps(data,indent=4,ensure_ascii=False))
		f.close()

	def repeat_l(self,*args):
		if self.status_rep == "List":
			self.ids.repeat_list.icon = 'repeat-once'
			self.status_rep = 'Treack'
			self._id_ = self.current_index 
		elif self.status_rep == "Treack":
			self.status_rep = "Disable"
			self.ids.repeat_list.icon = 'repeat-off'
		else:
			self.status_rep = "List"
			self.ids.repeat_list.icon = 'repeat-variant'

	def random_position(self,*args):
		if self.status_r == False:
			self.list_manager_defult = self.SouMan.list_manager_random
			self.status_r = True
			self.ids.random.icon = 'shuffle-variant'
		else:
			self.list_manager_defult = self.not_random_list
			self.ids.random.icon = 'shuffle-disabled'
			self.status_r = False

	def async_def(self):
		with open('database.json','r',encoding='utf-8') as f:
			e = json.load(f)
			self.info_ = e['Favorite']
			e = e['Last treack']
			self.current_index = e['index']
			try:
				element = self.SouMan.dict_[self.list_manager_defult[self.current_index]]
			except IndexError:
				self.current_index = 0
				element = self.SouMan.dict_[self.list_manager_defult[self.current_index]]
			self.ids.title.text = e['title']
			self.ids.Artist.text = e['artist']
			self.ids.progress.value = e['time_c']
			self.ids.progress.max = e['time_t']
			self.ids.total_time.text = time.strftime('%M:%S',time.gmtime(e['time_t']))
			self.ids.current_time.text = time.strftime('%M:%S',time.gmtime(e['time_c']))
		f.close()

	def update_info(self,index):
		with open('database.json','r',encoding='utf-8') as f:
			data = json.load(f)
		f.close()

		data['Last treack'].update({
			'title':self.ids.title.text,
            'artist':self.ids.Artist.text,
            'index':index,
            "time_c":self.ids.progress.value,
            "time_t":self.ids.progress.max})

		with open('database.json','w',encoding='utf-8') as f:
			f.write(json.dumps(data,indent=4,ensure_ascii=False))
		f.close()

	def set_treack(self,time_for_func=None,*args):
		if time_for_func == None:
			self.sound.set_time(self.ids.progress.value)
		else:
			element = self.SouMan.dict_[self.list_manager_defult[self.current_index]]
			self.sound.load(element['path'])
			self.sound.set_time(time_for_func)
			self.event = Clock.schedule_interval(self.update_progress,1)

	def update_progress(self,*args):
		if self.ids.progress.value > self.ids.progress.max:
			if self.status_rep == 'List':
				self.ids.progress.value = 0
				self.ids.current_time.text = '00:00'
				self.next_(1)
			elif self.status_rep == 'Treack':
				self.event.cancel()
				self.start_sound()
			else:
				self.event.cancel()
				self.sound.pause()

		else:
			self.ids.progress.value += 1
			self.ids.current_time.text = time.strftime('%M:%S',time.gmtime(self.ids.progress.value))

	def update_albom(self,path):
		try:
			tag = TinyTag.get(path,image=True)
			with open('Image/chas.png','wb') as f:
				f.write(tag._image_data)
			f.close()
			self.ids.albom.source = "Image/chas.png"
		except TypeError:
			self.ids.albom.source = 'Image/crahs-image.png'
		self.ids.albom.reload()

	def set_info(self,element):
		self.update_albom(element['path'])
		self.ids.total_time.text = time.strftime('%M:%S',time.gmtime(element['lenght']))
		self.ids.progress.max = element['lenght']
		self.ids.title.text = element['title']
		self.ids.Artist.text = element['artist']
		self.frist_start = False
		self.status_p = True
		self.ids_dict['play_button'].icon = 'pause'
		self.ids.progress.value = 0

	def load_and_start(self,element):
		self.sound.load(element['path'])
		self.event = Clock.schedule_interval(self.update_progress,1)
		self.sound.play()

	def start_sound(self,index_el=None,all_dislike=False):
		if index_el == None:
			if self.status_rep == 'Treack':
				self.current_index = self._id_
			else:
				pass
			element = self.SouMan.dict_[self.list_manager_defult[self.current_index]]
		else:
			element = self.SouMan.dict_[self.list_manager_defult[int(index_el)]]
			self.current_index = int(index_el)

		try:
			self.event.cancel()
		except Exception:
			pass

		self.set_info(element)

		try:
			if self.info_[element['title']+"_+_"+element['artist']]['status'] == 'Dislike':
				if all_dislike == True:
					self.ids_dict['dislike'].icon = 'heart-broken-outline'
					self.ids_dict['Like'].icon = 'cards-heart-outline'
					self.load_and_start(element)
				else:
					self.next_(0)
			else:
				self.ids_dict['Like'].icon = 'cards-heart'
				self.ids_dict['dislike'].icon = 'cards-heart-outline'
				self.load_and_start(element)
				
		except KeyError:
			self.ids_dict['Like'].icon = 'cards-heart-outline'
			self.ids_dict['dislike'].icon = 'cards-heart-outline'
			self.load_and_start(element)

		

	def prev_(self,*args):
		if self.current_index == 0:
			self.current_index = self.max_index
		else:
			self.current_index -= 1
		try:
			self.event.cancel()
		except AttributeError:
			pass
		self.start_sound(all_dislike=True)

	def play(self,*args):
		if self.frist_start == True:
			if self.ids.progress.value != 0:
				self.set_treack(self.ids.progress.value)
				self.frist_start = False
				self.status_p = True
				self.ids_dict['play_button'].icon = 'pause'
			else:
				self.start_sound()
		else:
			if self.status_p == False:
				self.status_p = True
				self.ids_dict['play_button'].icon = 'pause'
				self.sound.unpause()
				self.event()

			elif self.status_p == True:
				self.status_p = False
				self.ids_dict['play_button'].icon = 'play'
				self.sound.pause()
				self.event.cancel()
		self.update_info(self.current_index)

	def next_(self,*args):
		if self.current_index == self.max_index:
			self.current_index = 0
		else:
			self.current_index += 1
		try:
			self.event.cancel()
		except AttributeError:
			pass
		self.start_sound()

