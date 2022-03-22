from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


# Example from
# https://www.geeksforgeeks.org/python-gaussian-fit/



uwb_xdata = [0.092, 0.042, 0.068, 0.128, 0.068, 0.018, 0.018, 0.038, 0.012, 0.002, 0.038, 0.022, 0.008, 0.008, 0.088, 0.098, 0.042, 0.138, 0.128, 0.088, 0.058, 0.048, 0.032, 0.142, 0.098, 0.212, 0.138, 0.138, 0.022, 0.078, 0.022, 0.042, 0.038, 0.332, 0.008, 0.252, 0.008]   
uwb_ydata = [0.289, 0.151, 0.001, 0.071, 0.319, 0.481, 0.299, 0.289, 0.009, 0.259, 0.401, 0.109, 0.259, 0.851, 0.239, 0.161, 0.309, 0.091, 0.179, 0.231, 0.039, 0.141, 0.019, 0.311, 0.379, 0.041, 0.399, 0.399, 0.029, 0.331, 0.099, 0.361, 0.259, 0.211, 0.239, 0.101, 0.319]

# Recast xdata and ydata into numpy arrays so we can use their handy features
xdata = np.asarray(uwb_xdata)
ydata = np.asarray(uwb_ydata)
plt.plot(xdata, ydata, 'o')

# Define the Gaussian function


def gauss(x, A, B):
    y = A*np.exp(-1*B*x**2)
    return y


parameters, covariance = curve_fit(gauss, xdata, ydata)

fit_A = parameters[0]
fit_B = parameters[1]

fit_y = gauss(xdata, fit_A, fit_B)
plt.plot(xdata, ydata, 'o', label='data')
plt.plot(xdata, fit_y, '-', label='fit')
plt.legend()



