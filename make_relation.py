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

def jiritu(x):
    return x[0] == '名詞' or x[1] == '自立'

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

teach = tagger.parseToNode("この文は助詞の例を作るのが目的")
x = []
while teach:
    x.append((teach.surface, teach.feature))
    teach = teach.next

WA = x[3]
WO = x[7]
GA = x[10]

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
        r = []
        
        for x in xrange(tree.chunk_size()):
            try:
                g = tree.chunk(x)
                if g.link < 0 :continue
                a = tree.token(g.token_pos + g.head_pos).feature.split(',')[6]
                a = base(tagger.parseToNode(a).next)
                f = tree.chunk(g.link)
                b = tree.token(f.token_pos + f.func_pos).feature.split(',')[6]
                b = base(tagger.parseToNode(b).next)
                add_point((a.surface, a.feature), (b.surface, b.feature))
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

