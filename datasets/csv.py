
from datasets import DatasetBase

#format is user;item;rating;weight;date

class Dataset(DatasetBase):
    
    def __init__(self,csvfile):
        
        self.csvfile = csvfile
        
    def iterRatings(self):
        
        
        f = open(self.csvfile,"r")
        
        for line in f:
            x = line.split(";")

            if len(x)>4:
                yield (int(x[0]),int(x[1]),float(x[2]),float(x[3]),int(x[4]))
            else: raise "found not valid line in %s: %s" % (self.csvfile, line)
        
        f.close()
        


class Dataset_ratestuple(Dataset):

    def __init__(self,csvfile, rate_algo='default'):
        
        self.csvfile = csvfile
        
        if rate_algo=='default':    
            self.rate_algo = lambda x: 1.
        else: self.rate_algo = rate_algo             
        
    def iterRatings(self):    
        
        f = open(self.csvfile,"r")
        
        for line in f:
            x = line.split(";")
            
            rate_tuple = eval(x[2])
            rate = float(self.rate_algo(rate_tuple))

            if len(x)>4:
                yield (int(x[0]),int(x[1]),rate,float(x[3]),int(x[4]))
            else: raise "found not valid line in %s: %s" % (self.csvfile, line)
        
        f.close()
        
        