import numpy as np

# ── 1. Creating Arrays ──────────────────────────────────────────────────────
a = np.array([1, 2, 3, 4, 5])                  # 1D array
b = np.array([[1, 2, 3], [4, 5, 6]])            # 2D array
zeros = np.zeros((3, 3))                         # 3x3 array of zeros
ones = np.ones((2, 4))                           # 2x4 array of ones
rng = np.arange(0, 20, 2)                        # [0, 2, 4, ..., 18]
linspace = np.linspace(0, 1, 5)                  # 5 evenly spaced values

print("1D array:", a)
print("2D array:\n", b)
print("Zeros:\n", zeros)
print("Range:", rng)
print("Linspace:", linspace)

# ── 2. Array Properties ─────────────────────────────────────────────────────
print("\n--- Array Properties ---")
print("Shape:", b.shape)          # (2, 3)
print("Dimensions:", b.ndim)      # 2
print("Size:", b.size)            # 6
print("Data type:", b.dtype)      # int64

# ── 3. Reshaping & Transposing ──────────────────────────────────────────────
print("\n--- Reshaping ---")
c = np.arange(1, 13)               # [1, 2, ..., 12]
reshaped = c.reshape(3, 4)         # 3 rows, 4 cols
transposed = reshaped.T            # Transpose (4 rows, 3 cols)
flattened = reshaped.flatten()     # Back to 1D

print("Original:", c)
print("Reshaped (3x4):\n", reshaped)
print("Transposed (4x3):\n", transposed)
print("Flattened:", flattened)

# ── 4. Indexing & Slicing ───────────────────────────────────────────────────
print("\n--- Indexing & Slicing ---")
arr = np.array([[10, 20, 30],
                [40, 50, 60],
                [70, 80, 90]])

print("Element [1,2]:", arr[1, 2])          # 60
print("First row:", arr[0, :])              # [10 20 30]
print("Last column:", arr[:, -1])           # [30 60 90]
print("Sub-matrix:\n", arr[0:2, 1:3])      # [[20 30], [50 60]]

# ── 5. Boolean Masking ──────────────────────────────────────────────────────
print("\n--- Boolean Masking ---")
mask = arr > 40
print("Mask:\n", mask)
print("Values > 40:", arr[mask])            # [50 60 70 80 90]

arr[arr < 30] = 0                           # Set values < 30 to 0
print("After zeroing values < 30:\n", arr)

# ── 6. Math Operations ──────────────────────────────────────────────────────
print("\n--- Math Operations ---")
x = np.array([1, 2, 3, 4])
y = np.array([10, 20, 30, 40])

print("Addition:", x + y)                   # Element-wise add
print("Multiplication:", x * y)             # Element-wise multiply
print("Square root:", np.sqrt(x))           # [1.  1.41  1.73  2.]
print("Power:", np.power(x, 3))             # [1  8  27  64]
print("Sum:", np.sum(y))                    # 100
print("Mean:", np.mean(y))                  # 25.0
print("Max:", np.max(y), "| Min:", np.min(y))

# ── 7. Stacking & Splitting ─────────────────────────────────────────────────
print("\n--- Stacking & Splitting ---")
p = np.array([1, 2, 3])
q = np.array([4, 5, 6])

h_stack = np.hstack([p, q])                # Horizontal: [1 2 3 4 5 6]
v_stack = np.vstack([p, q])                # Vertical:  [[1 2 3], [4 5 6]]
print("HStack:", h_stack)
print("VStack:\n", v_stack)

splits = np.split(h_stack, 3)              # Split into 3 equal parts
print("Split:", splits)

# ── 8. Copying ──────────────────────────────────────────────────────────────
print("\n--- Copy vs View ---")
original = np.array([1, 2, 3, 4, 5])
view = original[:]          # View — shares memory
copy = original.copy()      # Deep copy — independent

view[0] = 99
copy[4] = 99

print("Original (affected by view):", original)   # [99  2  3  4  5]
print("Copy (independent):", copy)                # [ 1  2  3  4 99]