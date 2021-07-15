#!/usr/bin/env python
# coding: utf-8
import numpy as np
from runPM4SandOP import runPM4SandOP
from Parameters import *

open("nCyclesResultD.dat", 'w').close()

# Loading Conditions
# ------------------
# CSR = 0.11  # cyclic Stress Ratio
sigmav = 101.3  # Initial vertical effective stress
maxStrain = 0.03  # Max shear strain used as criteria for liquefaction initiation
alpha = 0.0  # Initial off-center shear stress ratio

# ## Material parameters
inputList = {'Dr': Dr, 'G0': G0, 'hpo': hpo}
csrlist = np.genfromtxt('Ottawa_F65_ExpData.txt', usecols=(0))
for x in csrlist[1:]:
    # print(x)
    runPM4SandOP(inputList, x, maxStrain, -sigmav, alpha)
    # createPlotsD()
# createCombinedPlots(expDataFile='Ottawa_F65_ExpData.txt', cols=2)

prediction = np.genfromtxt('nCyclesResultD.dat')
prediction = np.vstack((prediction[0,:], prediction))
np.savetxt('results.out', prediction[:,1], fmt='%4.2f')

