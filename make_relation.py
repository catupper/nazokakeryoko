#-*- coding:utf-8 -*-
import MeCab
import CaboCha

words = open("word_list.txt", "r")
sentences = open("smallwiki.txt", "r")
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

aaaaa = set()

nounbl = set()
nounbl.add('副詞可能')
nounbl.add('接尾')
nounbl.add('接続詞的')
nounbl.add('固有名詞')
nounbl.add('数')
def jiritu(x):
    if(x[0] == '名詞'):
        aaaaa.add(x[1])
    return (x[0] == '名詞' or x[1] == '自立' )and x[1] not in nounbl 


#動詞を基本形に変換
def base(node):
    if node.feature.split(',')[0] != "動詞" and node.feature.split(',')[0] != "形容詞":return node   
    it = node.feature.split(',')[6]
    return tagger.parseToNode(it).next        


def add_point(x, y):
    x = base(x)
    y = base(y)
    print x[0], y[0]
    if not jiritu(x[1].strip().split(',')):
        return 
    x = x[0].strip().split(',')[0]
    if x not in relation:
        return

    yomi = y[1].strip().split(',')[8]
    reals = y[1].strip().split(',')[6]
    if not jiritu(y[1].strip().split(',')):
        return
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


teach = tagger.parseToNode("この文とは助詞の例を作るのが目的")
x = []
while teach:
    x.append((teach.surface, teach.feature))
    teach = teach.next

TO = x[3]
WA = x[4]
WO = x[8]
GA = x[11]

#文章解析
#「が」「は」「を」で挟まれた２つをつなぐ
#前->後

p = 0
for sentenceses in sentences:
    p += 1
    if(p % 1000 == 0):
        print p
    for sentence in sentenceses.split('。'):
        tree = c.parse(sentence)
        node = tagger.parseToNode(sentence)

        for x in xrange(tree.chunk_size() - 1):
            try:
                if tree.token(x).feature == TO[1] and tree.token(x + 1).feature == WA[1]:
                    start = 0
                    for y in xrange(x, -1, -1):
                        if tree.token(y).chunk:
                            start = y
                            break
                    destination = tree.chunk(start).link
                    real_destination = 0
                    for y in xrange(x, -1, -1):
                        if tree.token(y).chunk:
                            if tree.token(y).chunk.link == destination:
                                real_destination = y
                    if real_destination == x:
                        real_destination = destination
                    real_destination = tree.chunk(real_destination).token_pos
                    start = tree.chunk(start).token_pos
                    start = (tree.token(start).feature.split(',')[6], tree.token(start).feature)
                    real_destination = (tree.token(real_destination).feature.split(',')[6], tree.token(real_destination).feature.split(',')[6])
                    add_point(start, real_destination)
            except: 
                pass

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

for x in list(aaaaa):
    print x
