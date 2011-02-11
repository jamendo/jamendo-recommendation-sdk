from datasets.csv import Dataset, Dataset_ratestuple 
import numpy as np
import sys
from datasets.jamendoalbumallrates import combine_album_rates
from datasets.jamendoartistallrates import combine_artist_rates


plot = False


def test_dataset(dataset, CLASS=Dataset, *new_csl_args): 
    global plot

    args = ['datasets/'+dataset] + list(new_csl_args)
    D = CLASS(*args)
    
    users, items = dict(), dict()
    row_len = 0
    for row in D.iterRatings():
        row_len += 1 
        if not users.has_key(row[0]): users[row[0]] = 0  
        users[row[0]] += 1
    
        if not items.has_key(row[1]): items[row[1]] = 0
        items[row[1]] += 1    
        
    uservalues, itemvalues = sorted(users.values(), reverse=True), sorted(items.values(), reverse=True)
    assert row_len == sum(uservalues) == sum(itemvalues)
    filled = row_len * 1.
    
    u_len, i_len = len(uservalues), len(itemvalues)  
    
    print '\n\n**** %s ****' % dataset.upper()
    print '\nmatrix with #users*#items=%s*%s=%s positions, and %s rates,\n\
     => %s%s of the positions is filled with a rate' % (u_len, i_len, u_len*i_len, filled, 100*( filled / (u_len * i_len) ), '%')
     
     
    print '\n %s top 25 raters and rated:' % dataset
    print uservalues[:25]
    print itemvalues[:25]


    if plot == True:
        plt.figure()
        plt.plot(uservalues)
        plt.title(dataset +' rates per user')
        
        plt.figure()
        plt.plot(itemvalues)
        plt.title(dataset + ' rates per item')
    

    
if __name__ == "__main__":     

    #dataset using Dataset_ratestuple: "dataset":rate_algo
    dataset_ratealgo = {"jamendoalbumallrates.csv":combine_album_rates, "jamendoartistallrates.csv":combine_artist_rates}
    
    datasets = [sys.argv[1]]
    
    if datasets == ['all']: 
        datasets = dataset_ratealgo.keys() + ['jamendoalbumreviews.csv', 'jamendoalbumstarred.csv', 'jamendoprocarts.csv']
        
    if plot == True: 
        import matplotlib.pyplot as plt
        
    for dataset in datasets:
        
        args = [dataset]
        if dataset in dataset_ratealgo.keys():
            args += [Dataset_ratestuple, dataset_ratealgo[dataset]]
        test_dataset(*args)
    
    if plot == True: plt.show()




