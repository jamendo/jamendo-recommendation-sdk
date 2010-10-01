import imp

def loadAlgorithm(id,*args,**kwargs):
    
    try:
        fp, pathname, description = imp.find_module(id,__path__)
        assert fp
        return imp.load_module(id.replace(".",""),fp, pathname, description).Algorithm(*args,**kwargs)
    except Exception, e:
        print "error while loading algorithm : %s" % e
        return False



class AlgorithmBase(object):
    
    def __init__(self):
        pass
    
    def trainDataset(self,dataset):
        
        self.preTraining(dataset)
        self.ratingCount = 0
        for r in dataset.iterRatings():
            self.train(r)
            self.ratingCount+=1
        self.postTraining(dataset)
    
    def postTraining(self,dataset):
        pass
    
    def preTraining(self,dataset):
        pass
    
    def train(self,rating):
        pass
    
    def predict(self,userId,itemId):
        
        return (0,0)