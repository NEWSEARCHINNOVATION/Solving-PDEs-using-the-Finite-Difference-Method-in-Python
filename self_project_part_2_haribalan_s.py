# -*- coding: utf-8 -*-
"""Self Project_Part 2_Haribalan S.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QL2VRg9C6s2k0GTnvuSiHS1oy8I2k32Q
"""

"""
Importing required libraries as below
math library is used for mathematical expressions such as exponential etc.,
numpy library is used inorder to perform trigonometric operations and also to use pi value
matplotlib library is used mainly to plot graphs
"""
import math
import numpy as np
from matplotlib import pyplot as plt

"""
Initialization of variables are as follows
"""
L = 1                     # Thickness of wall
Ti = 40                   # Initial temperature
Ts = 200                  # Surface temperature
alpha = 2.6*10**(-6)      # Diffusivity of nickel steel
dx = 0.02                 # Grid size
dt = (0.5*dx**2)/(alpha)  # Time step size, calculated for CFL(alpha*del_t/del_x^2) equals 0.5, for stability
CN = round((L/dx)+1)      # No of computational nodes along x axis

"""
The below function is to compute the temperature profile
T = T(x, t) using Explicit Forward Time Central Space (FTCS)
For stability, the CFL number is taken as 0.5
"""
def FTCS(hour):                                                                 # Hour value is passed as an argument
  Nt = round((hour*3600)/dt)                                                    # Nt is number of time step calculated based on hour value
  T_0 = np.zeros((Nt+1,CN))                                                     # A 2D array is initialized to store the temperature along 1D space and time
  T_0[0,:], T_0[:,0], T_0[:,-1] = Ti, Ts, Ts                                    # Temperature values are initialized as per Boundary conditions
  for n in range(0,Nt):                                                         # For loop moving along time, till it reaches the final time step
    for i in range(1,CN-1):                                                     # For loop moving along space from i=1 till i=CN-1
      T_0[n+1][i] = T_0[n][i] + 0.5*(T_0[n][i+1] - 2*T_0[n][i] + T_0[n][i-1])   # Explicit FTCS scheme given in the question document
  return T_0[-1]                                                                # It returns the array with temperature value at final time step

"""
As given in Question 2, to verify that the explicit FTCS is unstable,
CFL number is selected greater than 0.5, here it is selected as 0.575
The observation is given in detail in the report
"""
def FTCS_unstable(hour):
  dt = (0.65*dx**2)/(alpha)
  Nt = round((hour*3600)/dt)
  T_0 = np.zeros((Nt+1,CN))
  T_0[0,:], T_0[:,0], T_0[:,-1] = Ti, Ts, Ts
  for n in range(0,Nt):
    for i in range(1,CN-1):
      T_0[n+1][i] = T_0[n][i] + 0.65*(T_0[n][i+1] - 2*T_0[n][i] + T_0[n][i-1])
  return T_0[-1]

def Crank_Nicholson(hour): # Hour value is passed as an argument
  Nt = round((hour*3600)/dt)                                                    # Nt is number of time step calculated based on hour value
  T_0 = np.zeros((Nt+1,CN))                                                     # A 2D array is initialized to store the temperature along 1D space and time
  T_0[0,:], T_0[:,0], T_0[:,-1] = Ti, Ts, Ts                                    # Temperature values are initialized as per Boundary conditions
  A = np.zeros((CN,CN))                                                         # Since it was solved by matrix inversion method by AX = B, A is initialized
  B = np.zeros((CN))                                                            # Similarly, B is initialized
  """
  The below for loops are to assign values of matrix A, 1.5 is the diagonal term
  which is the co-efficient of T_i_n+1 term and -0.25 is the co-efficient of
  T_i-1_n+1 and T_i+1_n+1. The values 1.5 and -0.25 are calculated based on
  taking the value of CFL as 0.5. Matrix X is also initialized to store the
  calculated values. In the for loop to calculate B, which is the RHS term,
  which remains in terms of T_n terms. Similarly, here the values 0.25 and 0.5
  are calculated by taking the value of CFL as 0.5. The first and last term
  (computational nodes) is the wall which is maintained at 200 degree celcius,
  So the value for "0"th and "CN" th term equals 200, which is given at the
  last in terms of B[0], B[-1]. linalg function is used to solve as using
  matrix inversion method
  """
  for i in range (CN):
    for j in range (CN):
      if i==j:
        A[i][j] = 1.5
      elif j == i+1 or j== i-1:
        A[i][j] = -0.25
  X = np.zeros(CN)
  X[:]=Ti; X[0]=Ts;X[-1] = Ts
  for n in range (0,Nt) :
    j=1
    B=np.copy(X)
    i=0
    for i in range (1,CN-1):
      if i == 0 or i == CN-1:
        B[j] = 0.25*X[i-1] + 0.5*X[i] + 0.25*X[i+1]  + 0.25*Ts
      else:
        B[j] = 0.25*X[i-1] + 0.5*X[i] + 0.25*X[i+1]
      j= j+1
    B[0] = Ts
    B[-1] = Ts
    print("B: ",B)
    X = np.linalg.solve(A, B)
    X[0]=Ts;X[-1] = Ts
  #print("CN",X)
  return X

