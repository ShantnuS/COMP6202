Gmax = 0.02 #max G ( a 00000000 individual)
Gbase = 0.018 #base G  (a 11111111 individual)
Cmax = 0.2 #max C ( a 00000000 individual)
Cbase = 0.1 #base C ( a 11111111 individual)
N = 4000 #population size 
T = 150 #number of generations 
K = 0.1 #death rate
R_small = 4 #R for small groups
R_large = 50 #R for large groups
t = 4 #time spent in groups before dispersal 
L_size = 40 #size of the large group
S_size = 4 #size of the small group
allele_size = 8 #bitstring size not including Size parameter 


def sort_individual(individual):
    genotype = list(individual[:allele_size])
    genotype.sort()
    return ''.join(genotype)+individual[-1:]

def calculate_G(individual):
    steps = float((Gmax-Gbase)/allele_size)
    return Gbase+(list(individual[:allele_size]).count("0"))*steps

def calculate_C(individual):
    steps = float((Cmax-Cbase)/allele_size)
    return Cbase+(list(individual[:allele_size]).count("0"))*steps

def get_genotypes():
    genotypes = []
    for i in range(allele_size+1):
            individual = ("1"*(i)).zfill(allele_size)
            genotypes.append(individual+"L")
            genotypes.append(individual+"S")
    return genotypes

def get_genotypes2():
    genotypes = []
    individual = ("1"*(allele_size+1)).zfill(allele_size)
    individual2 = ("1"*(0)).zfill(allele_size)
    genotypes.append(individual2+"L")
    genotypes.append(individual2+"S")
    genotypes.append(individual+"L")
    genotypes.append(individual+"S")
    return genotypes

def resource_received(top, bottom, R):
    return (top/bottom) * R

# for i in get_genotypes():
#     print(i + " | " + "C: " + str(calculate_C(i)) + " | " + "G: " + str(calculate_G(i)))

print(resource_received(2,2,4))