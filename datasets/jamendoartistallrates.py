
from datasets.csv import Dataset as D


def combine_artist_rates( rate_list ):
    
    return (2*rate_list[0] + rate_list[1] + rate_list[2]) / 4.


class Dataset(D):
    
    query = """rate column contain: artist reviews avg rate, 1 if artist has been starred, (num of albums starred)/(album published)"""
    
    def __init__(self):
        self.csvfile = "datasets/jamendoalbumreviews.csv"
        
        self.rate_algo = combine_artist_rates
        
    