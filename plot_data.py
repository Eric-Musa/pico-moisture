import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('moisture_data.csv')

x = df['depth']
y = df['mean_moisture']
e = df['std_moisture']

plt.errorbar(x, y, e, linestyle='None', marker='^')
plt.title('Moisture (frac) vs. Depth (relative)')
plt.xlabel('relative depth')
plt.ylabel('moisture %')
# plt.show()


import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Define the tanh function to fit
def tanh(x, a, b, c, d):
    return a * np.tanh(b * (x - c)) + d

# Your data goes here
xdata = np.array(...)  # Replace with your actual x data
ydata = np.array(...)  # Replace with your actual y data

# Initial guess for the parameters
initial_guess = [1, 1, 0, 0]

# Use curve_fit to fit the tanh function to the data
popt, pcov = curve_fit(tanh, xdata, ydata, p0=initial_guess)

# popt contains the best fit parameters
a_fit, b_fit, c_fit, d_fit = popt

# Plotting the original data
plt.scatter(xdata, ydata, label='Data')

# Plotting the fitted curve
x_fit = np.linspace(min(xdata), max(xdata), 200)
y_fit = tanh(x_fit, *popt)
plt.plot(x_fit, y_fit, 'r-', label='Fitted tanh function')

# Adding the main title and axis titles
plt.title("Moisture (frac) vs. Depth (relative)")
plt.xlabel("relative depth")
plt.ylabel("moisture %")

# Show the legend
plt.legend()

# Display the plot
plt.show()