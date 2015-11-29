# coding: utf-8
from leancloud import Object

class Category(Object):
    def __str__(self):
    	return self.get('name')
