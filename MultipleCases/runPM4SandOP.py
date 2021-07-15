import fileinput
import sys
import os
import numpy as np
import multiprocessing
from subprocess import call, DEVNULL
import pandas as pd
from subprocess import Popen

#from plotCRR import calculateCRR, calculatehpo

def runPM4SandOP(inputList, CSR, maxStrain, sigmav, kAlpha):
	#print(os.getcwd())
	matInput = {'Dr':0.65, 'G0':600.0, 'hpo':0.08, 'rho':1.26, 'Patm':101.3, 'h0':-1.0, 'emax':0.800,
	'emin' :0.500, 'nb':0.50, 'nd':0.10, 'Ado': -1.0, 'zmax':-1.0, 'cz': 250.0, 'ce': -1.0, 'phicv':33.0,
	'nu':0.30, 'Cgd': 2.0, 'Cdr': -1.0, 'ckaf': -1.0, 'Q': 10.0, 'R':1.5, 'm_m': 0.01, 'Fsed_min': -1.0,
	'p_sedo':-1.0}
	# store the order of input parameters
	dictOrder = ['Dr', 'G0', 'hpo', 'rho', 'Patm', 'h0', 'emax', 'emin', 'nb', 'nd', 'Ado', 'zmax','cz', 'ce'
		,'phicv', 'nu', 'Cgd', 'Cdr', 'ckaf', 'Q', 'R', 'm_m', 'Fsed_min','p_sedo' ] 
	for key, value in inputList.items():
		if key in matInput:
			matInput[key] = float(value)
		if key == 'N160':
			Cd = 46.0
			matInput['Dr'] = ((float(value)) / Cd)	** 0.5
			matInput['G0'] = 167.0 * (matInput['Dr'] ** 2 * Cd + 2.5) ** 0.5

		f = open('Material.tcl','w')

		for param in dictOrder:
			f.write('set %s %f;\n'% (param, matInput[param]))
		
		f.close()

        # CSR + Max cycles + Max Strain + Initial Sigv + K0

		filename = "DSS_quad_DispControl2.tcl"
		err = open("log", "wb")

		if (sys.platform == 'win32'):
			
			args = r"C:\Users\adith\Downloads\quoFEM_Windows_Download\quoFEM_Windows_Download\applications\opensees\bin\opensees.exe  DSS_quad_DispControl2.tcl {:.3f} 400 {:.3f} {:.1f} 0.5 {:.3f} "

			#command2Run = os.path.join('OpenSees ' + filename + ' {} 200 {} {} 0.5 {} ')
			#p = Popen(command2Run .format(CSR, maxStrain, sigmav, kAlpha), stderr = err, shell = True)

		else:
			args = r"C:\Users\adith\Downloads\quoFEM_Windows_Download\quoFEM_Windows_Download\applications\opensees\bin\opensees.exe " + filename + " {:.3f} 200 {:.3f} {:.1f} 0.5 {:.3f} "


	args2 = args.format(CSR, maxStrain, sigmav, kAlpha)
	print(args2)
	call(args2.split(), stderr = DEVNULL)

if __name__ == "__main__":

        CSR = 0.11
        maxStrain = 0.03
        sigmav = 101 
        kAlpha = 0.0

        runPM4SandOP(inputList, CSR, maxStrain, sigmav, kAlpha)
