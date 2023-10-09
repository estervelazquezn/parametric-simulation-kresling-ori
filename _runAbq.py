""""
Run Abq from Python
------------------------------------------------------
 Generates the Abq file from the sampled data
    
    - INPUTS: values generated by the sampling that fits into the Kresling
               geometry restrictions in a txt file named '_sampling_data.txt'

               This txt includes by rows the following data:

                n - Sample list with number of polygon sides
                h - Sample list with flat pattern height
                R - List of radius according to the samples generated
              
    - OUTPUTS: Abaqus output files 


"""

import numpy as np
import _kreslingGeometry

n = 6
h = 45
R = 50

geoInputs = {
'n': n, 'R': R, 'h': h
}

(geoOutputs) = _kreslingGeometry.Geometry(geoInputs)
print("h3 = ", geoOutputs['h3'])

# Parametric data from txt
n = geoOutputs['n']
R = geoOutputs['R']
h = geoOutputs['h']
xH = geoOutputs['xH']
a = geoOutputs['a']
h3 = geoOutputs['h3']
rho = geoOutputs['delta']

# Additional data
nMesh = 20
N = 2
period = 0.01
nIntervals = period/50
thickness = 0.5
Dist = 5
materialId = 'TPU'
folderCAE = '_CAE/'
step = 'FOLD'

# Define the file name
jobName = '0-' + step + '-n-' + str(n) + '-h-' + str(int(h*100)) + 'e-2'
print(jobName)

import _geo2abq
# Run the main function
_geo2abq.run(n,R,h, xH, a, h3, rho,jobName,nMesh,period,materialId,N,thickness,folderCAE,step,nIntervals,Dist)
