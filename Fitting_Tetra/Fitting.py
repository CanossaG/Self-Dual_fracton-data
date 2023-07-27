import math
import h5py
import sys
import numpy as np
import pandas as pd
import dataset
from scipy.optimize import curve_fit
import scipy.optimize as optimization
import scipy.stats as stats
from scipy.optimize import leastsq
import scipy.special as sf
import matplotlib
from matplotlib import pyplot as plt
from operator import itemgetter
import matplotlib.ticker as mticker

sys.path.insert(1,'../')
from plt_settings import plt_settings
plt_settings()
np.set_printoptions(threshold=sys.maxsize)


#define exponential factor for the lengths (1/F will be used)
F=2
print('fitting with \u03BD=%f'%F)

Ndata=5
data = np.loadtxt('fittemps.txt')
titles = [r'$C_{V\rm  max}$',r'$\chi_{\rm  max}$',r'$B_{\rm  min}$',r'$P_{\rm eqw}$']

ENNE=1
column= [5,7,9,3]

colorfit = [(0.9,0,0), (0,0.9,0), (0,0,0.9), (1,0.6,0.), (0.3,0.3,0.3),(0.3,0.6,0.)] 
colordata = [(0.6,0,0),(0,0.6,0),(0,0,0.6),(0.8,0.5,0.),(0.2,0.2,0.2),(0.2,0.4,0.)]
markerfit = ['x','D','o','^','s']


for i in range(len(column)):

    L0      = data[:,0]
    Beta    = 1 / data[:,column[i]]
    Terr    = data[:,column[i]+1] 
    Beta_err= Terr*(Beta**2)

    x0=L0
    y0=Beta
    Sigma0=Beta_err

    x =x0[len(x0)-Ndata : len(x0)]
    y =y0[len(x0)-Ndata : len(x0)]
    L =L0[len(x0)-Ndata : len(x0)]
    Sigma = Sigma0[len(x0)-Ndata : len(x0)]

    func = lambda tpl,x : 0*tpl[0] + 1/(2/np.log(1+np.sqrt(2))) + tpl[1] *(x**(-F))
    ErrorFunc = lambda tpl,x,y,Sigma: ((func(tpl,x)-y))**2/Sigma**2
    diff = lambda tpl,x,y: func(tpl,x)-y

    Init= [0.4,-30.]
    params, cov,info,mesg, ier =leastsq(ErrorFunc,Init,args=(x,y,Sigma),maxfev=80000, full_output=1)    
    dP=np.zeros(len(params))
#    dP=cov**0.5
    print(titles[i])
    print ("outcomes:%f" %(1/params[0]))


    y_fit=func(params,x)
    chisq = sum((y_fit-y)**2/Sigma**2)
    dof   = len(y)-1
    print("\u03C7/DOF = %f" %(chisq/dof))


    xx=np.linspace(np.min(L0)-1,10**5,10)
    yy=func(params,xx)
    plt.figure('Fit',figsize=(8, 6))
    if (i==0):
        plt.plot(xx**(-F),yy,color='w',linestyle='',marker='')
        plt.plot(0 ,  1/(2/np.log(1+np.sqrt(2))) ,label=r'$\beta_{c}^{\infty} = \frac{1}{2} \text{log}(1+\sqrt2)$', color='k',mfc='k', marker='.', linestyle = '',markersize=25,zorder=10)

    plt.plot(xx**(-F) , yy ,label='%s'%(titles[i]), color=colorfit[i], linestyle = '-', linewidth = 2)
    plt.errorbar((L0)**(-F) , Beta ,Beta_err, color=colordata[i],linestyle = 'None', marker = markerfit[i],mfc='None',markersize=15,capsize=3)   


    plt.xlabel('$L^{-%s}$'%(F),fontweight='bold')
    plt.ylabel(r'$\beta$',fontweight='bold', labelpad=10)
    plt.legend(frameon=False)
#    plt.xlim([-0.000001,0.0013])
#    plt.ylim([1.544,1.5675])
    plt.tick_params(which='major', direction="in",labelsize=20)
    plt.tick_params(which='minor', direction="in",labelsize=20)
    plt.minorticks_on()


    RES = y_fit-y
    plt.figure('residues',figsize=(8, 6))
    plt.errorbar((1/L)**(F),RES,Sigma,color=colordata[i],linestyle='none', marker = 'o',elinewidth=1,capsize=8)
    plt.xlabel('$L^{-%s}$'%(F))
    plt.ylabel('Residues')


plt.show()

