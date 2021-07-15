import numpy as np
import matplotlib.pyplot as plt

def createPlotsD():
    # Read Data
    # ---------
    strain = np.loadtxt('CycstrainD.out')
    stress = np.loadtxt('CycstressD.out')

    #Remove time column
    strain = np.delete(strain, 0, 1)
    stress = np.delete(stress, 0, 1)

    p0  = (stress[0,0]+stress[0,1]) / 2.0
    p   = (stress[:,0]+stress[:,1]) / 2.0
    ru  = 1 - p / p0  # ru evaluated using change in effective mean stress p
    ru2 = 1-stress[:,1]/stress[0,1]  # ru evaluated using chanve in vertical effective stress
 

    #Plot Results
    # -----------
    fig1 = plt.figure(num=1, figsize=(14, 4))
    plt.clf()
    
    axs = []
    axs.append(fig1.add_subplot(131))
    axs.append(fig1.add_subplot(132))
    axs.append(fig1.add_subplot(133))
    
    axs[0].clear()
    axs[0].plot(strain[:,2]*100, stress[:,2], color='black', linestyle='solid', linewidth=1.25)
    axs[0].set_xlabel(r'$\gamma$(%)', fontsize=14)
    axs[0].set_ylabel(r'$\tau$(kPa)', fontsize=14)
    axs[0].grid(True)
    # --------------------
    axs[1].clear()
    axs[1].plot(-stress[:,1], stress[:,2], color='black', linestyle='solid', linewidth=1.25)
    axs[1].set_ylabel(r'$\tau$(kPa)', fontsize=14)
    axs[1].set_xlabel(r'$\sigma_v$ (kPa)', fontsize=14)
    axs[1].grid(True)
    # --------------------
    axs[2].clear()
    axs[2].plot(strain[:,2]*100, ru2, color='black', linestyle='dashed',  linewidth= 1.00, label=r'$1-\sigma_v / \sigma_{v0}$' )
    #axs[2].plot(strain[:,2]*100, 1-stress[:,1]/stress[0,1], color='green', linestyle='dashed',  linewidth= 1.00, label=r'$1-\sigma_v / \sigma_{v0}$' )
    axs[2].plot(strain[:,2]*100, ru, color='black', linestyle='solid',  linewidth= 1.00, label=r'$1-p / p_{0}$' )
    axs[2].set_ylabel(r'Ru', fontsize=14)
    axs[2].set_xlabel(r'$\gamma$(%)', fontsize=14)
    axs[2].grid(True)
    axs[2].set_xlim(-3, 3)
    axs[2].legend()

    plt.savefig(r'PM4Sand_wikiD.png')
    plt.show()
    

    #plt.figure(figsize=(12, 12))
    #plt.clf()
    #plt.subplot(2, 2, 1)
    #plt.plot(strain[:,2]*100, stress[:,2], color='black', linestyle='solid', linewidth=1.25)
    #plt.grid()
    #plt.xlabel(r'$\gamma$(%)', fontsize=14)
    #plt.ylabel(r'$\tau$(kPa)', fontsize=14)
#
    #plt.subplot(2, 2, 2)
    #plt.plot(-stress[:,1], stress[:,2], color='black', linestyle='solid', linewidth=1.25)
    #plt.grid()
    #plt.xlabel(r'$\sigma_v$ (kPa)', fontsize=14)
    #plt.ylabel(r'$\tau$(kPa)', fontsize=14)
#
    #plt.subplot(2, 2, 4) 
    #plt.plot(strain[:,2]*100, 1-stress[:,1]/stress[0,1], color='green', linestyle='dashed',  linewidth= 1.00, label=r'$1-\sigma_v / \sigma_{v0}$' )
    #plt.plot(strain[:,2]*100, ru, color='blue', linestyle='solid',  linewidth= 1.00, label=r'$1-p / p_{0}$' )
    #plt.xlim(-3, 3)
    #plt.grid()
    #plt.xlabel(r'$\gamma$(%)', fontsize=14)
    #plt.ylabel(r'Ru', fontsize=14)
    #plt.legend()

    #plt.savefig(r'PM4Sand_wikiD.png')

    #plt.show()

def createCombinedPlots(expDataFile='Dr67_100.txt', simDataFile='nCyclesResultD.dat', cols =3):

    # Read data
    # ---------
    # simDataFile = 'nCyclesResultD.dat'
    # simData = np.loadtxt(simDataFile, dtype=float,delimiter=',',usecols=(0, 1), skiprows = 1)
    simData = np.loadtxt(simDataFile, dtype=float,usecols=(0, 1))

    # expDataFile = 'Dr67_100.txt'
    expData = np.loadtxt(expDataFile,skiprows = 1)

    #Plot Results
    # -----------
    fig1 = plt.figure(num=1, figsize=(8, 6))
    plt.clf()
    
    axs = []
    axs.append(fig1.add_subplot(111))
    
    axs[0].clear()
    axs[0].semilogx(simData[:,1], simData[:,0], marker = 'o', markersize = 8,  markerfacecolor='w', markeredgewidth=1.5, markeredgecolor='black', color='black', linestyle='solid', linewidth=1.25, label = 'Simulation')
    axs[0].semilogx(expData[:,cols], expData[:,0], marker = 'o', markersize = 8,  markerfacecolor='k', markeredgewidth=1.5, markeredgecolor='black', color='black', linestyle='solid', linewidth=1.25, label = 'Experiment')
    axs[0].set_xlabel(r'# of cycles', fontsize=14)
    axs[0].set_ylabel(r'CSR', fontsize=14)
    # axs[0].set_xlim(5, 500)
    # axs[0].set_ylim(0.10, 0.17)
    axs[0].grid(color = 'blue', linestyle = '--', linewidth = 0.3)
    axs[0].legend()

    plt.savefig(r'PM4Sand_CSR-Ncycles.png')
    plt.show()


if __name__ == "__main__":
    createPlotsD()
