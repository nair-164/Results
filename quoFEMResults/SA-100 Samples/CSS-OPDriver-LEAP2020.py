#!/usr/bin/env python
# coding: utf-8
import numpy as np
from runPM4SandOP import runPM4SandOP
from Parameters import *
from scipy.optimize import curve_fit

open("nCyclesResultD.dat", 'w').close()

# Loading Conditions
# ------------------
# CSR = 0.11  # cyclic Stress Ratio
sigmav = 101.3  # Initial vertical effective stress
maxStrain = 0.03  # Max shear strain used as criteria for liquefaction initiation
alpha = 0.0  # Initial off-center shear stress ratio

# ## Material parameters
# inputList = {'Dr': Dr, 'G0': G0, 'hpo': hpo, 'rho': rho, 'h0': h0, 'emax': emax,
#                 'emin': emin, 'nb': nb, 'nd': nd, 'Ado': Ado, 'zmax': zmax, 'cz': cz, 'ce': ce,
#                 'phicv': phicv,
#                 'nu': nu, 'Cgd': Cgd, 'Cdr': Cdr, 'ckaf': ckaf, 'Q': Q, 'R': R, 'm_m': m_m, 'Fsed_min': Fsed_min,
#                 'p_sedo': p_sedo}
inputList = {'Dr': Dr, 'G0': G0, 'hpo': hpo, 'nb': nb, 'nd': nd}
# csrlist = np.genfromtxt('Ottawa_F65_ExpData.txt', usecols=(0))
csrlist = np.array([0.105, 0.105, 0.172, 0.2])
for x in csrlist[1:]:
    # print(x)
    runPM4SandOP(inputList, x, maxStrain, -sigmav, alpha)
    # createPlotsD()
# createCombinedPlots(expDataFile='Ottawa_F65_ExpData.txt', cols=2)

prediction = np.genfromtxt('nCyclesResultD.dat')
# prediction = np.vstack((prediction[0,:], prediction))

# power law fit function
def power(x, a, b):
    return (a * (x**(-b)))

csr4 = prediction[:,0]
cycles4 = prediction[:,1]
# plt.scatter(cycles4, csr4, s=60, c='blue', marker = 'P', edgecolor = 'cyan', label = 'Morales and Ziotopoulou (2018)')

# fitting the curve
# param, param_cov = curve_fit(power, cycles4, csr4, maxfev=10000);
try:
    param, param_cov = curve_fit(power, cycles4, csr4, maxfev=10000);
except:
    param = np.array([0.34, 0.27]);

# setting the parameter values
a, b = param;

np.savetxt('results.out', np.hstack((param[np.newaxis], cycles4[np.newaxis])))

