#-*- coding:utf-8 -*-

f = open("relation.csv", "r")
res  = []
for line in f:
    res += [line]


p = 1
while res != []:
    tmp, res = res[:5000], res[5000:]
    t = open("relation%d.csv"%p, "w")
    for l in tmp:
        t.write(l)
    t.close()
    p += 1

