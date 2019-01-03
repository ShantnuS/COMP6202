allele_size = 8

def sort_individual(individual):
    genotype = list(individual[:allele_size])
    genotype.sort()
    return ''.join(genotype)+individual[-1:]

print(sort_individual("111010010"))