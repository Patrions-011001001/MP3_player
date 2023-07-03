from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty
from Liberal.sound import init_SoundManager_and_scaning_mp3

class item(MDBoxLayout):
	text = StringProperty()
	secondary_text = StringProperty()
	source = StringProperty()
	id_treack = StringProperty()
	def __init__(self,**kwargs):
		super().__init__()
		self.orientation = 'vertical'
		self.padding = [10,15]



class search_screen(MDBottomNavigationItem):
	def __init__(self,**kwargs):
		super().__init__()
		self.icon = 'format-list-bulleted'
		self.name = 'screen 2'
		self.text = 'Ваши треки'
		self.SouMan = init_SoundManager_and_scaning_mp3()
		self.list = []
		for element in self.SouMan.SoundsManager.dict_:
			self.list.append(element)

		self.set_defult()

	def search(self,*args):
		self.ids.rv.data = []
		self.search_(self.ids.search_treack.text)

	def search_(self,tbr):
		for element in self.list:
			element = self.SouMan.SoundsManager.dict_[element]
			if tbr in element['title'] or tbr in element['artist']:
				self.add_item(text=element['title'],secondary_text=element['artist'],source=element['path_to_img'],id_=str(element['index']))
			else:
				pass

	def set_defult(self):
		self.ids.rv.data = []
		for element in self.list:
			element = self.SouMan.SoundsManager.dict_[element]
			self.add_item(text=element['title'],secondary_text=element['artist'],source=element['path_to_img'],id_=str(element['index']))

	def add_item(self,**kwargs):
		self.ids.rv.data.append(
			{
				'text':kwargs['text'],
				"secondary_text":kwargs['secondary_text'],
				'source':kwargs['source'],
				'id_treack':kwargs['id_']
			}
		)
		
