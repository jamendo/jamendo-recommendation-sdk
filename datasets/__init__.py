import imp

def loadDataset(id,*args,**kwargs):
    
    try:
        fp, pathname, description = imp.find_module(id,__path__)
        assert fp
        return imp.load_module(id.replace(".",""),fp, pathname, description).Dataset(*args,**kwargs)
    except Exception, e:
        print "error while loading dataset : %s" % e
        return False


class DatasetBase():
    
    
    def __init__(self):
        self.data=[]
        self._cache_iterRatingsByUser=False
        self._cache_iterRatingsOfItem=False
        
        
        pass
    
    # yields user,item,rating,weight,date
    def iterRatings(self):
        
        _cache_iterRatingsByUser_data={}
        _cache_iterRatingsOfItem_data={}
        
        for x in self.data:
            _cache_iterRatingsByUser_data.setdefault(x[0],[])
            _cache_iterRatingsByUser_data[x[0]].append(tuple(x[1:5]))
            
            _cache_iterRatingsOfItem_data.setdefault(x[1],[])
            _cache_iterRatingsOfItem_data[x[1]].append((x[0],x[2],x[3],x[4]))
            
            yield x
            
        # make cache
        self._cache_iterRatingsByUser = _cache_iterRatingsByUser_data
        self._cache_iterRatingsOfItem = _cache_iterRatingsOfItem_data
    
    def iterUsers(self):
        users = set()
        
        for u,i,r,w,d in self.iterRatings():
            if not u in users:
                users.add(u)
                yield u
    
    
    def iterItems(self):
        users = set()
        
        for u,i,r,w,d in self.iterRatings():
            if not i in users:
                users.add(i)
                yield i
        
    def iterRatingsOfItem(self,itemId):
        
        if self._cache_iterRatingsOfItem:
            for x in self._cache_iterRatingsOfItem[itemId]:
                yield x
        else:
            for u,i,r,w,d in self.iterRatings():
                if i==itemId:
                    yield (u,r,w,d)
    
    def iterRatingsByUser(self,userId):
        
        if self._cache_iterRatingsByUser:
            for x in self._cache_iterRatingsByUser[userId]:
                yield x
        else:
            for u,i,r,w,d in self.iterRatings():
                if u==userId:
                    yield (i,r,w,d)
                    
    
    
    #split a dataset in probe & learn datasets
    def splitInLearnAndProbe(self,splitFunction):
        
        learn = DatasetBase()
        probe = DatasetBase()
        
        for x in self.iterRatings():
            if splitFunction(x):
                probe.data.append(x)
            else:
                learn.data.append(x)
                
        
        
        return (learn,probe)
    
    
    def rmse(self, algorithm):
        '''Compute the root mean squared error of the given algorithm on this
        dataset.
        '''
        
        s=0.0; n=0
        for u,i,r,w,d in self.iterRatings():
            
            d = algorithm.predict(u,i) - r
            s += d*d
            n += 1
            #print (u,i,d)
        return (s/n) ** 0.5