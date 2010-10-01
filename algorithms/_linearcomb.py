from algorithms import AlgorithmBase as A
from algorithms import loadAlgorithm

import numpy as N


class Algorithm(A):
    
    
    def setAlgorithms(self,algos):
        self.algos = {}
        wsum = sum([algo[1] for algo in algos])
        for algo in algos:
            self.algos[algo[0]] = {"weight":algo[1]*1.0/wsum,"object":loadAlgorithm(algo[0])}
            
    def train(self,rating):
        [a["object"].train(rating) for a in self.algos.values()]
        
    def postTraining(self,dataset):
        for a in self.algos.values():
            a["object"].ratingCount = self.ratingCount
        [a["object"].postTraining(dataset) for a in self.algos.values()]
        
    def preTraining(self,dataset):
        [a["object"].preTraining(dataset) for a in self.algos.values()]
        
    def predict(self,userId,itemId):
        
        return sum([a["object"].predict(userId,itemId)*a["weight"] for a in self.algos.values()])