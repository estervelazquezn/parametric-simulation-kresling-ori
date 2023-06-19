""""
Latin Hypercube Sampling to Geometry generation
------------------------------------------------------
 Generates the 'txt' to be read by Abaqus script (called in the script '_runabq.py')
    
    - INPUTS: 'y' or 'n' (needed to be writen in terminal to specify is the sampling 
              has been previously made or not)
    - OUTPUTS: txt file configured to be read in script '_runabq.py'

"""
import numpy as np
import _kreslingGeometry
import _LHSampling

#-------------------------------------------------------------
# Interpretation of the txt previously generated with the script '_LHSampling.py'
def txtInterpreter():
    data = np.loadtxt('_sampling_data.txt',delimiter=' ')
    nlist = data[0,:]
    hlist = data[1,:]
    Rlist = data[2,:]
    geoGenerator(nlist,hlist,Rlist)

#-------------------------------------------------------------
# Generation of a new sampling calling the script '_LHSampling.py'
def samplingGenerator(num):
    [nlist,hlist,Rlist] = _LHSampling.data(num)
    geoGenerator(nlist,hlist,Rlist)

#-------------------------------------------------------------
# Creation of the geoemtry calling the script '_kreslingGeometry.py'
def geoGenerator(nlist,hlist,Rlist):
    kresling_data = np.zeros((len(nlist),7))

    for i in range(len(nlist)):
        n = int(nlist[i])
        h = np.round(hlist[i])
        R = np.round(Rlist[i])

        geoInputs = {
        'n': n, 'R': R, 'h': h
        }

        print('\nSample n =', i+1)
        (geoOutputs) = _kreslingGeometry.Geometry(geoInputs)
        print("h3 = ", geoOutputs['h3'])
        kresling_data[i,:] = [geoOutputs['n'],geoOutputs['R'],geoOutputs['h'],
                            geoOutputs['xH'],geoOutputs['a'],geoOutputs['h3'],geoOutputs['delta']]

    np.savetxt('_kresling_data.txt',kresling_data,delimiter=" ")

#-------------------------------------------------------------
# Management of the input value obtained
def inputManage(inputVal):
    while inputVal != 'y' and inputVal != 'n':
        print('Please enter valid command (y/n)')
        inputVal = input()

    if inputVal == 'y':
        txtInterpreter()
    elif inputVal == 'n':
        print('Please specify the number of samples desired (integer value)')
        num = input()
        samplingGenerator(int(num))        


#==================================================================
# -------------- M A I N ------------------------------------------
#
if __name__ == "__main__":
    print('--- LSH2geo -----------------------------------------------------------')
    print('- Enter (y) if you have created the txt file named _sampling_data.txt')
    print('- Enter (n) if you want to create a new sampling')
    print('-----------------------------------------------------------------------')
    input1 = input()
    inputManage(input1)



