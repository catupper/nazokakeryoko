#!/usr/bin/python
#-*- coding:utf-8 -*-
from random import choice
from google.appengine.ext import db
from google.appengine.ext.db import Key
relation = {}
inverse = {}

html = open("result.html","r").read()
class Dictionary(db.Model):
    filename = db.StringProperty()
    word = db.StringProperty()
    content = db.TextProperty()


def solve(word):
    if(word == ""):
        return ["1"]*5
    relapplicants = [x for x in Dictionary.gql("WHERE filename = :relationcsv AND word=:searching", relationcsv="relation.csv", searching=word.decode('utf-8'))]
    print len(relapplicants)
    if(len(relapplicants) == 0):
        return [""]*5
    relapplicants = relapplicants[0]
    relation = relapplicants.content.encode('utf-8').split(',')
    for x in xrange(1000):
        wordR = choice(relation).strip('()').split()
        if len(wordR[0]) < 9:continue
        inverse = invapplicants = [x for x in Dictionary.gql("WHERE filename = :inversecsv AND word = :searching", inversecsv = "inverse.csv", searching = wordR[0].decode('utf-8'))][0].content.encode('utf-8').split(',')
        res = choice(inverse).strip('()').split()
        if res[0] != word and res[1] != wordR[1]:
            return (word, res[0], wordR[0], wordR[1], res[1])
    return (word, "", "よくわかりません", "","")


import cgi

def main():

    f = cgi.FieldStorage()
    txt = f.getfirst('nazo', '')
    p = solve(txt)
    if(p[-1] == ""):
        print open("wrong.html","r").read()%("ごめんなさい", "私はその言葉が","よくわからないです")
    elif(p[-1] == "1"):
        print open("wrong.html","r").read()%("何か", "文字を","入力してください")
    else:
        print html%(p[0], p[1], p[2] + '(%s, %s)'%(p[3],p[4]), p[0], p[1], p[2], p[0], p[1], p[2])

main()
