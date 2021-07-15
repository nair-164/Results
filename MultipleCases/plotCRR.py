import glob, sys, os, csv
import numpy as np
import matplotlib.pyplot as plt
from math import ceil
from scipy.interpolate import PchipInterpolator

def calculateCRR():
    outputFiles = sorted(glob.glob('csr*.out'))
    CSR3s = np.empty([0, 1])
    numCycle3_all = np.empty([0, 1])

    for outputFile in outputFiles:
        data = np.loadtxt(outputFile,skiprows = 1)
        s12 = data[:,5]
        # absolute value of shear strain
        e12 = data[:,2]
        s11 = data[0,3]
        csr = round(np.amax(s12) / s11, 2)
        cycle = np.cumsum(abs(np.diff(s12)))/(4.0 * csr * s11)
        if cycle[-1] <= 199.0 and cycle[-1] >= 0.5:
            # liquefaction was triggered
            numCycle3_all = np.append(numCycle3_all, ceil(cycle[-1] * 2.0) / 2.0)
            CSR3s = np.append(CSR3s, csr)
        else:
            print("did not reach 3% in 200 cycles")

        #fig = plt.figure()
        #plt.plot(e12 * 100.0, s12)
        #plt.xlabel(r'$\gamma(\%)$')
        #plt.ylabel(r'$\tau(psf)$')
        #plt.grid()
        #fig.savefig(outputFile[0:-4] + '.png')
        #plt.close()
    
    #logCSR3s = np.log(CSR3s)
    #lognumCycle3_all = np.log(numCycle3_all)
    ## add small machine precision number to prevent same value causing interpolation crush
    #lognumCycle3_all = np.flip(lognumCycle3_all, 0) + np.finfo(float).eps * np.cumsum(np.ones(np.size(lognumCycle3_all)))
    #pchip_obj3 = PchipInterpolator(lognumCycle3_all, np.flip(CSR3s,0))
    #crr3 = pchip_obj3(np.log(15.0))

    #fig = plt.figure()
    #plt.semilogx(numCycle3_all,CSR3s)
    #plt.semilogx([15.0, 15.0], [CSR3s[0], CSR3s[-1]], '--')
    #plt.text(15, crr3, "CRR15 = {:.3f}".format(crr3), fontsize=12)
    #plt.xlabel('Number of Cycles')
    #plt.ylabel('CSR')
    #plt.grid()
    #fig.savefig('CRR.png')
    #plt.close()

    np.savetxt('results.csv', np.transpose([CSR3s, numCycle3_all]), delimiter=',', fmt="%5.2f", header='CSR, NumberCycles')
    #np.savetxt('CRR.csv', np.array([crr3]), fmt="%.3f", header = 'CRR')
    return CSR3s, numCycle3_all


def calculatePlotCRR():
    outputFiles = sorted(glob.glob('csr*.out'))
    CSR3s = np.empty([0, 1])
    numCycle3_all = np.empty([0, 1])

    for outputFile in outputFiles:
        data = np.loadtxt(outputFile,skiprows = 1)
        s12 = data[:,5]
        # absolute value of shear strain
        e12 = data[:,2]
        s11 = data[0,3]
        csr = round(np.amax(s12) / s11, 2)
        cycle = np.cumsum(abs(np.diff(s12)))/(4.0 * csr * s11)
        if cycle[-1] <= 199.0 and cycle[-1] >= 0.5:
            # liquefaction was triggered
            numCycle3_all = np.append(numCycle3_all, ceil(cycle[-1] * 2.0) / 2.0)
            CSR3s = np.append(CSR3s, csr)
        else:
            print("did not reach 3% in 200 cycles")

        fig = plt.figure()
        plt.plot(e12 * 100.0, s12)
        plt.xlabel(r'$\gamma(\%)$')
        plt.ylabel(r'$\tau(psf)$')
        plt.grid()
        fig.savefig(outputFile[0:-4] + '.png')
        plt.close()
    
    logCSR3s = np.log(CSR3s)
    lognumCycle3_all = np.log(numCycle3_all)
    # add small machine precision number to prevent same value causing interpolation crush
    lognumCycle3_all = np.flip(lognumCycle3_all, 0) + np.finfo(float).eps * np.cumsum(np.ones(np.size(lognumCycle3_all)))
    pchip_obj3 = PchipInterpolator(lognumCycle3_all, np.flip(CSR3s,0))
    crr3 = pchip_obj3(np.log(15.0))

    fig = plt.figure()
    plt.semilogx(numCycle3_all,CSR3s)
    plt.semilogx([15.0, 15.0], [CSR3s[0], CSR3s[-1]], '--')
    plt.text(15, crr3, "CRR15 = {:.3f}".format(crr3), fontsize=12)
    plt.xlabel('Number of Cycles')
    plt.ylabel('CSR')
    plt.grid()
    fig.savefig('CRR.png')
    plt.close()

    np.savetxt('results.csv', np.transpose([CSR3s, numCycle3_all]), delimiter=',', fmt="%5.2f", header='CSR, NumberCycles')
    np.savetxt('CRR.csv', np.array([crr3]), fmt="%.3f", header = 'CRR')
    return CSR3s, numCycle3_all


def calculatehpo():
    outputFiles = sorted(glob.glob('hpo*.out'))
    hpos = np.empty([0, 1])
    numCycle3_all = np.empty([0, 1])
    for outputFile in outputFiles:
        data = np.loadtxt(outputFile, skiprows = 1)
        s12 = data[:,5]
        # absolute value of shear strain
        e12 = data[:,2]
        s11 = data[0,3]
        hpos = np.append(hpos, float(outputFile[3:5]))
        csr = round(np.amax(s12) / s11, 2)
        cycle = np.cumsum(abs(np.diff(s12)))/(4.0 * csr * s11)
        if cycle[-1] <= 199.0 and cycle[-1] >= 0.5:
            # liquefaction was triggered
            numCycle3_all = np.append(numCycle3_all, ceil(cycle[-1] * 2.0) / 2.0)
        else:
            print("did not reach 3% in 200 cycles")

        fig = plt.figure()
        plt.plot(e12 * 100.0, s12)
        plt.xlabel(r'$\gamma(\%)$')
        plt.ylabel(r'$\tau(psf)$')
        plt.grid()
        fig.savefig(outputFile[3:5] + '.png')
        plt.close()
    
    numCycle3_all = numCycle3_all + np.finfo(float).eps * np.cumsum(np.ones(np.size(numCycle3_all)))
    pchip_obj3 = PchipInterpolator(numCycle3_all, hpos)
    try:
        hpo15 = pchip_obj3(15.0)
    except:
        hpo15 = 'NAN'
    
    np.savetxt('hpo.csv', np.array([hpo15]), fmt="%.3f", header = 'hpo')
    fig = plt.figure()
    plt.plot(numCycle3_all,hpos)
    plt.plot([15.0, 15.0], [1.5, 5.0], '--')
    plt.xlabel('Number of Cycles')
    plt.ylabel('hpo')
    plt.grid()
    fig.savefig('hpo.png')
    plt.close()

if __name__ == "__main__":
    #os.chdir(sys.argv[1])
    calculateCRR()
