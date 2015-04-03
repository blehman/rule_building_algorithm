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
        Loads the prediction classes and initalizes infoStore
        """
        for line in p.readlines():
            rec = line.strip().split('\t')
            cluster = str(rec[0])
            label = rec[1]
            predictors = rec[2].split(',')
            infoStore[cluster] = {
                    "label":label
                    , "predictors":predictors
                    , "success":0
                    , "fail":0
                    , "counts":{str(x):0 for x in range(0,15)}
                    }
    return infoStore


if __name__ == '__main__':

    infoStore = base_predictor_info()
    #print pprint(infoStore)
    for line in sys.stdin:

        # initializes the votes based on 15 clusters
        votes = {str(x):0 for x in range(0,15)}

        # data 
        rec = line.decode('utf-8').strip().split('|')

        # assign current cluster
        cluster = rec[0]

        if rec[1] == '':
            continue

        # tokenize bio
        bio = set(nltk.word_tokenize(rec[1]))

        # loop through all clusters
        for clusterCheck in infoStore:

            # loop through all the predictive terms
            for predictor in infoStore[clusterCheck]["predictors"]:
                if predictor in bio:
                    votes[clusterCheck]+=1
        # sort votes
        sorted_votes = sorted(votes.items(), key=operator.itemgetter(1), reverse = True)

        # remove ties
        if sorted_votes[0][1] != sorted_votes[1][1]:
            clusterValue = sorted_votes[0][0]
            infoStore[cluster]["counts"][clusterValue]+=1
            # count successes and failures
            if cluster == clusterValue: 
                infoStore[cluster]["success"]+=1
            else:
                infoStore[cluster]["fail"]+=1
    print pprint(infoStore)
    with open('rdata/counts.json','wb') as c:
        c.write(json.dumps(infoStore))
