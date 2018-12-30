import time

Gc = 0.018 #growth rate cooperative
Gs = 0.02 #growth rate selfish
Cc = 0.1 #consumption rate cooperative
Cs = 0.2 #consumption rate selfish
N = 4000 #population size 
T = 1000 #number of generations 
K = 0.1 #death rate
R_small = 4 #R for small groups
R_large = 50 #R for large groups

#Initialisation
#Group formation 
#Reproduction 
#Migrant pool formation 
#Maintaining the global carrying capacity
#Iteration 

def resource_received(ni, Gi, Ci, nj, Gj, Cj, R):
    #something
    ri = 0 
    return ri

def reproduce(ni, ri, Ci, K):
    return  ni + ri/Ci - K*ni

def run():
    print("Experiment Started!")
    pop = 50
    for _ in range(T):
        pop = reproduce(pop, 0.4, Cc, K)
        print(str(pop))


if __name__ == "__main__":
    import main
    main.main()