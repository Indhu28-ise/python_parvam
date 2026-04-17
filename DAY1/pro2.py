import numpy as np

# Create arrays
arr1 = np.array([1, 2, 3, 4, 5])
arr2 = np.array([10, 20, 30, 40, 50])

# Addition
add = arr1 + arr2
print("Addition:", add)

# Multiplication
mul = arr1 * arr2
print("Multiplication:", mul)

# Mean value
mean_val = np.mean(arr1)
print("Mean of arr1:", mean_val)

# 2D Array (Matrix)
matrix = np.array([[1, 2], [3, 4]])

# Matrix Transpose
transpose = matrix.T
print("Transpose:\n", transpose)

# Matrix Multiplication
result = np.dot(matrix, transpose)
print("Matrix Multiplication:\n", result)