"""
The below function is defined to calculate exact solution
"""
def Exact(hour):                                                                                       # Hour value is passed as an argument
  t = hour*3600                                                                                        # Hour is converted to seconds here
  sum = 0                                                                                              # Temproary variable to calculate sum inside the for loop
  Exact_soln = []                                                                                      # List to collect Exact solution values
  X = np.linspace(0,L,CN)                                                                              # X constitutes of distance of each node from origin along x axis
  for x in X:
    for m in range(1,100):
      sum = sum + (math.exp(-((m*np.pi)/L)**2 *alpha*t))*((1-(-1)**m)/(m*np.pi))*np.sin((m*np.pi*x)/L) # Summation term
    Exact_soln.append(Ts + 2*(Ti-Ts)*sum)                                                              # Appending of exact solution
    sum = 0
  #print("Exact ",Exact_soln)                                                                                         # Since to avoid overwriting of summation, sum is set to zero
  return Exact_soln                                                                                    # Returns the exact solution list

"""
The below function is to calculate the error between
exact solution and results of FTCS scheme
"""
def Error_FTCS(hour):
  temp = []
  temp = ((Exact(hour) - FTCS(hour))/Exact(hour))
  return temp

"""
The below function is to calculate the error between
exact solution and results of Crank Nicholson scheme
"""
def Error_CNN(hour):
  temp_ = []
  temp_ = ((Exact(hour) - Crank_Nicholson(hour))/Exact(hour))
  return temp_

"""
The below is the seperate function to plot results,
where the title, the function and y-axis label
are passed as arguments. Rest of syntax is general syntax
for plotting, which applies to all of the below plots

def plot_results(title,func,ylab):

    plt.figure(figsize=(5,15))

    plt.subplot(3,1,1)
    plt.plot(np.linspace(0, L, CN), func(0.1), color=np.random.rand(3,))
    plt.xlabel('x')
    plt.ylabel(ylab)
    plt.title(f'{title} (0.1 hour)')

    plt.subplot(3,1,2)
    plt.plot(np.linspace(0, L, CN), func(0.3), color=np.random.rand(3,))
    plt.xlabel('x')
    plt.ylabel(ylab)
    plt.title(f'{title} (0.3 hour)')

    plt.subplot(3,1,3)
    plt.plot(np.linspace(0, L, CN), func(0.5), color=np.random.rand(3,))
    plt.xlabel('x')
    plt.ylabel(ylab)
    plt.title(f'{title} (0.5 hour)')
"""
def plot_results(title, func, ylab):
  plt.figure(figsize=(8, 6))  # Adjust figure size as needed

  # Plot for 0.1 hour
  plt.plot(np.linspace(0, L, CN), func(0.1), label=f'{title} (0.1 hour)', color=np.random.rand(3,))

  # Plot for 0.3 hour
  plt.plot(np.linspace(0, L, CN), func(0.3), label=f'{title} (0.3 hour)', color=np.random.rand(3,))

  # Plot for 0.5 hour
  plt.plot(np.linspace(0, L, CN), func(0.5), label=f'{title} (0.5 hour)', color=np.random.rand(3,))

  plt.xlabel('x')
  plt.ylabel(ylab)
  plt.title(title)
  plt.legend()  # Add legend to distinguish different lines

def plot_results_single(title,func,ylab):

    plt.figure(figsize=(5,15))

    plt.subplot(3,1,1)
    plt.plot(np.linspace(0, L, CN), func(0.1), color=np.random.rand(3,))
    plt.xlabel('x')
    plt.ylabel(ylab)
    plt.title(f'{title} (0.1 hour)')

    plt.subplot(3,1,2)
    plt.plot(np.linspace(0, L, CN), func(0.3), color=np.random.rand(3,))
    plt.xlabel('x')
    plt.ylabel(ylab)
    plt.title(f'{title} (0.3 hour)')

    plt.subplot(3,1,3)
    plt.plot(np.linspace(0, L, CN), func(0.5), color=np.random.rand(3,))
    plt.xlabel('x')
    plt.ylabel(ylab)
    plt.title(f'{title} (0.5 hour)')

