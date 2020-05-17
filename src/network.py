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
                taken_lambdas = set([lamb for lambdas in links for lamb in links])
                lambdaNo = 1

                # For every transponder used on the path add a lambda to every link of the path.
                # Choose the smallest lambda number unoccupied on all of the links.
                while (transpondersCount > 0):
                    if lambdaNo not in taken_lambdas:
                        for l in links:
                            l.add_lambda(lambdaNo)
                            taken_lambdas.add(lambdaNo)
                            transpondersCount -= 1
                    
                    lambdaNo += 1

    def clear_network(self):
        for l in self.links:
            l.clear_lambdas()

# Demand, with a value and paths which can be used to realize it.
class Demand:
    def __init__(self, id, value, paths):
        self.id = id
        self.value = value
        self.paths = paths
    
# Path from one city to another, consisting of multiple links.
class Path:
    def __init__(self, links):
        self.links = links

# Direct connection between two cities.
class Link:
    def __init__(self, id, source, dest):
        self.id = id
        self.source = source
        self.dest = dest
        self.lambdas = [] # Lambdas being in use on the connection.
    
    def add_lambda(self, lambdaNo):
        self.lambdas.append(lambdaNo)

    def check_if_lambda_occupied(self, lambdaNo):
        return (lambdaNo in self.lambdas)
    
    def clear_lambdas(self):
        self.lambdas.clear()