import matplotlib.pyplot as plt
import numpy as np

# Sample data
x = np.linspace(0, 10, 100)
y = np.sin(x)
categories = ['A', 'B', 'C', 'D']
values = [10, 20, 15, 25]
data = np.random.randn(1000)
x_scatter = np.random.randn(100)
y_scatter = np.random.randn(100)
sizes = np.random.randint(10, 100, 100)
pie_labels = ['Apple', 'Banana', 'Cherry', 'Date']
pie_sizes = [30, 25, 20, 25]
box_data = [np.random.normal(0, std, 100) for std in range(1, 4)]

# 1. Line Plot
plt.figure(figsize=(10, 8))

plt.subplot(2, 3, 1)
plt.plot(x, y)
plt.title('Line Plot')
plt.xlabel('X')
plt.ylabel('Y')

# 2. Bar Chart
plt.subplot(2, 3, 2)
plt.bar(categories, values)
plt.title('Bar Chart')
plt.xlabel('Categories')
plt.ylabel('Values')

# 3. Histogram
plt.subplot(2, 3, 3)
plt.hist(data, bins=30)
plt.title('Histogram')
plt.xlabel('Value')
plt.ylabel('Frequency')

# 4. Scatter Plot
plt.subplot(2, 3, 4)
plt.scatter(x_scatter, y_scatter, s=sizes, alpha=0.5)
plt.title('Scatter Plot')
plt.xlabel('X')
plt.ylabel('Y')

# 5. Pie Chart
plt.subplot(2, 3, 5)
plt.pie(pie_sizes, labels=pie_labels, autopct='%1.1f%%')
plt.title('Pie Chart')

# 6. Box Plot
plt.subplot(2, 3, 6)
plt.boxplot(box_data)
plt.title('Box Plot')
plt.xlabel('Groups')
plt.ylabel('Values')

plt.tight_layout()
plt.show()