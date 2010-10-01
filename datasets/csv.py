
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
            
        f.close()