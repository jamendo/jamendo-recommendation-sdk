import cPickle
import numpy as N
import random

from algorithms.averagedoubleadj import Algorithm as A

from algorithms._utils import distance_euclidean,distance_pearson

class Algorithm(A):
    
    
    
    
    def preTraining(self,dataset):
        
        super(Algorithm,self).preTraining(dataset)
        
        self.dataset = dataset
        self.usersMap = {}
        self.itemsMap = {}
        self.usersToRatings = {}
        self.itemsToRatings = {}
        
        for index, user in enumerate(dataset.iterUsers()):
            self.usersMap[user] = index-1
        
        for index, item in enumerate(dataset.iterItems()):
            self.itemsMap[item] = index-1
        
    
    def train(self,rating):
        
        super(Algorithm,self).train(rating)
        
        self.usersToRatings.setdefault(rating[0],[])
        self.usersToRatings[rating[0]].append(rating[2])
        
    
    def postTraining(self,dataset):
        
        super(Algorithm,self).postTraining(dataset)
        
        
        
        #compute distance between each user
        self.itemSimilarity = N.empty((len(self.itemsMap),(len(self.itemsMap))))
        self.itemSimilarity.fill(-1)
        self.dataset=dataset
        
    def predict(self,userId,itemId):
        
        avg = super(Algorithm,self).predict(userId,itemId) #0.0
        
        #unknown user or movie
        if (not userId in self.usersMap) or (not itemId in self.itemsMap):
            return avg
        
        sum = 0.0
        
        #distance = distance_pearson #euclidean
        distance = distance_euclidean
        
        
        totalsim = 0.0
        
        for i,r,w,d in self.dataset.iterRatingsByUser(userId):
            sim = self.itemSimilarity[self.itemsMap[itemId]][self.itemsMap[i]]
            print (i,sim)
            if sim==-1:
                sim = distance(self.dataset.iterRatingsOfItem,itemId,i)
                self.itemSimilarity[self.itemsMap[itemId]][self.itemsMap[i]]=sim
            sum+=r*sim
            totalsim+=sim
            
        if totalsim==0:
            return avg
        
        return sum/totalsim
    

