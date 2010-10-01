from algorithms import AlgorithmBase as A

import numpy as N


class Algorithm(A):
    
    usersToRatings = {}
    ratingAverage=0.0
    
    def train(self,rating):
        
        self.usersToRatings.setdefault(rating[0],[])
        self.usersToRatings[rating[0]].append(rating[2])
        
        self.ratingAverage+=rating[2]
        
    def postTraining(self,dataset):
        self.ratingAverage /= self.ratingCount
        
    def predict(self,userId,itemId):
        return N.average(self.usersToRatings.get(userId,[self.ratingAverage]))
