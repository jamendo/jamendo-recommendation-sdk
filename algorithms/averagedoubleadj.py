from algorithms._linearcomb import Algorithm as A
from algorithms import loadAlgorithm

import numpy as N


class Algorithm(A):
    
    def __init__(self):
        self.setAlgorithms([("averageuseradj",1),("averageitemadj",1)])
        
    def postTraining(self,dataset):
        super(Algorithm,self).postTraining(dataset)
        
        self.algos["averageitemadj"]["object"].itemadjK = 0.5
        self.algos["averageuseradj"]["object"].useradjK = 0.4