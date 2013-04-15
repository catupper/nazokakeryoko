#-*- coding:utf-8 -*-
import MeCab
import CaboCha
words = open("word_list.txt", "r")
sentences = open("wiki.txt", "r")
#sentences = open("jawiki/jawiki-latest-pages-articles.xml-%03d.txt"%47, "r")
blackf = open("black_list.txt", "r")
relations = open("relation.csv", "w")
inverse = open("inverse.csv", "w")

word_list = set()

tagger = MeCab.Tagger('')
c = CaboCha.Parser()
relation = {}
hiragana = {}


#指示語への関係や辞書にない言葉からの関係を排除しつつつなぐ
black = []

for x in blackf:
    black += [tagger.parseToNode(x.strip()).next.feature.split(',')[-1]]

def add_point(x, y):
    x = x[0].strip().split(',')[0]
    if x not in relation:
        return
    yomi = y[1].strip().split(',')[8]
    reals = y[1].strip().split(',')[6]
    y = y[0].strip().split(',')[0]
    if yomi in black:
        return

    if len(yomi) < 9:
        return


    if yomi not in relation[x]:
        relation[x][yomi] = [0, reals]

    relation[x][yomi][0] += 1

for x in words:
    x = x.strip()
    word_list.add(x)
    relation[x] = {}

#動詞を基本形に変換
def base(node):
    if node.feature.split(',')[0] != "動詞":return node
    it = node.feature.split(',')[6]
    return tagger.parseToNode(it).next
        

teach = c.parse("この文は助詞の例を作るのが目的")

WA = teach.token(2).feature
WO = teach.token(6).feature
GA = teach.token(9).feature

#文章解析
#「が」「は」「を」で挟まれた２つをつなぐ
#前->後

p = 0

for sentenceses in sentences:
    p += 1
    if(p % 1000 == 0):print p
    for sentence in sentenceses.split('。'):
        tree = c.parse(sentence)

        r = []
        pp = []
        for x in xrange(tree.token_size()):
            pp.append(x)
            node = tagger.parseToNode(tree.token(x).feature.split(',')[6]).next
            r.append((node.surface, node.feature))
            if tree.token(x).chunk == None:
                pp[-1] = pp[-2]
            
        for x in xrange(tree.token_size()):
            try:
                if(tree.token(x).feature == WA):
                    link_to = pp[x] - 1 + tree.chunk(tree.token(pp[x]).chunk.link).head_pos
                    add_point(r[x - 1], r[link_to])
            except:
                pass

"""        
        for i, word in enumerate(r):
            if word == WA:
                try:
                    add_point(r[i - 1], r[i + 1])
                except:
                    pass
"""         

print "pya2"
#A -> A'作成
for x in word_list:
    relation[x] = relation[x].items()
    relation[x].sort(key = lambda x:x[1], reverse = True)
    c = x
    if len(relation[x][:100]) == 0:continue
    for z, point in relation[x][:100]:
        c += ',(%s %s)'%(z, point[1])
        if z not in hiragana:
            hiragana[z] = []
        hiragana[z] += [(point, x)]
    relations.write(c + '\n')
print "here"

#A' -> A作成
for x in hiragana:
    hiragana[x].sort(reverse = True)
    if len(hiragana[x]) is 0:continue
    c = x
    for _, z in hiragana[x]:
        c += ',(%s %s)'%(z, _[1])
    inverse.write(c + '\n')
