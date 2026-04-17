#pandas series 1D array
import pandas as pd
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'London', 'Tokyo']
}   
df = pd.DataFrame(data)
print(df)
print("\nMean age:", df['Age'].mean())
print("\nFiltered data (age > 25):")
print(df[df['Age'] > 25])

# data frame 2D array
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'London', 'Tokyo']
}
df = pd.DataFrame(data)
print(df)
