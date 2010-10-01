import numpy as N

def distance_euclidean(iter,u1,u2):
    
    # Get the list of shared_items 
    si={} 
    
    sum = 0
    
    for i,r,w,d in iter(u1):
        for i2,r2,w2,d2 in iter(u2):
            if i==i2:
                si[i]=1
                sum+=pow(r-r2,2)
    
    if len(si)==0:
        return 0
    
    return 1.0/(1+sum)


def distance_pearson(iter,u1,u2):
    
    # Get the list of shared_items 
    si={} 
    
    sum1 = 0
    sum2 = 0
    sum1Sq = 0
    sum2Sq = 0
    pSum = 0
    
    for i,r,w,d in iter(u1):
        for i2,r2,w2,d2 in iter(u2):
            if i==i2:
                si[i]=1
                sum1+=r
                sum2+=r2
                sum1Sq+=r*r
                sum2Sq+=r2*r2
                pSum+=r*r2
    
    n=len(si)
    
    if n==0:
        return 0
    
    
    num = pSum - (sum1*sum2/n)
    den = N.sqrt(round((sum1Sq-sum1*sum1/n)*(sum2Sq-sum2*sum2/n),14))
    
    if den==0:
        return 0
    
    return num/den
    