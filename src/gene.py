"""
class Gene

Class providing a solution to a problem for a given demand.
"""

class Gene:

    transponderCosts = [0, 0, 0]

    def __init__(self, routes_amount = 7):
        # Initialize genotype
        self.genotype = []
        for _ in range(routes_amount):
            self.genotype.append((0, 0, 0))
        
    def calculate_cost(self):
        cost = 0

        for allele in self.genotype:
            for i in range(3):
                cost += Gene.transponderCosts[i] * allele[i]
        
        return cost

    def get_allele(self, pos):
        return self.genotype[pos]

    def set_allele(self, pos, allele):
        self.genotype[pos] = allele
