#-*- coding:utf-8 -*-
from random import choice
relation = {}
inverse = {}

def make_map():
    f = open("relation.csv", "r")
    for x in f:
        x = x.strip().split(',')
<<<<<<< HEAD
<<<<<<< HEAD
        relation[x[0]] = x[1:100]
=======
        relation[x[0]] = x[1:]
>>>>>>> parent of 5cb8e9c... change glaph
=======
        relation[x[0]] = x[1:]
>>>>>>> parent of 5cb8e9c... change glaph

    f = open("inverse.csv", "r")
    for x in f:
        x = x.strip().split(',')
<<<<<<< HEAD
<<<<<<< HEAD
        inverse[x[0]] = x[1:100]
=======
        inverse[x[0]] = x[1:]
>>>>>>> parent of 5cb8e9c... change glaph
=======
        inverse[x[0]] = x[1:]
>>>>>>> parent of 5cb8e9c... change glaph
    f.close()

def solve(word):
    print word
    if word not in relation:
        return "わからぬ"
    for x in xrange(1000):
        wordR = choice(relation[word]).strip('()').split()
        if len(wordR[0]) < 9:continue
        res = choice(inverse[wordR[0]]).strip('()').split()
        if res[0] != word and res[1] != wordR[1]:
            print res[0], wordR[0]
            print res[1], wordR[1]
            return "どや"
    return "わからぬ"

def main():
    make_map()
    while True:
        print solve(raw_input())

main()
