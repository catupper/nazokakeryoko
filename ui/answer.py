#-*- coding:utf-8 -*-
import cgi

from google.appengine.ext import db
from google.appengine.ext.db import Key

class Dictionary(db.Model):
    filename = db.StringProperty()
    word = db.StringProperty()
    content = db.TextProperty()


def main():
    f = cgi.FieldStorage()
    for x in xrange(1,3):
        ans,a,b = f.getfirst('q%d'%x,'').split(',')
        if(ans != "YES"):
            relapplicant = [x for x in Dictionary.gql("WHERE filename=:relationcsv AND word=:word",relationcsv = "relation.csv", word=a.decode('utf-8'))][0]
    
            relation = map(lambda x:x.strip('()').split() , relapplicant.content.encode('utf-8').split(','))
            target = 0
            for i, token in enumerate(relation):
                if(token[0] == b):
                    target = i
            del relation[target]
            relapplicant.content = ','.join(map(lambda x:'('+' '.join(x)+')', relation)).decode('utf-8')
            relapplicant.put()
            
            invapplicant = [x for x in Dictionary.gql("WHERE filename=:inversecsv AND word=:yomi", inversecsv="inverse.csv", yomi=b.decode('utf-8'))][0]
            inverse = map(lambda x:x.strip('()').split(), invapplicant.content.encode('utf-8').split(','))
            target = 0
            for i, token in enumerate(inverse):
                if(token[0] == a):
                    target = i
            del inverse[target]
            invapplicant.content = ','.join(map(lambda x:'('+' '.join(x)+')', inverse)).decode('utf-8')
            invapplicant.put()
    print '''
<html><script type="text/javascript">
function link(){location.href='../';}
link();
</script></html>
'''


main()


