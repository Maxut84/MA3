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

    x_in, y_in, x_ut, y_ut = [], [], [], []
    total_inside = 0
    
    for i in range(n):
        x = random.uniform(-1,1)
        y = random.uniform(-1,1)
        
        if m.sqrt((x)**2 + (y)**2) <= 1:
            x_in.append(x)
            y_in.append(y)
            total_inside += 1
    
        else:
            x_ut.append(x)
            y_ut.append(y)
            
    est_pi = 4 * total_inside / n
    
    return est_pi

def sphere_volume(n, d): #Ex2, approximation
    
    #Generate point for every dimension
    rand_n = [[random.uniform(-1,1) for i in range(d)] for i in range(n)] 
    
    #square sum, term(villkoret)  ↓ function iterable ↓  ↓ initalizer for reduce
    square= lambda suum: reduce(lambda x,y: x+y**2, suum, 0)
    
    #filter, is x<=1? (inside hypersphare)
    rand_n_inside = list(filter(lambda z: square(z) <= 1, rand_n))
    
    #like first ex, a cube is needed
    hyper_cube = 2**d
    est_vol = hyper_cube * len(rand_n_inside)/n

    return est_vol

def hypersphere_exact(d): #Ex2, real value
    return m.pi **(d/2)/m.gamma(d/2 + 1)

################################################################# gives  error why
#Ex3: parallel code - parallelize for loop
def sphere_volume_parallel1(n, d, np=10):
    # Run sphere_volume(n,d) np times in parallel
    with future.ProcessPoolExecutor() as ex:
        # replicate n and d np times so map can pass them to sphere_volume
        list_vals = list(ex.map(sphere_volume, [n]*np, [d]*np))
        #lambda _: sphere_volume(n, d), range(10)
    return mean(list_vals) 
###############################################################################

#Ex4: parallel code - parallelize actual computations by splitting data
def sphere_volume_parallel2(n,d,np=10):
    n_per_process = n // np

    with future.ProcessPoolExecutor() as ex:
        # compute volumes in parallel for each chunk
        partial_volumes = list(ex.map(sphere_volume, [n_per_process]*np, [d]*np))
    
    # average of partial estimates (since all have same n)
    return mean(partial_volumes)
    
def main():
    #Ex1
    dots = [1000, 10000, 100000]
    for n in dots:
        approximate_pi(n)
    #Ex2
    n = 100000
    d = 2
    sphere_volume(n,d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)} m^{d} ")

    n = 100000
    d = 11
    sphere_volume(n,d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)} m^{d} ")

    #Ex3
    n = 100000
    d = 11
    start = pc()
    Seq_Process = [sphere_volume(n, d) for i in range(10)]
    stop = pc()
    print(f"Ex3: Sequential time of {d} and {n}: {round(stop-start, 2)} sek")
    
    #Ex3 - parallel
    start = pc()
    Par_Process = sphere_volume_parallel1(n, d)
    stop = pc()    
    print(f"Parallel time for Ex3: {round(stop-start, 2)} sek")

    #Ex4
    n = 1000000
    d = 11
    start = pc()
    sphere_volume_parallel2(n, d)
    stop = pc()
    print(f"Ex4: Parallel time of {d} and {n}: {round(stop-start, 2)} sek")
    

    
    

if __name__ == '__main__':
	main()
