import numpy as np

data = np.loadtxt('_kresling_data.txt',delimiter=' ')


for i in range(len(data)-2):
# for i in range(2):
    i = i + 2
    n = int(data[i][0])
    R = data[i][1]
    h = data[i][2]
    xH = data[i][3]
    a = data[i][4]
    h3 = data[i][5]
    rho = data[i][6]

    nMesh = 20
    N = 2
    period = 0.01
    nIntervals = period/50
    thickness = 0.5
    Dist = 5
    materialId = 'TPU'
    folderCAE = '_CAE/'
    folderPLOTS = '_PLOTS/'
    step = 'FOLD'

    jobName = str(i) + '-' + step + '-n-' + str(n) + '-h-' + str(int(h*100)) + 'e-2'
    # jobName = 'INF-PRUEBA-PARALLEL-QUAD-TRI-n5-N=2-nM=20' 
    print(jobName)

    import _geo2abq
    import _postProcessing
    # from abaqus import *
    # from abaqusConstants import *
    # Run the main function
    _geo2abq.run(n,R,h, xH, a, h3, rho,jobName,nMesh,period,materialId,N,thickness,folderCAE,step,nIntervals,Dist)
    # _postProcessing.run(jobName,folderPLOTS)