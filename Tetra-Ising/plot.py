import math
import h5py
import sys
import numpy as np
from matplotlib import pyplot as plt
import multiprocessing as mp
from time import time

title = 'Tetra'

Latticesizes=   [12, 16, 20, 24, 28]

color = [ (0,0,0), (0,0.3,0.8), (0.3,0.7,0), 
          (0.7,0.6,0.),(0.72,0,0),(0.8,0,0.42), (0.9,0,0.7) ]
markercolor = [ (0,0,0), (0,0.3*0.8,0.8*0.8), (0.3*0.8,0.7*0.8,0), 
          (0.7*0.8,0.6*0.8,0.),(0.72*0.8,0,0),(0.8*0.8,0,0.42*0.8), (0.9*0.8,0,0.7*0.8) ]



for i in range(len(Latticesizes)):
    print(Latticesizes[i])
    folderpath = 'L=' + str(Latticesizes[i])
    f = h5py.File('%s/Tetra.out.h5' %folderpath,'r')    

######## Initialization parameters ########    

    L = np.intc(f['/parameters/L'])
    if title == 'Tetra'  :
        lat_sites = 4*L*L*L
    if title == 'Fractal':
        lat_sites = L*L*L

    Npoints = np.intc(f['/parameters/N_replica'])
    NBins   = np.intc(f['/parameters/NBins']) + 1
    NBins_MUCA = np.intc(f['/parameters/NBins_muca']) + 2
    Nmeas = np.intc((f['/simulation/results/0/Energy/count']))
    
    E_histmat  = np.zeros((Npoints,NBins))  ## E_hist for each temperature
    DE_histmat = np.zeros((Npoints,NBins))  ## DE_hist for each temperature
    g   = np.zeros((Npoints,NBins_MUCA))    ## vector of weights used for each temperature
    T   = np.zeros(Npoints)                 ## Temperatures    
    c   = np.zeros(Npoints)                 ## normalization terms Z_muca/Z needed to find the correct terms, found through histogram renormalization

    ## Retrieving the energy intervals used for the MUCA sampling
    E_1 = np.float64(f['/parameters/E_1']) *lat_sites
    E_2 = np.float64(f['/parameters/E_2']) *lat_sites
    Emax = 2
    E_g =np.zeros(len(g[0,:]))
    E_g[0]=0    
    for m in range(1,len(g[0,:])):
        E_g[m] = E_1 + (m-1) * (E_2-E_1)/(len(g[0,:])-2)
    E = np.linspace(0,Emax*lat_sites,len(E_histmat[0,:]))



######## Fetch Data ########
    for q in range(Npoints):
        E_histmat[q,:] = np.array( f['/simulation/results/%s/Energy_Hist/mean/value' %q] )
        T[q] = np.float64(f['/simulation/results/%s/point'%q])
        c[q] = np.float64(f['/simulation/results/%s/C' %q] )
    DE_histmat = np.sqrt(E_histmat/(Nmeas))

######## Plot ########
    y = np.zeros(Npoints)
    dy= np.zeros(Npoints)

    plt.figure('E', figsize=(8,5))
    for q in range(Npoints):
        y[q] = np.float64(f['/simulation/results/%s/Energy/mean/value'%q]) * c[q]
        dy[q] = np.float64(f['/simulation/results/%s/Energy/mean/error'%q]) * c[q]
    plt.xlabel('T')
    plt.errorbar(T,y,dy,marker='.', linewidth = 0.8, label = L )
    plt.ylabel('E')

    plt.figure('C_v', figsize=(8,5))
    for q in range(Npoints):
        y[q] = np.float64(f['/simulation/results/%s/Energy_Susc/mean/value'%q]) * lat_sites / T[q]**2
        dy[q] = np.float64(f['/simulation/results/%s/Energy_Susc/mean/error'%q]) * lat_sites / T[q]**2
    plt.xlabel('T')
    plt.errorbar(T,y,dy,marker='.', linewidth = 0.8, label = L )
    plt.ylabel('C_v')

    plt.figure('Q', figsize=(8,5))
    for q in range(Npoints):
        y[q] = np.float64(f['/simulation/results/%s/Q_x/mean/value'%q]) * c[q]
        dy[q] = np.float64(f['/simulation/results/%s/Q_x/mean/error'%q]) * c[q]
    plt.xlabel('T')
    plt.errorbar(T,y,dy,marker='.', linewidth = 0.8,label = L)
    plt.ylabel('Q')


    plt.figure('Q_susc', figsize=(8,5))
    for q in range(Npoints):
        y[q] = np.float64(f['/simulation/results/%s/Q_x_Susc/mean/value'%q])  *lat_sites / T[q]
        dy[q] = np.float64(f['/simulation/results/%s/Q_x_Susc/mean/error'%q]) *lat_sites / T[q]
    plt.xlabel('T')
    plt.errorbar(T, y, dy, marker = '.', linewidth=0.8,label = L)
    plt.ylabel('Q_susc')


    plt.figure('E_BC', figsize=(8,5))
    for q in range(Npoints):
        y[q] = 1 - (1/3) *np.float64(f['/simulation/results/%s/Energy_Kurt/mean/value'%q]) 
        dy[q] = (1/3)    *np.float64(f['/simulation/results/%s/Energy_Kurt/mean/error'%q])
    plt.xlabel('T')
    plt.errorbar(T, y, dy, marker = '.', linewidth=0.8,label = L)
    plt.ylabel('E_BC')

    plt.figure('Q_BC', figsize=(8,5))
    for q in range(Npoints):
        y[q] = 1 - (1/3) *np.float64(f['/simulation/results/%s/Q_x_Kurt/mean/value'%q]) 
        dy[q] = (1/3)    *np.float64(f['/simulation/results/%s/Q_x_Kurt/mean/error'%q])
    plt.errorbar(1/T,  y, dy, label = L, color=color[i], linestyle = '-',linewidth=2, 
                  marker = '.', markersize=8, capsize=3, mfc = markercolor[i], 
                  mec = markercolor[i], ecolor = markercolor[i], zorder=12-i
                )
    plt.xlabel(r'$\beta$',fontweight='bold')
    plt.ylabel(r'$B$')
    plt.tick_params(which='major', direction="in")
    plt.tick_params(which='minor', direction="in")
    plt.minorticks_on()




for i in plt.get_fignums():
    plt.legend()
#    plt.figure(i).savefig(str(i) + '.pdf', format='pdf')
plt.show()