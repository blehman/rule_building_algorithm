#!/usr/bin/env python

import sys
import json
import nltk
import operator
from pprint import *

infoStore = {}
def base_predictor_info():
    with open('data/clusterPredictors.tsv') as p:
        """
        Loads the prediction classes
        """
        for line in p.readlines():
            rec = line.strip().split('\t')
            cluster = str(rec[0])
            label = rec[1]
            predictors = rec[2].split(',')
            infoStore[cluster] = {"label":label, "predictors":predictors, "success":0, "fail":0}
    return infoStore

if __name__ == '__main__':

    infoStore = base_predictor_info()
    #print pprint(infoStore)
    for line in sys.stdin:

        # initializes the votes based on 15 clusters
        votes = {str(x):0 for x in range(0,15)}

        # data: 
        # 10|Learning Strategist, Writer, OD Pro. Founder of ADVANCErva. Interested in what's next.
        # 10|Attorney & sorcerer -  can I get a witness? 
        rec = line.decode('utf-8').strip().split('|')

        # assign current cluster
        cluster = rec[0]

        if rec[1] == '':
            continue

        # tokenize bio
        bio = set(nltk.word_tokenize(rec[1]))

        # loop through all clusters
        for clusterCheck in infoStore:

            # loop through all the 
            for predictor in infoStore[clusterCheck]["predictors"]:
                if predictor in bio:
                    votes[clusterCheck]+=1
        # sort votes
        sorted_votes = sorted(votes.items(), key=operator.itemgetter(1), reverse = True)

        # check truth 
        if sorted_votes[0][1] != sorted_votes[1][1]:
            clusterValue = sorted_votes[0][0]
            if cluster == clusterValue: 
                infoStore[cluster]["success"]+=1
            else:
                infoStore[cluster]["fail"]+=1

    print pprint(infoStore)


