"""
Classes providing abstraction for the elements in the network.
"""

class Network:
    def __init__(self, links, demands):
        self.links = links
        self.demands = demands

    def apply_solution_to_network(self, solution):
         # For each demand (gene)...
        for i in range(len(self.demands)):
            # ...for each path (allele)...
            for j in range(len(self.demands[i].paths)):

                # Get transponders count on the path.
                transpondersCount = 0
                for t in solution.genotype[i].get_allele(j):
                    transpondersCount += t

                # Get links from that path.
                links = self.demands[i].paths[j].links

                # For every transponder used on the path add a lambda to every link of the path.
                # Choose the smallest lambda number unoccupied on all of the links.
                for _ in range(transpondersCount):
                    lambdaNo = 1
                    lambdaOccupied = True
                    while (lambdaOccupied):
                        lambdaOccupied = False
                        for l in links:
                            if (l.check_if_lambda_occupied(lambdaNo)):
                                lambdaNo += 1
                                lambdaOccupied = True
                                break
                    
                    for l in links:
                        l.add_lambda(lambdaNo)

    def clear_network(self):
        for l in self.links:
            l.clear_lambdas()

# Demand, with a value and paths which can be used to realize it.
class Demand:
    def __init__(self, demand_id, value, paths):
        self.demand_id = demand_id
        self.value = value
        self.paths = paths
    
# Path from one city to another, consisting of multiple links.
class Path:
    def __init__(self, links):
        self.links = links

# Direct connection between two cities.
class Link:
    def __init__(self, link_id, source, dest):
        self.link_id = link_id
        self.source = source
        self.dest = dest
        self.lambdas = [] # Lambdas being in use on the connection.
    
    def add_lambda(self, lambdaNo):
        self.lambdas.append(lambdaNo)

    def check_if_lambda_occupied(self, lambdaNo):
        return (lambdaNo in self.lambdas)
    
    def clear_lambdas(self):
        self.lambdas.clear()