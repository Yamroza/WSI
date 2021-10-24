import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import random
import timeit


# Booth function:
def f(x, y):
    return ((x + 2*y - 7)**2 + (2*x + y - 5)**2)

def x_dev(x, y):
    return 10*x + 8*y - 34

def y_dev(x, y):
     return 8*x + 10*y - 38

def gradient(x, y):
    return [x_dev(x, y), y_dev(x, y)]


# Calculated values:
X_X_DEV = 10
Y_Y_DEV = 10
X_Y_DEV = Y_X_DEV = 8
HESS = [[10, 8], [8, 10]]
HESS_1 = [[5/18, -4/18], [-4/18, 5/18]]
BETA_GRAD = 0.05
BETA_HES = 1
EPSILON = 10**(-12)
ITERS = 50
X = random.randint(-5, 5)
Y = random.randint(-5, 5)


# Steepest gradient descent method:
def grad_func(x, y, beta_grad, iterations, epsilon):
    x_data = [x]
    y_data = [y]
    i = 1
    while (abs(f(x,y))>epsilon or i < iterations):
        d = gradient(x, y)
        x -= d[0] * beta_grad
        y -= d[1] * beta_grad
        x_data.append(x)
        y_data.append(y)
        i += 1
    return [x_data, y_data]


# Newton's Method
def hess_func(x, y, beta_hess, hessian, iterations, epsilon):
    x_data = [x]
    y_data = [y]
    i = 1
    while (abs(f(x,y))>epsilon or i < iterations):
        d = gradient(x, y)
        d1 = [hessian[0][0] * d[0] + hessian[0][1] * d[1] , hessian[1][0] * d[0] + hessian[1][1] * d[1]]                     # d1 = hessian^(-1) * gradient
        x -= d1[0] * beta_hess
        y -= d1[1] * beta_hess
        x_data.append(x)
        y_data.append(y)
        i += 1
    return [x_data, y_data]

# times:
# def grad_time(x, y, b):
#     a = grad_func(x, y, b).timeit(number=1)

# def Newton_time(x, y, b):
#     a = hess_func(x, y, b).timeit(number=1)


# drawing a plot
ax = plt.axes(projection='3d')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
x = np.linspace(-5, 5, 30)
y = np.linspace(-5, 5, 30)
A, B = np.meshgrid(x, y)
C = f(A, B)
ax.plot_surface(A, B, C, rstride=1, cstride=1,cmap='viridis', edgecolor='none', alpha=0.5)

#To get appropriate plot you should comment one section below:
#If both sections are uncommented, you get a plot with both methods.

#Gradient
ax.set_title('Steepest gradient descent method')
data = grad_func(X, Y, BETA_GRAD, ITERS, EPSILON)
xdata = data[0]
ydata = data[1]
zdata = []
for i in range(len(xdata)):
    zdata.append(f(xdata[i], ydata[i]))
ax.scatter3D(xdata, ydata, zdata, c="#000000")

# #Hessian
# ax.set_title("Newton's method")
# data = hess_func(X, Y, BETA_HES, HESS_1, ITERS, EPSILON)
# xdata = data[0]
# ydata = data[1]
# zdata = []
# for i in range(len(xdata)):
#     zdata.append(f(xdata[i], ydata[i]))
# ax.scatter3D(xdata, ydata, zdata, c="#000000")

plt.show()

# liczba iteracji
# mierzenie czasu
# raport