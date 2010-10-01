import cPickle
import numpy as N
import random

from algorithms.averagedoubleadj import Algorithm as A

MAX_FEATURES     = 5            # Number of features to use 
MIN_EPOCHS       = 1            # Minimum number of epochs per feature
MAX_EPOCHS       = 3           # Max epochs per feature

MIN_IMPROVEMENT  = 0.00005       # Minimum improvement required to continue current feature
LRATE            = 0.1        # Learning rate parameter
K                = 0.0015 #0.015        # Regularization parameter used to minimize over-fitting
INIT             = 0.3          # Initialization value for features
SQR_INIT         = INIT*INIT #0.01         # INIT * INIT

PLOT = False




class Algorithm(A):
    
    
    def postTraining(self,dataset):
        
        super(Algorithm,self).postTraining(dataset)
        
        self.usersMap = {}
        
        
        for index, user in enumerate(dataset.iterUsers()):
            self.usersMap[user] = index-1
        
        self.itemsMap = {}
        
        for index, item in enumerate(dataset.iterItems()):
            self.itemsMap[item] = index-1
        
        self.plot = False
        
        if PLOT:
            
            import Gnuplot, Gnuplot.funcutils
            
            self.plot = Gnuplot.Gnuplot(debug=0)
            self.plot.title('A simple example') # (optional)
            self.plot('set data style linespoints')
            self.plot('set multiplot')
            

            self.plotData = {"rmse":[],"trmse":[]}
        
        
        print 'initializing matrices (%s ratings, %s users, %s items)' % (self.ratingCount,len(self.usersMap),len(self.itemsMap))
        self.itemFeatures = N.empty( (MAX_FEATURES, len(self.itemsMap)+1), 'f' )  # Array of features by item
        self.userFeatures  = N.empty( (MAX_FEATURES, len(self.usersMap)+1),  'f' )  # Array of features by customer
        self.cache         = N.empty( (self.ratingCount+1),               'f' )  # cache all the residuals
        
        self.itemFeatures.fill(INIT)
        self.userFeatures.fill(INIT)
        self.cache.fill(0)
        
        print 'calculating features'
        
        # CalcFeatures
        # - Iteratively train each feature on the entire data set
        # - Once sufficient progress has been made, move on
        
        rmse = 1
    
        iteration = 0
        
        for f in xrange(MAX_FEATURES):
            
            print '--- Calculating feature: ', f, ' ---'
    
            
    
            uff = self.userFeatures[f]
            mff = self.itemFeatures[f]
    
            
            for e in xrange(MAX_EPOCHS):
                iteration+=1
                sqErr     = 0.0
                rmse_last = rmse
    
                for i, v in enumerate(dataset.iterRatings()):
                    
                    # Predict rating and calc error
                    itemId = self.itemsMap[v[1]]
                    userId  = self.usersMap[v[0]]
                    
                    pred = self.predictWhileTraining(v[0], v[1], f, self.cache[i], True)
                    err     = v[2] - pred
                    sqErr  += err*err

                    # Cache off old feature values
                    cf =  uff[userId]
                    mf = mff[itemId]
    
                    #print (pred,v[2],err,mf,cf,(LRATE * (err * mf - K * cf)),(LRATE * (err * cf - K * mf)))
    
                    # Cross-train the features
                    uff[userId]  += (LRATE * (err * mf - K * cf))
                    mff[itemId] += (LRATE * (err * cf - K * mf))
    
                    if (i % 1000 == 0): print '.',
                
                rmse = (sqErr / self.ratingCount) ** 0.5
                trmse = dataset._probe.rmse(self)
                print 'e = ', e, ', square error = ', sqErr, ' rmse = ', rmse , "trmse = ", trmse
                
                if self.plot:
                    self.plot.reset()
                    self.plotData["rmse"].append([iteration,rmse])
                    self.plotData["trmse"].append([iteration,trmse])
                    
                    self.plot.plot(self.plotData["rmse"])
                    self.plot.plot(self.plotData["trmse"])
                    
                
                # Keep looping until you have passed a minimum number 
                # of epochs or have stopped making significant progress 
                if (e >= MIN_EPOCHS and rmse > rmse_last - MIN_IMPROVEMENT): break
    
            print "AVG : item=%s user=%s / MIN-MAX : item=%s %s  user=%s %s" % (N.average(uff),N.average(mff),min(mff),max(mff),min(uff),max(uff))
    
            # Cache off old predictions
            for i, v in enumerate(dataset.iterRatings()):
                self.cache[i] = self.predictWhileTraining(v[0],v[1], f, self.cache[i], False)

        
        
        """
        print 'saving features'
        fOut = open('userFeatures', 'wb')
        cPickle.dump(userFeatures, fOut, protocol=-1)
        fOut.close()
        
        fOut = open('movieFeatures', 'wb')
        cPickle.dump(movieFeatures, fOut, protocol=-1)
        fOut.close()
        """
        
    def predictWhileTraining(self,userId,itemId,feature, cache, bTrailing = True):
    
        # PredictRating
        # - During training there is no need to loop through all of the features
        # - Use a cache for the leading features and do a quick calculation for the trailing
        # - The trailing can be optionally removed when calculating a new cache value
    
        # Get cached value for old features or default to an average
        if (cache > 0):
            sum = cache
        else:
            sum = super(Algorithm,self).predict(userId,itemId) - (MAX_FEATURES*SQR_INIT)
        
        
        # Add contribution of current feature
        sum += self.itemFeatures[feature][self.itemsMap[itemId]] * self.userFeatures[feature][self.usersMap[userId]]
        if (sum > 1): sum = 1
        if (sum < 0): sum = 0
    
    
        # Add up trailing defaults values
        if (bTrailing):
            sum += (MAX_FEATURES-feature-1) * SQR_INIT
            if (sum > 1): sum = 1
            if (sum < 0): sum = 0
    
        return sum

    def predict(self,userId,itemId):
    
        # PredictRating
        # - This version is used for calculating the final results
        # - It loops through the entire list of finished features
        
        sum = super(Algorithm,self).predict(userId,itemId) #0.0
        
        #unknown user or movie
        if (not userId in self.usersMap) or (not itemId in self.itemsMap):
            return sum
        
        sum-=(MAX_FEATURES*SQR_INIT)
        
        for f in xrange(MAX_FEATURES):
            sum += self.itemFeatures[f][self.itemsMap[itemId]] * self.userFeatures[f][self.usersMap[userId]]
            if (sum > 1): sum = 1
            if (sum < 0): sum = 0
        
        return sum

