#https://towardsdatascience.com/integer-programming-in-python-1cbdfa240df2
from xmlrpc.client import boolean
import cvxpy
import numpy as np

# The data for the Knapsack problem
# weights and utilities are also specified
pesos = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310])
personagens = np.array([1.8, 1.6, 1.6, 1.6, 1.4, 0.9, 0.7])

# The variable we are solving for
selecoes = [cvxpy.Variable(len(personagens), boolean = True) for i in range(len(pesos))]

# Our total utility is the sum of the item utilities
tempo_total = sum([pesos[i] * cvxpy.inv_pos(personagens @ selecoes[i]) for i in range(len(pesos))])
restricaoPersonagens = [sum(selecao[j] for selecao in selecoes) <= 8 for j in range(len(personagens))]
restricaoPersoFases = [sum(selecao) >= 1 for selecao in selecoes]
restricaoParticipacoes = [sum(sum(selecao) for selecao in selecoes) <= 55]
# We tell cvxpy that we want to minimize total utility  
# cvxpy must be passed as a list
knapsack_problem = cvxpy.Problem(cvxpy.Minimize(tempo_total), restricaoParticipacoes+restricaoPersonagens+restricaoPersoFases)

#print(cvxpy.__dir__())
# Solving the problem
knapsack_problem.solve(solver=cvxpy.CPLEX, verbose=True, cplex_params={"threads":5, "parallel":-1, "mip.display":4, "mip.limits.auxrootthreads": 0, "read.scale":-1, "mip.tolerances.absmipgap":0.1, "mip.tolerances.uppercutoff":1830.0,"mip.tolerances.lowercutoff":1800.0, "mip.strategy.startalgorithm":0,"qpmethod":0, "mip.tolerances.mipgap":0.004, "simplex.tolerances.optimality": 0.000000001})#"timelimit": 5})

for selecao in selecoes:
    print(selecao.value)

print("Tempo total: ", tempo_total.value)
