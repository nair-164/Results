import fileinput
import sys
import os
import numpy as np
import multiprocessing
from subprocess import call
import pandas as pd
from plotCRR import calculateCRR, calculatehpo

def runSandMixedDriver(inputList, CSR, maxStrain, sigmav, kAlpha, outputName):
	#print(os.getcwd())
	matInput = {'dr':0.65, 'Go':600.0, 'hpo':0.08, 'den':1.26, 'patm':101.3, 'h0':-1.0, 'emax':0.800,
	'emin' :0.500, 'nb':0.50, 'nd':0.10, 'Ado': -1.0, 'zmax':-1.0, 'cz': 250.0, 'ce': -1.0, 'phic':33.0,
	'nu':0.30, 'cgd': 2.0, 'cdr': -1.0, 'ckaf': -1.0, 'Q': 10.0, 'R':1.5, 'mpar': 0.01, 'Fsed_min': -1.0,
	'p_sedo':-1.0}
	# store the order of input parameters
	dictOrder = ['dr', 'Go', 'hpo', 'den', 'patm', 'h0', 'emax', 'emin', 'nb', 'nd', 'Ado', 'zmax','cz', 'ce'
		,'phic', 'nu', 'cgd', 'cdr', 'ckaf', 'Q', 'R', 'mpar', 'Fsed_min','p_sedo' ] 
	for key, value in inputList.items():
		if key in matInput:
			matInput[key] = float(value)
		if key == 'N160':
			Cd = 46.0
			matInput['dr'] = ((float(value)) / Cd)	** 0.5
			matInput['Go'] = 167.0 * (matInput['dr'] ** 2 * Cd + 2.5) ** 0.5

	f = open('Material.in','w')
	for param in dictOrder:
		f.write('%s = %f;\n'% (param, matInput[param]))
	f.close()	
	# Config file + Material file + CSS test + CSR + Max cycles + Max Strain + Initial Sigv
	# + K0 + Output file 
	if (sys.platform == 'win32'):
		args = "C:/Tools/bin/MixedDriver.exe \
			Config.in Material.in CSS {:.3f} 200 {:.3f} {:.1f} 0.5 {:.3f} " + outputName
	else:
		args = "/mnt/c/Tools/bin/MixedDriverSand.exe \
			Config.in Material.in CSS {:.3f} 200 {:.3f} {:.1f} 0.5 {:.3f} " + outputName
	args2 = args.format(CSR, maxStrain, sigmav, kAlpha)
	# print(args2)
	call(args2.split())

def runSiltMixedDriver(inputList, CSR, maxStrain, sigmav, outputName):	
	matInput = {'Su' : -1.0, 'su_rate' : 0.5, 'Go' : 600.0, 'hpo' : 20.0, 'den' : 1.26, 'Su_factor' : -1.0, 'patm' : 101.3, 
	'nu' : 0.30, 'nG' : 0.75, 'h0' : -1.0, 'eInit' : 0.9, 'labmbda' : 0.06, 'phicv' : 32.0, 'nb_wet' : 0.8,  
	'nb_dry' : 0.500, 'nd' : 0.30, 'Ado': -1.0, 'ru_max' : -1.0, 'zmax' : -1.0, 'cz' : 100.0, 'ce' : -1.0,
	'cgd' : -1.0, 'ckaf' : -1.0, 'mpar' : 0.01, 'CG_consol' : -1.0}
	# store the order of input parameters
	dictOrder = ['Su', 'su_rate', 'Go', 'hpo', 'den', 'Su_factor', 'patm', 'nu', 'nG', 'h0', 'eInit', 'labmbda', 'phicv', 
	'nb_wet', 'nb_dry', 'nd', 'Ado', 'ru_max', 'zmax', 'cz', 'ce', 'cgd', 'ckaf', 'mpar', 'CG_consol' ] 
	for key, value in inputList.items():
		if key in matInput:
			matInput[key] = float(value)

	f = open('Material.in','w')
	for param in dictOrder:
		f.write('%s = %f;\n'% (param, matInput[param]))
	f.close()
	if matInput['Su'] > 0.0:
		CSRmax = matInput['Su'] / matInput['patm']
	else:
		CSRmax = matInput['su_rate']

	# CSRs = [CSRmax * 0.30, CSRmax * 0.40, CSRmax * 0.55, CSRmax * 0.63, CSRmax * 0.7, CSRmax * 0.75, CSRmax * 0.8, CSRmax * 0.96]
	err = open("log", "wb")

	if (sys.platform == 'win32'):
		args = "C:/Tools/bin/MixedDriverSilt.exe \
			Config.in Material.in CSS {:.3f} 200.0 {:.3f} {:.1f} 0.5 " + outputName
	else:
		args = "/mnt/c/Tools/bin/MixedDriverSilt.exe \
			Config.in Material.in CSS {:.3f} 200.0 {:.3f} {:.1f} 0.5 " + outputName
	args2 = args.format(CSR, maxStrain, sigmav)
	call(args2.split(), stderr = err)


