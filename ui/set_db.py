#-*- coding:utf-8 -*-
import cgi
from google.appengine.ext import db

f = cgi.FieldStorage()
class Dictionary(db.Model):
    filename = db.StringProperty()
    word = db.StringProperty()
    content = db.TextProperty()
    
x = f.getfirst("filename", "")
f = open(x, "r")
for line in f:
    try:
        line = line.decode('utf-8')
        tmp = Dictionary()
        if(x[0] == 'r'):
            tmp.filename = "relation.csv"
        else:
            tmp.filename = "inverse.csv"
        tmp.word, tmp.content = map(lambda x:x.strip(), line.split(',', 1))
        tmp.put()
    except:
        pass
