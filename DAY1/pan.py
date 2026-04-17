import pandas as pd

# Create sample data
data = {
    "Name": ["Papu", "Rahul", "Anita", "Kiran"],
    "Age": [21, 22, 20, 23],
    "City": ["Bangalore", "Delhi", "Mumbai", "Chennai"],
    "Score": [85, 90, 88, 92]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("students.csv", index=False)

print("CSV file 'students.csv' created successfully!")

import pandas as pd

# Read CSV file
df = pd.read_csv("students.csv")

# Display data
print("Dataset:\n", df)

# Basic info
print("\nInfo:\n")
print(df.info())

# Describe data
print("\nStatistics:\n")
print(df.describe())

#add a new column
df['Passed'] = df['Score'] >= 60
print("\nUpdated Dataset:\n", df)

#write new colunm to csv
df.to_csv("students_updated.csv", index=False)
print("Updated CSV file 'students_updated.csv' created successfully!")

# write a new column to csv in same file
df.to_csv("students.csv", index=False)  
print("CSV file 'students.csv' updated successfully with new column!")
