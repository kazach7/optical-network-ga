"""
"""
from network import *
from solution import *
import random
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Program using genetic algorithm for solving a \
                     problem of demand in optic networks")

    parser.add_argument("--costs", type=int, nargs="+",
                        help="costs of 10G, 40G and 100G transponder")

    args = parser.parse_args()

    if args.costs is not None:
        if len(args.costs) != 3:
            print("costs flag must be given exactly 3 values!")
            return

        Solution.transponderCosts = tuple(args.costs) 

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
    solution = Solution(7)
    solution.set_allele(3, (3, 0, 1))
    solution.set_allele(1, (3, 4, 5))

    print("Example cost: {}".format(solution.calculate_cost()))
    


if __name__ == "__main__":
    main()

