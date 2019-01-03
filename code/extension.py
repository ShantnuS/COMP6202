from random import shuffle
import csv

Gbase = 0.018 #base G for a 11111111 individual
Cbase = 0.1 #base C for a 11111111 individual
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
                individual = scramble_individual(("1"*(i+1)).zfill(allele_size))
                pool.append(individual+"1")
                pool.append(individual+"0")

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

def reproduce_individuals(groups):
    return 0

#Perform Reproduction
#Disperse Progeny
#Resize Pool

def run():
    print("Extension Started!")

    #Migrant pool
    migrant_pool = initialise_pool()

    #Form Groups
    groups = create_groups(migrant_pool)
    print(groups["small_groups"][0])


    print("Extension Finished")


if __name__ == "__main__":
    import main
    main.main()