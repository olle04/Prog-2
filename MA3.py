""" MA3.py

Student:
Mail:
Reviewed by:
Date reviewed:

"""
import random
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
from statistics import mean 
from time import perf_counter as pc
from functools import reduce

def approximate_pi(n): # Ex1
    ncx = []
    ncy = []
    nsx = []
    nsy = []
    nc = 0
    for i in range(n):
        x = random.uniform(-1,1)
        y = random.uniform(-1,1)
        if x**2 + y**2 <= 1:
            nc +=1
            ncx.append(x)
            ncy.append(y)
        else:
            nsx.append(x)
            nsy.append(y)
    pi = 4*nc/n
    print(f'Approximation of pi using Monte Carlo with {n} points is {pi}')

    plt.scatter(ncx, ncy, color='red')
    plt.scatter(nsx, nsy, color='blue')
    filename = f'plot_{n}_points_mc_pi'
    plt.savefig(filename)        
    return pi

def sphere_volume(n, d): #Ex2, approximation
    ns = 0
    for i in range(n):
        vektor = [random.uniform(-1, 1) for i in range(d)]
        distance = m.sqrt(reduce(lambda value, entery : value + entery**2, vektor, 0))
        if distance <= 1:
            ns += 1
    return ns/n * 2**d

def hypersphere_exact(d): #Ex2, real value
    return (m.pi ** (d / 2)) / m.gamma((d / 2) + 1)

#Ex3: parallel code - parallelize for loop
def sphere_volume_parallel1(n,d,np=10):
    start = pc()
    with future.ProcessPoolExecutor() as ex:
        futures = [ex.submit(sphere_volume, n, d) for i in range(10)]
        result = [i.result() for i in futures]
    avr = sum(result)/len(result)
    end = pc()
    print(f'Avrage:{avr} and time:{round(end-start, 3)} s')
    return avr

def loop_sphere():
    start = pc()
    total = [sphere_volume(10**5, 11) for i in range(10)]
    avr = sum(total)/len(total)
    end = pc()
    print(f'Avrage:{avr} and time:{round(end-start, 3)} s')
    return avr

#Ex4: parallel code - parallelize actual computations by splitting data
def sphere_volume_parallel2(n,d,np=10):
    start = pc()
    processize = n // np
    with future.ProcessPoolExecutor() as ex:
        futures = [ex.submit(sphere_volume, processize, d) for i in range(10)]
        result = [i.result() for i in futures]
    result = mean(result)
    end = pc()
    print(f'Approximation: {result}, Time: {round(end - start, 3)} s')
    return result
    
def sphere_sequential (n, d):
    n, d = 10**6, 11
    start = pc()
    result = sphere_volume(n, d)
    end = pc()
    print(f'Volume: {result} and time: {round(end - start, 3)} s')
    return result

def main():
    #Ex1
    dots = [1000, 10000, 100000]
    for n in dots:
        approximate_pi(n)
    #Ex2
    n = 100000
    d = 2
    sphere_volume(n,d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)}")

    n = 100000
    d = 11
    sphere_volume(n,d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)}")

    #Ex3
    n = 100000
    d = 11
    start = pc()
    for y in range (10):
        sphere_volume(n,d)
    stop = pc()
    print(f"Ex3: Sequential time of {d} and {n}: {stop-start}")
    print("What is parallel time?")

    #Ex4
    n = 1000000
    d = 11
    start = pc()
    sphere_volume(n,d)
    stop = pc()
    print(f"Ex4: Sequential time of {d} and {n}: {stop-start}")
    print("What is parallel time?")

    
    

if __name__ == '__main__':
	main()