"""
The below is the seperate function to plot results,
where the title, the function (schemes)
are passed as arguments. Rest of syntax is general syntax
for plotting, which applies to all of the below plots
"""
def plot_comparison(title,scheme1,scheme2,func1,func2):

    plt.figure(figsize=(5,15))
    plt.subplot(3,1,1)
    plt.plot(np.linspace(0, L, CN), func1(0.1), color=np.random.rand(3,), label=f'{scheme1} scheme')
    plt.plot(np.linspace(0, L, CN), func2(0.1), color=np.random.rand(3,), label=f'{scheme2} scheme')
    plt.plot(np.linspace(0, L, CN), Exact(0.1), color='black', label='Exact solution', linestyle='dotted')
    plt.xlabel('x')
    plt.ylabel('Temperature(°C)')
    plt.legend()
    plt.title(f'{title} (0.1 hour)')

    plt.subplot(3,1,2)
    plt.plot(np.linspace(0, L, CN), func1(0.3), color=np.random.rand(3,), label=f'{scheme1} scheme')
    plt.plot(np.linspace(0, L, CN), func2(0.3), color=np.random.rand(3,), label=f'{scheme2} scheme')
    plt.plot(np.linspace(0, L, CN), Exact(0.3), color='black', label='Exact solution', linestyle='dotted')
    plt.xlabel('x')
    plt.ylabel('Temperature(°C)')
    plt.legend()
    plt.title(f'{title} (0.3 hour)')

    plt.subplot(3,1,3)
    plt.plot(np.linspace(0, L, CN), func1(0.5), color=np.random.rand(3,), label=f'{scheme1} scheme')
    plt.plot(np.linspace(0, L, CN), func2(0.5), color=np.random.rand(3,), label=f'{scheme2} scheme')
    plt.plot(np.linspace(0, L, CN), Exact(0.5), color='black', label='Exact solution',linestyle='dotted')
    plt.xlabel('x')
    plt.ylabel('Temperature(°C)')
    plt.legend()
    plt.title(f'{title} (0.5 hour)')

"""
The below is the seperate function to plot error comparison,
where the title, the function (schemes)
are passed as arguments. Rest of syntax is general syntax
for plotting, which applies to all of the below plots
"""
def Error_comparison(title,scheme1,scheme2,func1,func2):

    plt.figure(figsize=(5,15))
    plt.subplot(3,1,1)
    plt.plot(np.linspace(0, L, CN), func1(0.1), color=np.random.rand(3,), label=f'{scheme1} scheme')
    plt.plot(np.linspace(0, L, CN), func2(0.1), color=np.random.rand(3,), label=f'{scheme2} scheme',linestyle='dotted')
    plt.xlabel('x')
    plt.ylabel('Temperature(°C)')
    plt.legend()
    plt.title(f'{title} (0.1 hour)')

    plt.subplot(3,1,2)
    plt.plot(np.linspace(0, L, CN), func1(0.3), color=np.random.rand(3,), label=f'{scheme1} scheme')
    plt.plot(np.linspace(0, L, CN), func2(0.3), color=np.random.rand(3,), label=f'{scheme2} scheme',linestyle='dotted')
    plt.xlabel('x')
    plt.ylabel('Temperature(°C)')
    plt.legend()
    plt.title(f'{title} (0.3 hour)')

    plt.subplot(3,1,3)
    plt.plot(np.linspace(0, L, CN), func1(0.5), color=np.random.rand(3,), label=f'{scheme1} scheme')
    plt.plot(np.linspace(0, L, CN), func2(0.5), color=np.random.rand(3,), label=f'{scheme2} scheme',linestyle='dotted')
    plt.xlabel('x')
    plt.ylabel('Temperature(°C)')
    plt.legend()
    plt.title(f'{title} (0.5 hour)')

plot_results("FTCS Scheme",FTCS,"Temperature(°C)")

plot_results("Crank Nicholson Scheme",Crank_Nicholson,"Temperature(°C)")

plot_results_single("Explicit FTCS (Unstable)",FTCS_unstable,"Temperature(°C)")

plot_results("Exact Solution",Exact,"Temperature(°C)")

plot_comparison("Schemes Vs Exact","FTCS","Crank Nicholson",FTCS,Crank_Nicholson)

plot_results_single("Error wrt FTCS scheme",Error_FTCS,"Error")

plot_results("Error wrt Crank Nicholson scheme",Error_CNN,"Error")

Error_comparison("Error Comparison","FTCS","Crank Nicholson",Error_FTCS,Error_CNN)