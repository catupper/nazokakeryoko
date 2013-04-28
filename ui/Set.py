
#!/usr/bin/python
#-*- coding:utf-8 -*-
from random import choice
relation = {}
inverse = {}

html = open("ask.html","r").read()
import cgi

def main():
    f = cgi.FieldStorage()
    txt = f.getfirst('grade', '')
    p = txt.split(',')
    ans = p[0]
    p = p[1:]
    if ans == "YES":
        print '''
<html><script type="text/javascript">
function link(){location.href='../';}
link();
</script></html>
'''
    else:
        print html%(p[0], p[2],p[0], p[2], p[0], p[2], p[1], p[2], p[1], p[2], p[1], p[2])
        

main()
