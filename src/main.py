"""
"""
from network import *
import random

def main():
    connections = [Connection(1,2), Connection(2,3), 
                   Connection(3,4), Connection(2,4)]

    demands = []
    links = [Link([connections[0], connections[3]])]
    demands.append(Demand(random.randint(1,100), links))

    i = 0
    for d in demands:
        print ("Demand %d:" % i)
        i += 1
        j = 0
        for l in d.links:
            print ("\tLink %d:" % j)
            j += 1
            k = 0
            print ("\t\t", end = '')
            for c in l.connections:
                print (c.cities, end = '  ')
                k += 1
                if (k > 7): print("\n\t\t", end = '')

    
main()

