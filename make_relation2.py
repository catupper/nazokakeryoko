#-*- coding:utf-8 -*-
import MeCab

words = open("word_list.txt", "r")
sentences = open("wiki.txt", "r")
blackf = open("black_list.txt", "r")
relations = open("relation.csv", "w")
inverse = open("inverse.csv", "w")

word_list = set()

tagger = MeCab.Tagger('')

relation = {}
hiragana = {}


#指示語への関係や辞書にない言葉からの関係を排除しつつつなぐ
black = []

for x in blackf:
    black += [tagger.parseToNode(x.strip()).next.feature.split(',')[-1]]

aaaaa = set()

hiraganas = "あ,い,う,え,お,か,き,く,け,こ,さ,し,す,せ,そ,た,ち,つ,て,と,な,に,ぬ,ね,の,は,ひ,ふ,へ,ほ,ま,み,む,め,も,や,ゆ,よ,わ,を,ん,ら,り,る,れ,ろ,が,ぎ,ぐ,げ,ご,ざ,じ,ず,ぜ,ぞ,だ,ぢ,づ,で,ど,ば,び,ぶ,べ,ぼ,ぱ,ぴ,ぷ,ぺ,ぽ,ぁ,ぃ,ぅ,ぇ,ぉ,ゃ,ゅ,ょ,っ".split(',')

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



def add_point(x, y):
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
        tmpre = reals
        for xz in hiraganas:
            tmpre = tmpre.replace(xz, '')      
        if tmpre == '':
            return
        relation[x][yomi] = [0, reals]
    relation[x][yomi][0] += 1

for x in words:
    x = x.strip()
    word_list.add(x)
    relation[x] = {}

#動詞を基本形に変換
def base(node):
    if node.feature.split(',')[0] != "動詞" and node.feature.split(',')[0] != "形容詞":return node   
    it = node.feature.split(',')[6]
    return tagger.parseToNode(it).next        

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
    if(p % 10000 == 0):
        print p
    for sentence in sentenceses.split('。'):
        node = tagger.parseToNode(sentence)
        r = []

        while node:
            tnode = base(node)
            r.append((tnode.surface, tnode.feature))
            node = node.next
        
        for i, word in enumerate(r):
            try:
                if word in(WA, GA, WO):
                    add_point(r[i - 1], r[i + 1])
            except:
                pass
            

relation_file = open("relation.sv", "w")
relation_file.write(repr(relation))

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

print "here"


oks = set()
okh = set()
#A' -> A作成
for x in hiragana:
    hiragana[x].sort(reverse = True)
    if len(hiragana[x]) is 0:continue
    p = set()
    for _, z in hiragana[x]:
        p.add(_[1])
    if len(p) is 1:continue
    c = x
    okh.add(x)
    for _, z in hiragana[x]:
        c += ',(%s %s)'%(z, _[1])
        oks.add(z)
    inverse.write(c + '\n')



print "pya2"
#A -> A'作成
for x in word_list:
    c = x 
    if x not in oks:continue
    if len(relation[x][:100]) == 0:continue
    ooo = False
    for z,point in relation[x][:100]:
        if z in okh:
            ooo = True
            break
    if not ooo:continue
    for z, point in relation[x][:100]:
        if z in okh:
            c += ',(%s %s)'%(z, point[1])
    relations.write(c + '\n')

