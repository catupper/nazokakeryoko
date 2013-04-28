#-*- coding:utf-8 -*-
import MeCab
import sys

words = open("word_list.txt", "r")
blackf = open("black_list.txt", "r")


word_list = set()

tagger = MeCab.Tagger('')

hiragana = {}

black = []

nounbl = set()
nounbl.add('副詞可能')
nounbl.add('接尾')
nounbl.add('接続詞的')
nounbl.add('固有名詞')
nounbl.add('数')

word_list=set()

for x in words:
    x = x.strip()
    word_list.add(x)



for x in blackf:
    black += [tagger.parseToNode(x.strip()).next.feature.split(',')[-1]]

relation_file = open("relation.sv", "r")
relation = eval(relation_file.read())


def add_point(x, y, val):
    relation[x][y][0] += val
    if relation[x][y][0] < -1000:
        del relation[x][y]


def save_relations():
    relation_file = open("relation.sv", "w")
    relation_file.write(repr(relation))
    relations = open("relation.csv", "w")
    inverse = open("inverse.csv", "w")
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



#A' -> A作成
    for x in hiragana:
        hiragana[x].sort(reverse = True)
        if len(hiragana[x]) is 0:continue
        c = x
        for _, z in hiragana[x]:
            c += ',(%s %s)'%(z, _[1])
        inverse.write(c + '\n')


def main():
    _, a, b, c = sys.argv
    add_point(a, b, int(c))
    save_relations()

main()
