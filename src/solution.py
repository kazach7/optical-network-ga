"""
Classes providing abstraction for a solution to the problem.
"""

class Solution:
    transponderCosts = [0, 0, 0]
    transpondersCapacities = [0, 0, 0]

    def __init__(self, demands_amount, routes_amount = 7):
        self.genotype = []
        for _ in range(demands_amount):
            self.genotype.append(Gene(routes_amount))

    def calculate_cost(self):
        cost = 0
        for gene in self.genotype:
            cost += gene.calculate_cost()
        
        return cost
    
    # Get list of differences between demands values and their coverages in this solution.
    # divergence > 0 means this much is missing to cover the demand.
    # divergence < 0 means the demand is covered and this much is excessive.
    def get_coverage_divergencies_in_genes(self, demands):
        divergencies = []
        assert(len(self.genotype) == len(demands))
        for i in range(len(self.genotype)):
            divergencies.append(demands[i].value - self.genotype[i].calculate_coverage())
        
        return divergencies
            
    def apply_transponders_to_connections(self, demands):
        # For each gene (demand)...
        for i in range(len(self.genotype)):
            # ...for each allele (link)...
            for j in range(len(self.genotype[i].alleles)):
                # ...for every transponder used on that link add a lambda to every connection
                # used by the link. Choose the smallest lambda number unoccupied on all of the
                # connections.
            
                # Get transponders count on the link.
                transpondersCount = 0
                for t in self.genotype[i].get_allele(j):
                    transpondersCount += t

                # Get connections in that link.
                connections = demands[i].links[j].connections

                # Apply transponders to connections.
                for _ in range(transpondersCount):
                    lambdaNo = 1
                    lambdaOccupied = True
                    while (lambdaOccupied):
                        lambdaOccupied = False
                        for c in connections:
                            if (c.check_if_lambda_occupied(lambdaNo)):
                                lambdaNo += 1
                                lambdaOccupied = True
                                break
                    
                    for c in connections:
                        c.add_lambda(lambdaNo)


# One gene in the solution's genotype - corresponds to one demand.
class Gene:

    def __init__(self, routes_amount):
        self.alleles = []
        # One allele corresponds to one link available to fulfill the demand.
        for _ in range(routes_amount):
            self.alleles.append((0, 0, 0))
        
    def calculate_cost(self):
        cost = 0

        for allele in self.alleles:
            for i in range(3):
                cost += Solution.transponderCosts[i] * allele[i]
        
        return cost
    
    def calculate_coverage(self):
        coverage = 0

        for allele in self.alleles:
            for i in range(3):
                coverage += Solution.transpondersCapacities[i] * allele[i]

        return coverage

    def get_allele(self, pos):
        return self.alleles[pos]

    def set_allele(self, pos, allele):
        self.alleles[pos] = allele
