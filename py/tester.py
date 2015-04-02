#!/usr/bin/env python

import sys
import json
import nltk
import operator

infoStore = {}

with open('data/clusterPredictors.tsv') as p:
    for line in p.readlines():
        rec = line.strip().split('\t')
        cluster = rec[0]
        label = rec[1]
        predictors = rec[2].split(',')
        infoStore[cluster] = {"label":label, "predictors":predictors, "success":0, "fail":0}

for line in sys.stdin:
    votes = {x:0 for x in range(1,11)}
    rec = line.strip().split('|')
    cluster = rec[0]
    bio = set(nltk.word_tokenize(rec[1]))
    for clusterCheck in infoStore:
        for item in infoStore[clusterCheck]["predictors"]:
            if item in bio:
                votes[clusterCheck]+=1
    # sort votes
    sorted_votes = sorted(votes.items(), key=operator.itemgetter(1))
    print sorted_votes
    if sorted_votes[0][1] != sorted_votes[1][1]:
        print cluster,",",sorted_votes[0]
    else:
        print "FAIL"
