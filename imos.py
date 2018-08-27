import os 
import subprocess
import simhash as si
result=os.environ['PATH']
new_result=result+'//liu//text//'
os.putenv(new_result,'PATH')
print os.environ['PATH']



def find():

	pass

if __name__ == '__main__':
    s = 'To be or not to be ,this is a question'
    hash1 = si.simhash(s.split())
    
    s = 'whether to be is a question'
    hash2 = si.simhash(s.split())
    
    s = 'i have a question to say ,not to be or to be'
    hash3 = si.simhash(s.split())
    
    print(hash1.hamming_distance(hash2) , "   " , hash1.similarity(hash2))
    print(hash1.hamming_distance(hash3) , "   " , hash1.similarity(hash3))
