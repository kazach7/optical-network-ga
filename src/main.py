"""
Application startup; parses arguments, starts the algorithm and displays its final results. 
"""
from network import *
from solution import Solution
from algorithm import AlgorithmPerformer
import config
import xml.etree.ElementTree as ET
import random
import argparse
from profiling_tools import measure_time

@measure_time
def main():
    parser = argparse.ArgumentParser(
        description="Program using genetic algorithm for solving a \
                     problem of demand in optic networks")

    parser.add_argument("path", type=str, help="path to an xml file with the network")
    parser.add_argument("--capacity", metavar="fiberCapacity", type=int,
                        help ="maximum number of lambdas in the fiber")
    parser.add_argument("--costs", type=int, nargs="+",
                        help="costs of 10G, 40G and 100G transponder")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Print additional info")

    args = parser.parse_args()

    network = parseNetwork(args.path)
    
    fiber_capacity = args.capacity if args.capacity is not None else config.FIBER_CAPACITY
    Solution.transponderCosts = tuple(args.costs) if args.costs is not None else config.TRANSPONDER_COSTS

    if len(Solution.transponderCosts) != 3:
        print("There must be provided three costs of transponders!")
        return

    solver = AlgorithmPerformer(network, fiber_capacity)
    solver.verbose = args.verbose
    
    winner = solver.perform_algorithm(config.POPULATION_SIZE, config.ITERATIONS, config.MUTATION_PROBABILITY)
    winner.present(network, fiber_capacity)
    print ("\nConfiguration:")
    print ("Fiber capacity: {}".format(fiber_capacity))
    print ("Popultaion size: {}".format(config.POPULATION_SIZE))
    print ("Mutation probability: {}".format(config.MUTATION_PROBABILITY))
    print ("Overfilled fiber punishment factor: {}".format(config.OVERFILLED_FIBER_PUNISHMENT_FACTOR))
    print ("Unfulfilled demand punishment factor: {}".format(config.UNFULFILLED_DEMAND_PUNISHMENT_FACTOR))
    
   
def parseNetwork(path):
        tree = ET.parse(path)
        root = tree.getroot()

        links = []
        for link in root[0][1]:
            link_id = link.get('id')
            source = link[0].text
            dest = link[1].text
            links.append(Link(link_id, source, dest))

        temp_dictionary = {link.id:link for link in links}

        demands = []
        for demand in root[1]:
            demand_id = demand.get('id')
            value = float(demand[2].text)

            paths = []
            for path in demand[3]:

                links_of_path = []
                for l in path:
                    links_of_path.append(temp_dictionary[l.text])

                paths.append(Path(links_of_path))

            demands.append(Demand(demand_id, value, paths))

        return Network(links, demands)


if __name__ == "__main__":
    main()

