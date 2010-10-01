from algorithms import AlgorithmBase as A

import numpy as N


class Algorithm(A):
    
    itemsToRatings = {}
    usersToRatings = {}
    ratingAverage=0.0
    
    def train(self,rating):
        
        self.itemsToRatings.setdefault(rating[1],[])
        self.itemsToRatings[rating[1]].append(rating[2])
        
        self.usersToRatings.setdefault(rating[0],[])
        self.usersToRatings[rating[0]].append(rating[2])
        
        self.ratingAverage+=rating[2]
        
    def postTraining(self,dataset):
        self.ratingAverage /= self.ratingCount
        
    def predict(self,userId,itemId):
        return (N.average(self.itemsToRatings.get(itemId,[self.ratingAverage])) + N.average(self.usersToRatings.get(userId,[self.ratingAverage]))) /2