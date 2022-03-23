from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


# Example from
# https://www.geeksforgeeks.org/python-gaussian-fit/
uwb_xdata = list()
uwb_ydata = list()
with open("Errors/UWB Error-Table 1.csv") as file:
    for line in file:
        a,b = line.split(",")
        uwb_xdata.append(float(a))
        uwb_ydata.append(float(b))




odom_xdata = list()
odom_ydata = list()
with open("Errors/ODOM Error-Table 1.csv") as file:
    for line in file:
        a,b = line.split(",")
        odom_xdata.append(float(a))
        odom_ydata.append(float(b))





# Recast xdata and ydata into numpy arrays so we can use their handy features
xdata = np.asarray(uwb_xdata)
ydata = np.asarray(uwb_ydata)
plt.plot(xdata, ydata, 'o')

# Define the Gaussian function


def gauss(x, A, B):
    y = A*np.exp(-1*B*x**2)
    return y


parameters, covariance = curve_fit(f=gauss, xdata=xdata, ydata=ydata)

fit_A = parameters[0]
fit_B = parameters[1]


fit_y = gauss(xdata, fit_A, fit_B)
plt.plot(xdata, ydata, 'o', label='data')
plt.plot(xdata, fit_y, '-', label='fit')
plt.legend()
plt.show()



