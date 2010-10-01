
from datasets.csv import Dataset as D

class Dataset(D):
    
    query = 'SELECT user_id,join_id,note/10,IF(source_type="user",0.5,1),UNIX_TIMESTAMP(date_added) FROM reviews2 WHERE unit="album" and note IS NOT NULL'
    
    def __init__(self):
        self.csvfile = "datasets/jamendoalbumreviews.csv"
        
    