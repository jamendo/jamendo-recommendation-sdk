
from datasets.csv import Dataset_ratestuple as D


def combine_album_rates( rate_list ):
  
  if all([True if e!=0 else False for e in rate_list]):
      return sum(rate_list) / 3.

  elif (rate_list[0]!=0 and rate_list[1]!=0): 
      return (rate_list[0] + 0.9) / 2.
  
  elif (rate_list[0]!=0 and rate_list[2]!=0):
      return (rate_list[0] + 0.8) / 2.
  
  elif (rate_list[1]!=0 and rate_list[2]!=0):
      return 1.
          
  elif rate_list[0]!=0:
      return rate_list[0]
         
  elif rate_list[1]!=0:
      return 0.9

  elif rate_list[2]!=0:
      return 0.7
  
  elif all([True if e==0 else False for e in rate_list]):
      """happen with reviews rates = 0"""
      return 0.
  else:
      raise Exception('combine_album_rates else: this string should never be printed')

      
    
class Dataset(D):
    
    query = """rate column contain: review rate, 1 if starred, 1 if playlisted"""
    
    def __init__(self):
        self.csvfile = "datasets/jamendoalbumallrates.csv"
        
        self.rate_algo = combine_album_rates