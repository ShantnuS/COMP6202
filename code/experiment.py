import time
from random import shuffle

Gc = 0.018 #growth rate cooperative
Gs = 0.02 #growth rate selfish
Cc = 0.1 #consumption rate cooperative
Cs = 0.2 #consumption rate selfish
N = 4000 #population size 
T = 1000 #number of generations 
K = 0.1 #death rate
R_small = 4 #R for small groups
R_large = 50 #R for large groups
t = 4 #time spent in groups before dispersal 
L_size = 40 #size of the large group
S_size = 4 #size of the small group

# 11 = Cooperative + Large
# 10 = Cooperative + Small
# 01 = Selfish + Large
# 00 = Selfish + Small

#splits a list into chunks!
def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        if len(l[i:i+n]) == n:
            yield l[i:i+n]

#Initialisation
def initialise_pool(N):
    group_size = N/4

    #Create initial groups
    migrant_pool = []
    for _ in range(int(group_size)):
        migrant_pool.append("11") #CL
        migrant_pool.append("10") #CS
        migrant_pool.append("01") #SL
        migrant_pool.append("00") #SS

    shuffle(migrant_pool)
    return migrant_pool

#Create groups
def create_groups(migrant_pool):
    large_group = []
    small_group = []
    for individual in migrant_pool:
        if individual[1] == "1":
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

#Group formation 
#Reproduction 
#Migrant pool formation 
#Maintaining the global carrying capacity
#Iteration 

def resource_received(ni, Gi, Ci, nj, Gj, Cj, R):
    #something
    ri = 0 
    return ri

#Calculate the new population of each type of individual. ni = current population, ri = resouce received, Ci = consumption rate, K = death rate
def replicate(ni, ri, Ci, K):
    return  ni + ri/Ci - K*ni

#Not sure whether to call it replicate or reproduce so will use them interchangeably 
def reproduce(ni, ri, Ci, K):
    return replicate(ni, ri, Ci, K)

def run():
    print("Experiment Started!")

    #Initialise migrant pool
    migrant_pool = initialise_pool(N)
    # for i in migrant_pool:
    #     print(i)

    #Form the groups
    groups = create_groups(migrant_pool)
    print(groups["large_groups"])


if __name__ == "__main__":
    import main
    main.main()