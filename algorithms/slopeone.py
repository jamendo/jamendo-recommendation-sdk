#!/usr/bin/env python

import numpy as N

from algorithms.averagedoubleadj import Algorithm as A

class Algorithm(A):

    diffs, freqs, ratings, userRatings = {}, {}, {}, {}  


    def train(self,rating): #rating = u,i,r,w,d
        
        self.freqs.setdefault(rating[1],{})
        self.diffs.setdefault(rating[1],{})
        
        self.userRatings.setdefault(rating[0],[])
        
        self.userRatings[rating[0]].append((rating[1],rating[2],rating[3]))
        
        super(Algorithm,self).train(rating)
        
    def postTraining(self,dataset):
        
        super(Algorithm,self).postTraining(dataset)
        
        for user in self.userRatings:
            for i in self.userRatings[user]:
                for j in self.userRatings[user]:
                    self.freqs[i[0]].setdefault(j[0],0)
                    self.diffs[i[0]].setdefault(j[0],0.0)
                    self.freqs[i[0]][j[0]]+=1
                    self.diffs[i[0]][j[0]]+= i[1]-j[1]
                    
                for j in self.userRatings[user]:
                    self.diffs[i[0]][j[0]]/=self.freqs[i[0]][j[0]]
                    
        
        
    def predict(self, userId,itemId):
        preds, freqs = {}, {}
        
        if (userId not in self.userRatings) or (itemId not in self.diffs) or (self.freqs[itemId]==0):
            return super(Algorithm,self).predict(userId,itemId) #average ratings
        
        for rating in self.userRatings[userId]:
            
            diffratings = self.diffs[itemId]
        
            try:
                freq = self.freqs[itemId][rating[0]]
            except KeyError:
                continue
            preds.setdefault(itemId, 0.0)
            freqs.setdefault(itemId, 0)
            preds[itemId] += freq * (diffratings[rating[0]] + rating[1])
            freqs[itemId] += freq
            
        if itemId not in preds:
            return super(Algorithm,self).predict(userId,itemId)
        
        return preds[itemId]/freqs[itemId]
               