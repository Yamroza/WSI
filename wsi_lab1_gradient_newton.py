import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import random

# Booth function:
def f(x, y):
    return ((x + 2*y - 7)**2 + (2*x + y - 5)**2)

def x_dev(x, y):
    return 10*x + 8*y - 34

def y_dev(x, y):
     return 8*x + 10*y - 38

def gradient(x, y):
    return [x_dev(x, y), y_dev(x, y)]

X_X_DEV = 10
Y_Y_DEV = 10
X_Y_DEV = Y_X_DEV = 8
HESS = [[10, 8], [8, 10]]
HESS_1 = [[5/18, -4/18], [-4/18, 5/18]]
BETA_GRAD = 0.1
BETA_HES = 5
X = random.randint(-5, 5)
Y = random.randint(-5, 5)

def grad_func():
    x = random.randint(-5, 5)
    y = random.randint(-5, 5)
    print(x, y)
    #point = [x, y]
    e = 10**(-12)
    while (abs(f(x,y))>e):
        d = gradient(x, y)
        print(d)
        # point[0] += d[0] * BETA_GRAD
        # point[1] += d[1] * BETA_GRAD
        x -= d[0] * BETA_GRAD
        y -= d[1] * BETA_GRAD
        print ("x,y: ",x,y)


def hess_func():
    x = random.randint(-5, 5)
    y = random.randint(-5, 5)
    xdata = [x]
    ydata = [y]
    #point = [x, y]
    e = 10**(-12)
    while (abs(f(x,y))>e):
        d = gradient(x, y)
        d1 = [HESS_1[0][0] * d[0] + HESS_1[0][1] * d[1] , HESS_1[1][0] * d[0] + HESS_1[1][1] * d[1]]                     # d1 = hessian^(-1) * gradient
        #print(d1)
        # point[0] += d[0] * BETA_GRAD
        # point[1] += d[1] * BETA_GRAD
        x -= d1[0] * BETA_GRAD
        y -= d1[1] * BETA_GRAD
        xdata.append(x)
        ydata.append(y)
        #print ("x,y: ",x,y)
    return [xdata, ydata]



# def x_x_dev(x, y):
#     return 10

# def y_y_dev(x, y):
#     return 10

# def x_y_dev(x, y):
#     return 8

# def hessian(x, y):
#     return [[x_x_dev(x, y), x_y_dev(x, y)], [x_y_dev(x, y), y_y_dev(x, y)]]

# def hess_1(x,y):
#     return [[5/18, -4/18], [-4/18, 5/18]]

# drawing a plot


ax = plt.axes(projection='3d')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
data = hess_func()
xdata = data[0]
ydata = data[1]
zdata = []
for i in range(len(xdata)):
    zdata.append(f(xdata[i], ydata[i]))
ax.scatter3D(xdata, ydata, zdata, c="#000000")
x = np.linspace(-5, 5, 130)
y = np.linspace(-5, 5, 130)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)
#ax.plot_wireframe(X, Y, Z, color='black')
ax.plot_surface(X, Y, Z, rstride=1, cstride=1,cmap='viridis', edgecolor='none')
ax.set_title('Wykres')

plt.show()

hess_func()