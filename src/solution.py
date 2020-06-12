"""
Classes providing abstraction for a solution to the problem.
"""
import copy

# Represents a single solution of the optimized problem.
class Solution:
    transponderCosts = [1, 5, 15]
    transpondersCapacities = [10, 40, 100]

    def __init__(self, demands_amount, routes_amount = 7):
        self.genotype = []
        self.fitness = 0
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

    def present(self, network, fiber_capacity):
        demands = network.demands
        links = network.links
        assert(len(self.genotype) == len(demands))
        sum_cost = 0
        unfulfilled_count = 0
        unfulfilled_total_value = 0

        for gen, i in zip(self.genotype, range(len(self.genotype))):
            print("{}: {}".format(demands[i].id, demands[i].value))

            for allele in gen.alleles:
                print("{}".format(allele))
            cost = gen.calculate_cost()
            sum_cost += cost
            print("Cost: {}".format(cost))
            
            divergence = demands[i].value - gen.calculate_coverage()
            if (divergence > 0):
                unfulfilled_total_value += divergence
                unfulfilled_count += 1
            print("Divergence: {}".format(divergence))
            print()

        network.apply_solution_to_network(self)
        total_excess = 0
        print("Links above capacity:")
        for link in links:
            excess = len(link.lambdas) - fiber_capacity
            if (excess > 0):
                print("{}, {} above cap".format(link.id, excess))
                total_excess += excess
        network.clear_network()
        print ("In total: {} above cap".format(total_excess))

        print("\nFitness value: {}".format(self.fitness))
        print("Total solution cost: {}".format(sum_cost))
        print("Unfulfilled demands: {} (total value: {})".format(unfulfilled_count, unfulfilled_total_value))
                

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

    def deepcopy(self):
        new_gene = Gene(0)
        new_gene.alleles = copy.deepcopy(self.alleles)
        return new_gene
