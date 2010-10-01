
from datasets.csv import Dataset as D

class Dataset(D):
    
    query = 'SELECT user_id,album_id,1,1,0/*UNIX_TIMESTAMP(date_star)*/ FROM album_user WHERE star=1'
    
    def __init__(self):
        self.csvfile = "datasets/jamendoalbumstarred.csv"
        
    