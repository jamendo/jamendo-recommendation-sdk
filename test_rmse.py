import sys,re

dataset = sys.argv[1]
algorithms = [sys.argv[2]]

ALL_ALGORITHMS = ["rand","flatmedium","averageuser","averageitem","averagedouble","averageuseradj","averageitemadj","averagedoubleadj","averageoffset","slopeone","funksvd"]

from datasets import loadDataset
from algorithms import loadAlgorithm


d = loadDataset(dataset)



def testAlgorithm(dataset,algorithm):


    print "[%s] Splitting learn & probe" % (algorithm)
    #(learn,probe) = dataset.splitInLearnAndProbe(lambda row:row[4]%80==0)
    #(learn,probe) = dataset.splitInLearnAndProbe(lambda row:row[1]!=33 )
    learn_ids = (33,80753,65893,51330,41201,24426, 23932, 16853, 6534, 2131, 43152, 43153, 43155, 43156, 43161, 43162, 43163, 43164, 43169)
    (learn,probe) = dataset.splitInLearnAndProbe(lambda row:row[1] not in learn_ids)
    #(learn,probe) = dataset.splitInLearnAndProbe(lambda row:row[1]!=32)

    a = loadAlgorithm(algorithm)
    
    learn._probe = probe
    
    print "[%s] Training dataset (%s rows of %s total)..." % (algorithm,len(learn.data),len(learn.data)+len(probe.data))
    a.trainDataset(learn)
    
    print "[%s] Computing RMSE..." % (algorithm)
    #return (learn.rmse(a),probe.rmse(a))

    return (0,probe.rmse(a))


if algorithms==["all"]:
    algorithms = ALL_ALGORITHMS
    
res = []

for a in algorithms:
    res.append(testAlgorithm(d,a)+(a,))
    
res.sort(lambda x,y:cmp(x[1],y[1]))

print "Algorithm            \tTest RMSE\tLearn RMSE"
for a in res:
    print "%s : \t%s\t%s" % (a[2].ljust(15," "),a[1],a[0])