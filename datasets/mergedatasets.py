
   

def merge_dataset(newfile, *csvfiles):

    datasetpairs = []
    for csvfile in csvfiles:
        datasetpairs += [( open(csvfile,"r"), dict() )]
         
    
    c = 0
    for f, f_useritem_dict in datasetpairs:         
    
        c += 1
        print 'create dict %s' % c
        for line in f:
            x = line.split(";")
        
            if len(x)>4:
                if f_useritem_dict.has_key(x[0]+'-'+x[1]): raise Exception('not primary key found')
                f_useritem_dict[x[0]+';'+x[1]] = x[2] 
                
            else: raise "found not valid line in %s: %s" % (self.csvfile, line)
    
        f.close()
    
    
    print '\ncreate keys list'
    keys_duplicated = reduce(lambda x,y: x+y, [e[1].keys() for e in datasetpairs])
    #keys_duplicated = f1_useritem_dict.keys() + f2_useritem_dict.keys() + f3_useritem_dict.keys()
    keys = set(keys_duplicated)
    print '%s duplicated keys to %s unique user-item keys' % (len(keys_duplicated), len(keys)) 
    print '\t=> %s%s of times users have rated items only with one of the considered rating tools (review, star, playlist)' % (100*len(keys)/(1.*len(keys_duplicated)), '%')


    print '\nbegin to create new csv file: ' % newfile
    new = open(newfile, "wb")
    for key in keys:
        
        rates = []
        for f_useritem_dict in [e[1] for e in datasetpairs]:         
            if f_useritem_dict.has_key(key): rates += [f_useritem_dict[key]] 
            else: rates += ['0']
        
        row = '%s;(%s);1;0\n' % (key, ','.join(rates))
        new.write(row)
    print 'Done!'
    new.close()



merge_dataset("jamendoalbum_rev_st.csv", "jamendoalbumreviews.csv", "jamendoalbumstarred.csv")
#merge_dataset("jamendoalbumallrates.csv", "jamendoalbumreviews.csv", "jamendoalbumstarred.csv", "jamendoalbumplaylisted.csv")
#merge_dataset("jamendoartistallrates.csv", "jamendoartistreviews.csv", "jamendoartiststarred.csv", "jamendoartiststarredalbums.csv")

     