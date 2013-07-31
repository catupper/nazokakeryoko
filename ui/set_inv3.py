#-*- coding:utf-8 -*-
import cgi
from google.appengine.ext import db

f = cgi.FieldStorage()
x = f.getfirst("name","")
class Dictionary(db.Model):
    filename = db.StringProperty()
    word = db.StringProperty()
    content = db.TextProperty()
    

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
