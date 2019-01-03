from random import shuffle
import csv

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

#Initialise migrant pool
def initialise_pool():
    pool = []
    while len(pool)<N:
        for _ in range(2):
            for i in range(allele_size):
                individual = scramble_individual(("1"*(i+1)).zfill(allele_size)) ##IS scamble necessary?!
                pool.append(individual+"1")
                pool.append(individual+"0")

    shuffle(pool)
    return pool

#Group formation 
def create_groups(migrant_pool):
    large_group = []
    small_group = []
    for individual in migrant_pool:
        if individual.endswith("1"):
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
def resize_pool(migrant_pool):
    

def run():
    print("Extension Started!")

    #Migrant pool
    migrant_pool = initialise_pool()

    for i in range(T):
        #Form Groups
        groups = create_groups(migrant_pool)

        #Perform reproduction
        groups = reproduce_pool(groups)

        #disperse progeny into migrant pool
        migrant_pool = disperse_progeny(groups)
        print(migrant_pool)

        #resize pool to maintain global carrying capacity
        migrant_pool = resize_pool(migrant_pool)


    print("Extension Finished")


if __name__ == "__main__":
    import main
    main.main()