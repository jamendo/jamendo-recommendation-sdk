from algorithms import AlgorithmBase as A

import numpy as N


class Algorithm(A):
    
    itemsToRatings = {}
    usersToRatings = {}
    userOffsets = {} #offset to default rating
    itemOffsets = {} #offset to default rating
    
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
            self.userOffsets[u] = N.average(self.usersToRatings[u])-N.average(self.itemsToRatings[i])
            
        
        for u,i,r,w,d in dataset.iterRatings():
            self.itemOffsets.setdefault(i,0)
            self.itemOffsets[i]+=(r-N.average(self.usersToRatings[u]))
        
        for i in self.itemOffsets:
            self.itemOffsets[i]/=len(self.itemsToRatings[i])
            
    def predict(self,userId,itemId): #N.average(self.itemsToRatings.get(itemId,[self.ratingAverage]))
        return self.ratingAverage + self.userOffsets.get(userId,0) + self.itemOffsets.get(itemId,0)
