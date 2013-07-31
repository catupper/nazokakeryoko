#-*- coding:utf-8 -*-
from google.appengine.ext import db

class Dictionary(db.Model):
    filename = db.StringProperty()
    word = db.StringProperty()
    content = db.TextProperty()
    

x = "inverse1.csv"
f = open(x, "r")
for line in f:
    try:
        line = line.decode('utf-8')
        tmp = Dictionary()
        tmp.filename = x
        tmp.word, tmp.content = map(lambda x:x.strip(), line.split(',', 1))
        tmp.put()
    except:
        pass
