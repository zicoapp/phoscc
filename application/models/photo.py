# coding: utf-8
from leancloud import Object

class Photo(Object):

	def dump(self):
		return {'id': self.id, 
				'url_thumbnail': self.get('url') + "?imageView2/2/w/700/interlace/1", 
				'url': self.get('url')}
