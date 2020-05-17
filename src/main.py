"""
"""
import xml.etree.ElementTree as ET
from network import *
from solution import Solution
from algorithm import AlgorithmPerformer
import random
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Program using genetic algorithm for solving a \
                     problem of demand in optic networks")

    parser.add_argument("path", type=str, help="path to an xml file with the network")
    parser.add_argument("--capacity", metavar="fiberCapacity", type=int, required=True,
                        help ="maximum number of lambdas in the fiber")
    parser.add_argument("--costs", type=int, nargs="+",
                        help="costs of 10G, 40G and 100G transponder")

    args = parser.parse_args()

    network = parseNetwork(args.path)
    fiber_capacity = args.capacity
    if args.costs is not None:
        if len(args.costs) != 3:
            print("costs flag must be given exactly 3 values!")
            return
        Solution.transponderCosts = tuple(args.costs)

    solver = AlgorithmPerformer(network, fiber_capacity)
    
    population_size = 10
    iterations = 80
    mutation_probability = 0.005
    winner = solver.perform_algorithm(population_size, iterations, mutation_probability)
    
    winner.present(network, fiber_capacity)

    #solution = Solution(len(network.demands), len(network.demands[0].paths))
    #solution.genotype[0].set_allele(3, (3, 0, 1))
    #solution.genotype[0].set_allele(1, (3, 4, 5))
    #print("Example cost: {}".format(solution.calculate_cost()))
   
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

