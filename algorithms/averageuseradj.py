from algorithms import AlgorithmBase as A

import numpy as N

class Algorithm(A):
    
    usersToRatings = {}
    ratingAverage=0.0
    useradjK = 3
    
    def train(self,rating):
        
        self.usersToRatings.setdefault(rating[0],[])
        self.usersToRatings[rating[0]].append(rating[2])
        
        self.ratingAverage+=rating[2]
        
    def postTraining(self,dataset):
        self.ratingAverage /= self.ratingCount
        
        #derived from experimentation - average ratings per movie / 2 (=3 for jamendoreviews)
        self.useradjK = self.ratingCount*0.66/len(self.usersToRatings)
        
        
    def predict(self,userId,itemId):
        return (self.ratingAverage*self.useradjK + N.sum(self.usersToRatings.get(userId,[0]))) / (self.useradjK + len(self.usersToRatings.get(userId,[])))
