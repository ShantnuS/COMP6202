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

#Reproduction 
def reproduce_individuals(groups):
    small_groups = groups["small_groups"]
    large_groups = groups["large_groups"]

    # [10, 10, 00, 00]
    for group in small_groups:
        coop_num = group.count("10")
        self_num = group.count("00")
        for _ in range(t):
            coop_sum = coop_num*Gc*Cc 
            self_sum = self_num*Gs*Cs

            ri_coop = resource_received(coop_sum,self_sum,R_small)
            ri_self = resource_received(self_sum,coop_sum,R_small)

            coop_num = replicate(coop_num,ri_coop,Cc,K)
            self_num = replicate(self_num,ri_self,Cs,K)

        group.clear()
        coop_num = int(round(coop_num))
        self_num = int(round(self_num))
        for _ in range(coop_num):
            group.append("10")

        for _ in range(self_num):
            group.append("00")    

    
    for group in large_groups:
        coop_num = group.count("11")
        self_num = group.count("01")
        for _ in range(t):
            coop_sum = coop_num*Gc*Cc 
            self_sum = self_num*Gs*Cs

            ri_coop = resource_received(coop_sum,self_sum,R_large)
            ri_self = resource_received(self_sum,coop_sum,R_large)

            coop_num = replicate(coop_num,ri_coop,Cc,K)
            self_num = replicate(self_num,ri_self,Cs,K)

        group.clear()
        coop_num = int(round(coop_num))
        self_num = int(round(self_num))
        for _ in range(coop_num):
            group.append("11")

        for _ in range(self_num):
            group.append("01") 
     
    groups = {
        "small_groups":small_groups,
        "large_groups":large_groups
    }

    return groups

#Equation 1 
def resource_received(top, bottom, R):
    return (top)/(top+bottom) * R

#Equation 2
def replicate(ni, ri, Ci, K):
    return  ni + (ri/Ci) - (K*ni)

#Dispersal
def disperse_progeny(groups):
    small_groups = groups["small_groups"]
    large_groups = groups["large_groups"]

    small_pool = [j for i in small_groups for j in i]
    large_pool = [j for i in large_groups for j in i]

    migrant_pool = large_pool + small_pool
    return migrant_pool


#Maintaining the global carrying capacity
def resize_pool(migrant_pool):
    total = len(migrant_pool)

    cl_num = int(float(migrant_pool.count("11")/total)*N)
    cs_num = int(float(migrant_pool.count("10")/total)*N)
    sl_num = int(float(migrant_pool.count("01")/total)*N)
    ss_num = int(float(migrant_pool.count("00")/total)*N)

    cl_pool = ["11"]*cl_num
    cs_pool = ["10"]*cs_num
    sl_pool = ["01"]*sl_num
    ss_pool = ["00"]*ss_num

    new_pool = cl_pool + cs_pool + sl_pool + ss_pool
    shuffle(new_pool)
    return new_pool

def run():
    print("Experiment Started!")

    #Initialise migrant pool
    migrant_pool = initialise_pool(N)

    for _ in range(T):
        #Form the groups
        groups = create_groups(migrant_pool)

        #Perform reproduction
        groups = reproduce_individuals(groups)
        
        #disperse progeny into migrant pool
        migrant_pool = disperse_progeny(groups)

        #resize pool to maintain global carrying capacity
        migrant_pool = resize_pool(migrant_pool)
        print(migrant_pool.count("00"))




if __name__ == "__main__":
    import main
    main.main()