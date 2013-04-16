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
black = set()

for x in blackf:
    black += [x.strip()]

def add_point(x, y):
    if(x[1].strip().split(',')[0] != '名詞' or y[1].strip().split(',')[1] != '自立'):return
    x = x[0].strip().split(',')[0]
    if x not in relation:
        return
    
    yomi = y[1].strip().split(',')[8]
<<<<<<< HEAD
<<<<<<< HEAD
    reals = y[1].strip().split(',')[6]
    if(y[1].strip().split(',')[0] != '名詞' or y[1].strip().split(',')[1] != '自立'):return
    y = y[0].strip().split(',')[0]
    if yomi in black:
=======
    if(y[1].strip().split(',')[0] != '名詞' or y[1].strip().split(',')[1] != '自立'):
>>>>>>> parent of 3c3fced... add ui
=======
    if(y[1].strip().split(',')[0] != '名詞' or y[1].strip().split(',')[1] != '自立'):
>>>>>>> parent of 3c3fced... add ui
        return
    y = y[0].strip().split(',')[0]
    if y in black:
        return
    
    if yomi not in relation[x]:
        relation[x][yomi] = 0
    relation[x][yomi] += 1

for x in words:
    x = x.strip()
    word_list.add(x)
    relation[x] = {}

#動詞を基本形に変換
def base(node):
    if node.feature.split(',')[0] != "動詞":return node
    it = node.feature.split(',')[6]
    return tagger.parseToNode(it).next
        

#文章解析
#「が」「は」「を」で挟まれた２つをつなぐ
#前->後


pq = 0
for sentenceses in sentences:
    if(pq % 1000 == 0):print pq
    pq += 1
    for sentence in sentenceses.split('。'):
        node = tagger.parseToNode(sentence)
        r = []

        while node:
            tnode = base(node)
            if(tnode.feature.split(',')[0] != "名詞" and tnode.feature.split(',')[1] != "自立"):
                node = node.next
                continue

            if tnode.surface not in relation:
                node = node.next
                continue
        
            if tnode.surface in black:
                node = node.next
                continue

            r.append((tnode.surface, tnode.feature))
            node = node.next

        

        p = len(r)
        for x in xrange(p):
            for y in xrange(x + 1, p):
                try:
                    add_point(r[x], r[y])
                except:
                    print r[x][0], r[y][1]


print "pya2"
#A -> A'作成
for x in word_list:
    relation[x] = relation[x].items()
    relation[x].sort(key = lambda x:x[1], reverse = True)
    c = x
    if len(relation[x][:10]) == 0:continue
    for z, point in relation[x][:10]:
        c += ',%s'%z
        if z not in hiragana:
            hiragana[z] = []
        hiragana[z] += [(poinxt, x)]
    relations.write(c + '\n')
print "here"
#A' -> A作成
for x in hiragana:
    hiragana[x].sort(reverse = True)
    if len(hiragana[x]) is 0:continue
    c = x
    for _, z in hiragana[x]:
        c += ',%s'%z
    inverse.write(c + '\n')
