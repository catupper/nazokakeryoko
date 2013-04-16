#!/usr/bin/python
#-*- coding:utf-8 -*-
from random import choice
relation = {}
inverse = {}

html="""
<!DOCTYPE html>
<html lang = "jp">
<head>
<meta charset="utf-8" />
<title> NazoKake</title>
<script type="text/javascript" src="jquery-1.9.1.min.js"></script>
<script type="text/javascript" src="snowfall.jquery.js"></script>
<link rel="stylesheet" href="style.css" />

</head>

<body>



<!--
<script type="text/javascript">
$(document).snowfall({
 flakeCount: 100,
 flakeIndex: 99999,
 maxSpeed: 5,
 minSpeed: 1,
 maxSize: 20,
 minSize: 1,
 image: 'sakura.png'
});
</script>  
-->

<div id="main">
  <div id="nazo" class="form">
      <p><input type="text" value="%s" readonly="readonly"><span class="twice">と</span></p>
    <p class="twice">かけまして</p>
  </div>
  <div id="kake" class="form">
      <p><input type="text" value="%s" readonly="readonly"><span class="twice">と</span></p>
    <p class="twice">解く</p>
  </div>
  <div id="kokoro" class="form">
      <p class="triple">その心は</p>
    <p class="twice left">どちらも</p>
    <p><input type="text" value="%s" readonly="readonly"></p>
    <p class="twice">でしょう</p>
  </div>
  </div>
</div>
</html>
"""

def make_map():
    f = open("relation.csv", "r")
    for x in f:
        x = x.strip().split(',')
        relation[x[0]] = x[1:100]

    f = open("inverse.csv", "r")
    for x in f:
        x = x.strip().split(',')
        inverse[x[0]] = x[1:100]
    f.close()

def solve(word):
    print word
    if word not in relation:
        return (word, choice(relation), "よくわかりません")
    for x in xrange(1000):
        wordR = choice(relation[word]).strip('()').split()
        if len(wordR[0]) < 9:continue
        res = choice(inverse[wordR[0]]).strip('()').split()
        if res[0] != word and res[1] != wordR[1]:
            return (wrod, res[0], wordR[0])
    return (word, choice(relation), "よくわかりません")


import cgi

def main():
    make_map()
    f = cgi.FieldStorage()
    txt = f.getfirst('text', '')
    print html%solve(txt)

main()
