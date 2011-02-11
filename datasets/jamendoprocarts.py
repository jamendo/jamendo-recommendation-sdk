
from datasets.csv import Dataset as D

class Dataset(D):
    
    query = 'SELECT sale_id,data,1,1,UNIX_TIMESTAMP(date_added) FROM `pro_sales_data` WHERE sale_id IN (SELECT id FROM `pro_sales` WHERE `product_id` = 6 AND `paid` = 1) and type="track"'
    
    def __init__(self):
        self.csvfile = "datasets/jamendoprocarts.csv"
    