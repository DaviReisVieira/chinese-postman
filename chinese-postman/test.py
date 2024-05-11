import eulerian
from ChinesePostman import EulerianPathSolver

# edges = [(0, 1, 70), (0, 5, 70), (1, 5, 50), (1, 2, 50), (1, 4, 50), (2, 4, 50),
#          (2, 3, 50), (3, 4, 70), (4, 5, 60), (3, 6, 70), (3, 7, 120), (6, 7, 70), (5, 7, 60)]
# result = 1000
# n = 8

edges = [(0, 1, 3), (0, 2, 1), (0, 4, 5), (2, 4, 2),
         (4, 5, 4), (1, 5, 6), (1, 3, 1), (5, 3, 1)]

# # [0, 3, 1, 0, 5, 0]
# # [3, 0, 0, 1, 0, 6]
# # [1, 0, 0, 0, 2, 0]
# # [0, 1, 0, 0, 0, 1]
# # [5, 0, 2, 0, 0, 4]
# # [0, 6, 0, 1, 4, 0]

result = 28
n = 6

classe = EulerianPathSolver(edges, n)
r = classe.solving()
is_eulerian_path = eulerian.is_eulerian_path(edges, r[1])

print(f"Result: {r[0]}| Expected: {result}")
print(f"Is eulerian path: {is_eulerian_path}")
print(f"Edges: {r[1]}")
