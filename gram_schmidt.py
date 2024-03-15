from sage.all import *

# Define the vectors
v1 = vector([4, 1, 3, -1])
v2 = vector([2, 1, -3, 4])
v3 = vector([1, 0, -2, 7])
v4 = vector([6, 2, 9, -5])

# Create a matrix from the vectors
A = matrix([v1, v2, v3, v4])

# Compute the Gram-Schmidt orthogonalization
Q, R = A.gram_schmidt()

# Print the orthogonalized vectors
print(round(float(Q.T.column(3)[1]), 5))
