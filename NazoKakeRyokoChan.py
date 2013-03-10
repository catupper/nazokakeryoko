#-*- coding:utf-8 -*-
from random import choice
relation = {}
inverse = {}

def make_map():
    f = open("relation.csv", "r")
    for x in f:
        x = x.strip().split(',')
        relation[x[0]] = x[1:]

    f = open("inverse.csv", "r")
    for x in f:
        x = x.strip().split(',')
        inverse[x[0]] = x[1:]
    f.close()

def solve(word):
    if word not in relation:
        return "わからぬ"
    for x in xrange(100):
        wordR = choice(relation[word])
        res = choice(inverse[wordR])
        if res != word:
            print res, wordR
            return res, wordR
    return "わからぬ"

def main():
    make_map()
    while True:
        print solve(raw_input())

main()
