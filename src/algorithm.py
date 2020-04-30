from solution import Solution
import random
import itertools 

class AlgorithmPerformer:
    def __init__(self, demands, connections):
        self.demands = demands
        self.connectins = connections

    def perform_algorithm(self, populationSize, iterations, mutationProbability):
        self.mutationProbability = mutationProbability

        population = self.generate_initial_population(populationSize)

        for _ in range(iterations):
            children = self.perform_crossover(population)
            self.perform_mutation(children)
            population = self.choose_new_population(population, children)
        
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
        # Poki co krzyzowanie dwupunktowe.
        return self.perform_multipoint_crossover(population, 2)

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

    def perform_mutation(self, children):
        mutationCount = 0
        rand_max = (int)(1/self.mutationProbability)
        for child in children:
            for gene in child:
                for allele in gene.get_allele():
                    for i in range(len(allele)):
                        if (random.randint(1, rand_max) < 2):
                            mutationCount += 1
                            allele[i] += random.choice((-1,1))
        print ("Mutated %d times among %d children." % mutationCount, len(children))

    def choose_new_population(self, population, children):
        pass

                        