from algorithms import AlgorithmBase as A

import numpy as N


class Algorithm(A):
    
    itemsToRatings = {}
    usersToRatings = {}
    userOffsets = {} #offset to default rating
    ratingAverage=0.0
    
    def train(self,rating):
        
        self.itemsToRatings.setdefault(rating[1],[])
        self.itemsToRatings[rating[1]].append(rating[2])
        
        self.usersToRatings.setdefault(rating[0],[])
        self.usersToRatings[rating[0]].append(rating[2])
        
        self.ratingAverage+=rating[2]
        
    def postTraining(self,dataset):
        self.ratingAverage /= self.ratingCount
        
        for u,i,r,w,d in dataset.iterRatings():
            self.userOffsets.setdefault(u,0)
            self.userOffsets[u]+=(r-N.average(self.itemsToRatings[i]))
        
        for u in self.userOffsets:
            self.userOffsets[u]/=len(self.usersToRatings[u])
            
    def predict(self,userId,itemId):
        return N.average(self.itemsToRatings.get(itemId,[self.ratingAverage])) + self.userOffsets.get(userId,0)
