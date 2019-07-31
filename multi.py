import time
import math
from multimethod import multimethod



def calculate_time(func):
    def inner1(*args, **kwargs): 
    
        begin = time.time() 
          
        func(*args, **kwargs) 
        
        end = time.time() 
        print("Total time taken in : ", func.__name__, end - begin) 
  
    return inner1 

@calculate_time
def factori(num):
    print(math.factorial(num))
    time.sleep(2)
    
print(factori(5))