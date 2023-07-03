from view_page import Player, search

import kivymd
from kivymd.app import MDApp
from kivymd.uix.bottomnavigation import MDBottomNavigation
from kivy.core.window import Window

Window.size = (450,650)

class manger_botton_navigation(MDBottomNavigation):
	def __init__(self,**kwargs):
		super().__init__()
		self.add_widget(Player.Player())
		self.add_widget(search.search_screen())

class DEO(MDApp):
	def build(self):
		self.theme_cls.theme_style = "Dark"
		self.mbn = manger_botton_navigation()
		#self.mbn.children[1].current = 'screen 1'
		return self.mbn


if __name__ == '__main__':
	DEO().run()