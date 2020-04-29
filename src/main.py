"""
"""
from network import *
from gene import *
import random


def main():
    Gene.transponderCosts = [1, 5, 15]

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

    print("\n")
    gene = Gene(7)
    gene.set_allele(3, (3, 0, 1))
    gene.set_allele(1, (3, 4, 5))

    print("Example cost: {}".format(gene.calculate_cost()))
    


if __name__ == "__main__":
    main()

