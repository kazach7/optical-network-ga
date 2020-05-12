"""
Classes providing abstraction for a solution to the problem.
"""

# Represents a single solution of the optimized problem.
class Solution:
    transponderCosts = [1, 5, 15]
    transpondersCapacities = [10, 40, 100]

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

# One gene in the solution's genotype - corresponds to one demand.
class Gene:
    def __init__(self, allele_count):
        self.alleles = []
        # One allele corresponds to one link available to fulfill the demand.
        for _ in range(allele_count):
            self.alleles.append([0, 0, 0])
        
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
