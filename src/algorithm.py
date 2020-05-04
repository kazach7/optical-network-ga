from solution import Solution
import random
import itertools 

class AlgorithmPerformer:
    # Mnozone przez liczbe nadmiarowych lambd i odejmowane od f. przystosowania.
    overfilledFiberPunishmentFactor = 200
    #  Mnozone przez wartosc jakiej zabraklo by spelnic zapotrzebowanie i odejmowane od f. przyst.
    unfulfilledDemandPunishmentFactor = 3
    # Poki co krzyzowanie dwupunktowe.
    crossoverSplitPointsNumber = 2 

    def __init__(self, demands, connections, fiberCapacity):
        self.demands = demands
        self.connections = connections
        self.fiberCapacity = fiberCapacity

    def perform_algorithm(self, populationSize, iterations, mutationProbability):
        population = self.generate_initial_population(populationSize)

        for _ in range(iterations):
            children = self.perform_crossover(population)
            self.perform_mutation(children, mutationProbability)
            population = self.choose_new_population(population, children, populationSize)
        
        return population[0] # byc moze tak, ale nie wiem

    def generate_initial_population(self, populationSize):
        result = []
        for _ in range(len(populationSize)):
            s = Solution(len(self.demands))
            j = 0
            for gene in s.genotype:
                while (gene.calculate_coverage() < self.demands[j].value):
                    gene.get_allele()[random.randint(0,2)] += 1
                j += 1
            result.append(s)

        return result

    def perform_crossover(self, population):
        return self.perform_multipoint_crossover(population, self.crossoverSplitPointsNumber)

    def perform_multipoint_crossover(self, population, pointsNo):
        children = []
        genotype_len = len(self.demands)
        for parents in list(itertools.combinations(population, 2)):
            loci = []
            loci.append(random.randint(0, genotype_len-(pointsNo-1)))
            for i in range(1, pointsNo):
                loci.append(random.randint(loci[i-1] + 1, genotype_len - (pointsNo-i-1)))

            twins = []
            shift = 0
            nextLocusIndex = 0
            allLociPassed = False
            for i in range(genotype_len):
                if (not allLociPassed and i == loci[nextLocusIndex]):
                    shift = (shift+1) % 2
                    nextLocusIndex += 1
                    if (nextLocusIndex == len(loci)): allLociPassed = True
                for j in range(2):
                    twins[j].append(parents[(j + shift) % 2][i])
            for t in twins:
                children.append(t)

        return children

    def perform_mutation(self, children, mutationProbability):
        mutationCount = 0
        rand_max = (int)(1/mutationProbability)
        for child in children:
            for gene in child:
                for allele in gene.get_allele():
                    for i in range(len(allele)):
                        if (random.randint(1, rand_max) < 2):
                            mutationCount += 1
                            allele[i] += random.choice((-1,1))
        print ("Mutated %d times among %d children." % mutationCount, len(children))

    def choose_new_population(self, population, children, populationSize):
        # Calculate fitness values for all solutions from parent population and children
        solutions_with_fitness_values = []
        for solution in (population + children):
            solutions_with_fitness_values.append((solution, self.calculate_fitness_value(solution)))
        # Sort solutions descending by their fitness value
        solutions_with_fitness_values.sort(key=lambda x: x[1], reverse=True)
        # Get the sorted list of solutions from the list of pairs
        unzipped = zip(*solutions_with_fitness_values)
        new_population = list(list(unzipped)[0])
        # Truncate the new population to the populationSize size
        del new_population[populationSize:]
        
        return new_population

    def calculate_fitness_value(self, solution):
        # Fitness value is negative and we want to maximize it.

        # The smaller the cost, the better.
        fitness = (-1)*solution.calculate_cost()

        # For all unfulfilled demands diminish the fitness value much.
        for div in solution.get_coverage_divergencies_in_genes():
            if (div > 0):
                fitness -= div*self.unfulfilledDemandPunishmentFactor
            
        # For every connection where there is more lambdas than the capacity diminish
        # the fitness value much.
        solution.apply_transponders_to_connections()
        for conn in self.connections:
            excess = len(conn.lambdas) - self.fiberCapacity
            if (excess > 0):
                fitness -= excess*self.overfilledFiberPunishmentFactor
            conn.clear_lambdas()
        
        return fitness
        
                        