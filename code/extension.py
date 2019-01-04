from random import shuffle
import csv

Gmax = 0.02 #max G ( a 00000000 individual)
Gbase = 0.019 #base G  (a 11111111 individual)
Cmax = 0.2 #max C ( a 00000000 individual)
Cbase = 0.15 #base C ( a 11111111 individual)
N = 4000 #population size 
T = 200 #number of generations 
K = 0.1 #death rate
R_small = 4 #R for small groups
R_large = 50 #R for large groups
t = 4 #time spent in groups before dispersal 
L_size = 40 #size of the large group
S_size = 4 #size of the small group
allele_size = 8 #bitstring size not including Size parameter 

#splits a list into chunks!
def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        if len(l[i:i+n]) == n:
            yield l[i:i+n]

def scramble_individual(individual):
    individual = list(individual)
    shuffle(individual)
    return ''.join(individual)

def sort_individual(individual):
    genotype = list(individual[:allele_size])
    genotype.sort()
    return ''.join(genotype)+individual[-1:]

def get_genotypes():
    genotypes = []
    for i in range(allele_size+1):
            individual = ("1"*(i)).zfill(allele_size)
            genotypes.append(individual+"L")
            genotypes.append(individual+"S")
    return genotypes

#Initialise migrant pool
def initialise_pool():
    pool = []
    while len(pool)<N:
        for i in range(allele_size+1):
            individual = ("1"*(i)).zfill(allele_size)
            pool.append(individual+"L")
            pool.append(individual+"S")

    shuffle(pool)
    return pool

#Group formation 
def create_groups(migrant_pool):
    large_group = []
    small_group = []
    for individual in migrant_pool:
        if individual.endswith("L"):
            large_group.append(individual)
        else:
            small_group.append(individual)
    
    #create subgroups from the larger pool
    small_groups = list(chunks(small_group, S_size))
    large_groups = list(chunks(large_group, L_size))

    groups = {
        "small_groups":small_groups,
        "large_groups":large_groups
    }
    
    return groups

def calculate_G(individual):
    steps = float((Gmax-Gbase)/allele_size)
    return Gbase+(list(individual[:allele_size]).count("0"))*steps

def calculate_C(individual):
    steps = float((Cmax-Cbase)/allele_size)
    return Cbase+(list(individual[:allele_size]).count("0"))*steps

def calculate_bottom(group):
    result = 0
    for i in group:
        result += calculate_G(i)*calculate_C(i)
    return result

def resource_received(top, bottom, R):
    return (top/bottom * R)

def repicate(ni, ri, Ci, K):
    return ni + (ri/Ci) - (K*ni)

#reproduce the group and return new group
def reproduce_group(group, R):
    reproduced_genotype = []
    for _ in range(t):
        bottom = calculate_bottom(group)
        reproduced_genotype.clear()
        result_group = []
        for individual in group:
            individual = sort_individual(individual)
            if individual not in reproduced_genotype:
                reproduced_genotype.append(individual)
                individual_num = group.count(individual)
                individual_G = calculate_G(individual)
                individual_C = calculate_C(individual)
                ri = resource_received(individual_num*individual_C*individual_G, bottom, R)
                new_num = repicate(individual_num, ri, individual_C, K)
                for _ in range(int(round(new_num))):
                    result_group.append(individual)
        group = result_group       
    return group

#Perform Reproduction
def reproduce_pool(groups):
    small_groups = groups["small_groups"]
    large_groups = groups["large_groups"]

    output_small = []
    output_large = []

    for group in small_groups:
        output_small.append(reproduce_group(group, R_small))

    for group in large_groups:
        output_large.append(reproduce_group(group, R_large))

    groups = {
        "small_groups":output_small,
        "large_groups":output_large
    }

    return groups

#Disperse Progeny
def disperse_progeny(groups):
    small_groups = groups["small_groups"]
    large_groups = groups["large_groups"]

    small_pool = [j for i in small_groups for j in i]
    large_pool = [j for i in large_groups for j in i]

    migrant_pool = large_pool + small_pool
    return migrant_pool

#Resize Pool
def resize_pool(migrant_pool, genotypes):
    total = len(migrant_pool)
    output_pool = []
    for genotype in genotypes:
        genotype_num = migrant_pool.count(genotype)
        genotype_prop = float(genotype_num/total)
        to_add = int(N*genotype_prop)
        for _ in range(to_add):
            output_pool.append(genotype)
    shuffle(output_pool)
    return output_pool

def initialise_output(output_file, genotypes, migrant_pool):
    with open(output_file, "w", newline='') as file:
        myFields = genotypes
        writer = csv.DictWriter(file, fieldnames=myFields)   
        writer.writeheader()
        row = {}
        for i in genotypes:
            row[i] = migrant_pool.count(i)
        writer.writerow(row)

def process_pool(output_file, migrant_pool, genotypes):
        with open(output_file, "a", newline='') as file:
            myFields = genotypes
            writer = csv.DictWriter(file, fieldnames=myFields)
            row = {}
            for i in genotypes:
                row[i] = migrant_pool.count(i)
            writer.writerow(row)   

def run():
    print("Extension Started!")

    output_file = "output2.csv"
    genotypes = get_genotypes()

    #Migrant pool
    migrant_pool = initialise_pool()
    initialise_output(output_file,genotypes,migrant_pool)

    for i in range(T):
        print(i)
        print(len(migrant_pool))
        #Form Groups
        groups = create_groups(migrant_pool)

        #Perform reproduction
        groups = reproduce_pool(groups)

        #disperse progeny into migrant pool
        migrant_pool = disperse_progeny(groups)

        #resize pool to maintain global carrying capacity
        migrant_pool = resize_pool(migrant_pool, genotypes)

        process_pool(output_file,migrant_pool,genotypes)
        
    print("Extension Finished")


if __name__ == "__main__":
    import main
    main.main()