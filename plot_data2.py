import matplotlib.pyplot as plt
import pandas as pd
import re
import numpy as np
from scipy.stats import norm

with open('data/wet_with_drying.data', 'r') as f:
    lines = f.readlines()

data = {
    'timestamp': [],
    'mean': [],
    'var': [],
    'rvar': [],
    'std': [],
    'rstd': [],
    # 'min': [],
    # 'max': [],
}

def extract_numbers_from_line(line):
    '''
    a la ChatGPT
    '''
    # Regular expression to match both integers and floating point numbers
    pattern = r'-?\d+\.?\d*'
    return re.findall(pattern, line)

# Example usage
# line = "60 (19331.89, 100.5766, 18836, 19956)"
# numbers = extract_numbers_from_line(line)
# print(numbers)  # This will print: ['60', '19331.89', '100.5766', '18836', '19956']


def prob_difference_normals(Xmu, Xvar, Ymu, Yvar):
    '''
    probability that N(X) > N(Y) == N(X) - N(Y) > 0
    where N(X) is assumed to be the more recent value.
    Therefore, this is the probability that, reading by reading, 
    the ADC value from the moisture sensor is increasing and the 
    moisture is decreasing.
    '''
    Zmu = Xmu - Ymu
    Zvar = Xvar + Yvar
    # return np.random.normal(Zmu, Zvar)
    return 1 - norm(loc=Zmu, scale=Zvar).cdf(0)

    
def compare_two_rows(row1, row2):
    return prob_difference_normals(row1['mean'], row1['var'], row2['mean'], row2['var'])


var_cutoff_z = 2

for i, line in enumerate(lines):
    # try:
    timestamp, mean, std, minval, maxval = extract_numbers_from_line(line)
    if minval == 0 and maxval == 65335:
        print(f'Index {i}: minval == 0 and maxval == 65335, likely sensor disconnected')
        continue

    # except ValueError:
    #     print(i)
    timestamp = int(timestamp)
    mean, std = float(mean), float(std)
    rstd = std / mean
    var = std ** 2
    rvar = var / (mean ** 2)

    var_mean = np.array(data['var']).mean()
    var_std = np.array(data['var']).std()
    var_z = ((var - var_mean) / var_std)
    if var_z > var_cutoff_z:
        print(f'Index {i}: var == {var} which is {var_z} z_score, greater than {var_cutoff_z}, too much sensor noise.')
        continue 

    data['timestamp'].append(timestamp)
    data['mean'].append(mean)
    data['var'].append(var)
    data['rvar'].append(rvar)
    data['std'].append(std)
    data['rstd'].append(rstd)
    # data['timestamp'] = timestamp
    # data['timestamp'] = timestamp
    # timestamp, stats = line.split(' ', 1)
    # timestamp = int(timestamp)
    # mean, std, _, __ = stats.replace('(', '').replace(')', '')
    

df = pd.DataFrame(data=data)


def calculate_prob_row_diffs(row, window, data):
    # Get the index of the current row
    idx = row.name

    # Calculate the start and end indices for the window
    start_idx = idx - window
    if start_idx < 0: return np.nan

    return compare_two_rows(data.iloc[idx], data.iloc[start_idx])


# Apply the custom function for each moving average
# df['1_row_diff_prob'] = df.apply(lambda row: calculate_prob_row_diffs(row, 1, df), axis=1)
# df['5_row_diff_prob'] = df.apply(lambda row: calculate_prob_row_diffs(row, 5, df), axis=1)
df['10_row_diff_prob'] = df.apply(lambda row: calculate_prob_row_diffs(row, 10, df), axis=1)
# df['25_row_diff_prob'] = df.apply(lambda row: calculate_prob_row_diffs(row, 25, df), axis=1)
df['100_row_diff_prob'] = df.apply(lambda row: calculate_prob_row_diffs(row, 25, df), axis=1)
# df['250_row_diff_prob'] = df.apply(lambda row: calculate_prob_row_diffs(row, 25, df), axis=1)
df['500_row_diff_prob'] = df.apply(lambda row: calculate_prob_row_diffs(row, 500, df), axis=1)

# print(df)
print(f'{0} to {len(df)}: {compare_two_rows(df.iloc[-1], df.iloc[0])}')
# df = pd.read_csv('moisture_data.csv')

x = df['timestamp']
y = df['mean']
e = df['std']

plt.errorbar(x, y, e, linestyle='None')  # , marker='^')
# plt.title('Moisture (frac) vs. Depth (relative)')
plt.title('ADC vs. time')
plt.xlabel('time')
plt.ylabel('ADC')
plt.scatter(x, y, c='r', zorder=10)
plt.show()


# import numpy as np
# from scipy.optimize import curve_fit
# import matplotlib.pyplot as plt

# # Define the tanh function to fit
# def tanh(x, a, b, c, d):
#     return a * np.tanh(b * (x - c)) + d

# # Your data goes here
# xdata = np.array(...)  # Replace with your actual x data
# ydata = np.array(...)  # Replace with your actual y data

# # Initial guess for the parameters
# initial_guess = [1, 1, 0, 0]

# # Use curve_fit to fit the tanh function to the data
# popt, pcov = curve_fit(tanh, xdata, ydata, p0=initial_guess)

# # popt contains the best fit parameters
# a_fit, b_fit, c_fit, d_fit = popt

# # Plotting the original data
# plt.scatter(xdata, ydata, label='Data')

# # Plotting the fitted curve
# x_fit = np.linspace(min(xdata), max(xdata), 200)
# y_fit = tanh(x_fit, *popt)
# plt.plot(x_fit, y_fit, 'r-', label='Fitted tanh function')

# # Adding the main title and axis titles
# plt.title("Moisture (frac) vs. Depth (relative)")
# plt.xlabel("relative depth")
# plt.ylabel("moisture %")

# # Show the legend
# plt.legend()

# # Display the plot
# plt.show()