def runPDMY03MixedDriver(inputList, CSR, maxStrain, sigmav, outputName):	
	matInput = {"rho" : 1.5, "refShearModul" :4.69e4, "refBulkModul" :1.251e5, "frictionAng": 30.0, "peakShearStra" :0.1, "refPress" : 101.3,
	"pressDependCoe" : 0.5, "PTAng" : 20.4, "mType" : 2, "ca" : 0.03, "cb" : 5, "cc" : 0.2, "cd" : 16.0, "ce" : 2.000000, "da" : 0.150,
	"db" : 3.0000, "dc" : -0.2, "noYieldSurf" : 20, "liq1" : 1.0, "liq2" : 0.0, "patm" : 101.3, "s0" : 1.73}
	# store the order of input parameters
	dictOrder = ["rho", "refShearModul", "refBulkModul", "frictionAng", "peakShearStra", "refPress","pressDependCoe", "PTAng", "mType",
	"ca", "cb", "cc", "cd", "ce", "da",	"db", "dc", "noYieldSurf", "liq1", "liq2", "patm", "s0"] 
	for key, value in inputList.items():
		if key in matInput:
			matInput[key] = float(value)

	f = open('Material.in','w')
	for param in dictOrder:
		f.write('%s = %f;\n'% (param, matInput[param]))
	f.close()

	if (sys.platform == 'win32'):
		args = "C:/Tools/bin/MixedDriverPDMY03.exe \
			Config.in Material.in CSS {:.3f} 200.0 {:.3f} {:.1f} 0.5 " + outputName
	else:
		args = "/mnt/c/Tools/bin/MixedDriverPDMY03.exe \
			Config.in Material.in CSS {:.3f} 200.0 {:.3f} {:.1f} 0.5 " + outputName
	args2 = args.format(CSR, maxStrain, sigmav)
	call(args2.split())

def generateInput(df):
	# create dictionary for generating material.in for MixedDriver 
	for index, row in df.iterrows():
		if row['Calibration'] in 'Yes':
			subdir = borehole + '-' + str(row['No.']) + '_' + row['Name']
			if not os.path.exists(subdir):
				os.makedirs(subdir)
			os.chdir(subdir)
			matInput = {}
			matInput['dr'] = ((float(row['N160CS'])) / Cd)	** 0.5
			matInput['Go'] = row['Go']
			matInput['patm'] = patm
			matInput['CSR'] = row['CRR']
			# cp for linux and copy for Windows
			os.system('cp ../Config.in Config.in')
			if row['Method'] == 1:
				# generate full CRR curve using multiple CSRs
				matInput['hpo'] = row['hpo']
				CSRs = [matInput['CSR'] / 2.0,  matInput['CSR'] / 1.5, matInput['CSR'] / 1.25, matInput['CSR'], \
	 				matInput['CSR'] * 1.25, matInput['CSR'] * 1.5, matInput['CSR'] * 2.0]
				for csr in CSRs:
					runSandMixedDriver(matInput, csr, 0.03, initialVStress, "csr{:.3f}.out".format(csr))
				calculateCRR()
			elif row['Method'] == 2:
				# check a series of hpos and find the one associated with 15 cycles
				Hpos = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
				for hpo in Hpos:
					matInput['hpo'] = hpo
					runSandMixedDriver(matInput, matInput['CSR'], 0.03, initialVStress, "hpo{:.1f}.out".format(hpo))
				calculatehpo()
			elif row['Method'] == 3:
				# calibration using both input csr and hpo
				Hpos = np.array([0.8, 0.9, 1.0, 1.1, 1.2]) * row['hpo']
				for hpo in Hpos:
					matInput['hpo'] = hpo
					runSandMixedDriver(matInput, matInput['CSR'], 0.03, initialVStress, "hpo{:.1f}.out".format(hpo))
				calculatehpo()
			else:
				print('Wrong method')	
			os.chdir('../')

if __name__ == "__main__":
	df = pd.read_csv('calibration.csv')
	borehole = 'B16'
	patm = 2107
	initialVStress = 1.0 * patm
	Cd = 46
	generateInput(df)

	## parallel part, needs more testing ##
	# num_processes = 4
	# pool = multiprocessing.Pool(num_processes)
	# # calculate the chunk size as an integer
	# chunk_size = int(df.shape[0]/num_processes)
	# chunks = [df.ix[df.index[i:i + chunk_size]] for i in range(0, df.shape[0], chunk_size)]
	# pool.map(generateInput, chunks)
