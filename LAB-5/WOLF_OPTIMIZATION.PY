# Input: 
#     Generator cost coefficients, power limits, demand PD
#     Population size N, max iterations MaxIter

# Initialize:
#     Create N wolves with random power outputs within limits
#     Evaluate fitness = total cost + penalty if sum(power) ≠ PD        
#     Identify alpha, beta, delta wolves (best 3 solutions)
                                                                                                                                                                                                                                                                                                             
# For iter = 1 to MaxIter:
#     a = 2 - iter * (2 / MaxIter)
    
#     For each wolf i:
#         For each generator j:
#             Compute A1, C1, A2, C2, A3, C3 with random numbers
#             X1 = alpha[j] - A1 * |C1*alpha[j] - wolf[i][j]|
#             X2 = beta[j]  - A2 * |C2*beta[j]  - wolf[i][j]|
#             X3 = delta[j] - A3 * |C3*delta[j] - wolf[i][j]|
#             wolf[i][j] = (X1 + X2 + X3) / 3
#             Clip wolf[i][j] within limits
        
#         Update fitness of wolf[i]
    
#     Update alpha, beta, delta wolves based on fitness

# Return alpha power outputs and cost




import random
import math

# Generator cost coefficients and limits
a = [500, 400, 200]
b = [5.3, 5.5, 5.8]
c = [0.004, 0.006, 0.009]
P_min = [150, 100, 50]
P_max = [600, 400, 200]

demand = 850

def cost_function(P):
    total_power = sum(P)
    penalty = 1000 * abs(total_power - demand)  # penalty if demand not met
    cost = 0
    for i in range(len(P)):
        cost += a[i] + b[i]*P[i] + c[i]*(P[i]**2)
    return cost + penalty

class GWO:
    def __init__(self, obj_func, dim, lb, ub, population=20, iterations=100):
        self.obj_func = obj_func
        self.dim = dim
        self.lb = lb
        self.ub = ub
        self.population = population
        self.iterations = iterations
        
        # Initialize positions randomly within bounds
        self.positions = []
        for _ in range(self.population):
            wolf = [random.uniform(self.lb[i], self.ub[i]) for i in range(self.dim)]
            self.positions.append(wolf)
        
        self.alpha_pos = [0.0]*self.dim
        self.alpha_score = float('inf')
        self.beta_pos = [0.0]*self.dim
        self.beta_score = float('inf')
        self.delta_pos = [0.0]*self.dim
        self.delta_score = float('inf')
        
    def optimize(self):
        for iter in range(self.iterations):
            for i in range(self.population):
                # Bound check
                for d in range(self.dim):
                    if self.positions[i][d] < self.lb[d]:
                        self.positions[i][d] = self.lb[d]
                    if self.positions[i][d] > self.ub[d]:
                        self.positions[i][d] = self.ub[d]

                fitness = self.obj_func(self.positions[i])

                # Update alpha, beta, delta
                if fitness < self.alpha_score:
                    self.alpha_score = fitness
                    self.alpha_pos = self.positions[i][:]
                elif fitness < self.beta_score:
                    self.beta_score = fitness
                    self.beta_pos = self.positions[i][:]
                elif fitness < self.delta_score:
                    self.delta_score = fitness
                    self.delta_pos = self.positions[i][:]
            
            a_val = 2 - iter * (2 / self.iterations)  # linearly decreases from 2 to 0
            
            for i in range(self.population):
                new_pos = []
                for d in range(self.dim):
                    r1 = random.random()
                    r2 = random.random()
                    A1 = 2 * a_val * r1 - a_val
                    C1 = 2 * r2
                    D_alpha = abs(C1 * self.alpha_pos[d] - self.positions[i][d])
                    X1 = self.alpha_pos[d] - A1 * D_alpha
                    
                    r1 = random.random()
                    r2 = random.random()
                    A2 = 2 * a_val * r1 - a_val
                    C2 = 2 * r2
                    D_beta = abs(C2 * self.beta_pos[d] - self.positions[i][d])
                    X2 = self.beta_pos[d] - A2 * D_beta
                    
                    r1 = random.random()
                    r2 = random.random()
                    A3 = 2 * a_val * r1 - a_val
                    C3 = 2 * r2
                    D_delta = abs(C3 * self.delta_pos[d] - self.positions[i][d])
                    X3 = self.delta_pos[d] - A3 * D_delta
                    
                    new_val = (X1 + X2 + X3) / 3
                    # Clip to bounds
                    if new_val < self.lb[d]:
                        new_val = self.lb[d]
                    if new_val > self.ub[d]:
                        new_val = self.ub[d]
                    new_pos.append(new_val)
                self.positions[i] = new_pos
                
        return self.alpha_pos, self.alpha_score

# Bounds for generators
lb = P_min
ub = P_max

# Run GWO optimizer
gwo = GWO(cost_function, dim=3, lb=lb, ub=ub, population=30, iterations=200)
best_power, best_cost = gwo.optimize()

print("Optimal Power Generation (MW):", [round(p, 2) for p in best_power])
print("Total Fuel Cost ($):", round(best_cost, 2))
print("Total Power Generated:", round(sum(best_power), 2))






