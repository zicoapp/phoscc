# coding: utf-8
from leancloud import Object

class Photo(Object):

	def dump(self):
		relation = self.relation('category')
		cats = relation.query().find()
		return {'id': self.id, 
				'cats': ','.join([str(item) for item in cats]),
				'url_thumbnail': self.get('url') + "?imageView2/2/w/700/interlace/1", 
				'url': self.get('url')}
