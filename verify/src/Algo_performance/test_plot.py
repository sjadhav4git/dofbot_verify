import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# Data for the 3D bar plot
x = np.linspace(1, 5, 5)
y = np.linspace(1, 100, 100)
z = np.linspace(1, 50, 50)

# Create a meshgrid for X, Y, and Z
X, Y, Z = np.meshgrid(x, y, z)

# Heights of the bars (you can replace this with your own data)
heights = np.random.rand(5, 100, 50)

# Create a 3D bar plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.bar3d(X.ravel(), Y.ravel(), Z.ravel(), 1, 1, heights.ravel(), shade=True)

# Set labels
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
ax.set_title('3D Bar Plot')

# Show the plot
plt.show()
