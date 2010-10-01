from algorithms import AlgorithmBase as A

import numpy as N

class Algorithm(A):
    
    itemsToRatings = {}
    ratingAverage=0.0
    itemadjK = 3
    
    def train(self,rating):
        
        self.itemsToRatings.setdefault(rating[1],[])
        self.itemsToRatings[rating[1]].append(rating[2])
        
        self.ratingAverage+=rating[2]
        
    def postTraining(self,dataset):
        self.ratingAverage /= self.ratingCount
        
        #derived from experimentation - average ratings per movie / 2 (=3 for jamendoreviews)
        self.itemadjK = self.ratingCount*0.5/len(self.itemsToRatings)
        
    def predict(self,userId,itemId):
        return (self.ratingAverage*self.itemadjK + N.sum(self.itemsToRatings.get(itemId,[0]))) / (self.itemadjK + len(self.itemsToRatings.get(itemId,[])))
