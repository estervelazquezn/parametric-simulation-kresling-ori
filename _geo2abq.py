import _kreslingGeometry
import numpy as np
from abaqus import *
from abaqusConstants import *

def run(n,R,h, xH, a, h3, rho,jobName,nMesh,period,materialId,N,thickness,folder,stepName,nIntervals,Dist):
    TPUWidth = 1
    offsetDist = R/10
    i = 1
    NType = np.mod(N,2)

    meshSize = a/nMesh
    backwardCompatibility.setValues(includeDeprecated=True,
                                    reportDeprecated=False)

    # Create a model.
    myModel = mdb.Model(name='Origami')

    # Create a new viewport in which to display the model
    # and the results of the analysis.
    myViewport = session.Viewport(name='Origami Example',
        origin=(20, 20), width=150, height=120)

    #-----------------------------------------------------
    import part

    myModel.rootAssembly.DatumCsysByThreePoints(coordSysType=CARTESIAN, 
        line1=(1.0, 0.0, 0.0), line2=(0.0, 1.0, 0.0), origin= (0,0,0), name='Datum-1')

    # Create a sketch for the base feature
    sketch1 = myModel.ConstrainedSketch(name='OrigamiProfile-'+ str(i),sheetSize=5)

    # Create the triangle
    sketch1.Line(point1=(0,0),point2=(a,0))
    sketch1.Line(point1=(a,0),point2=(xH,h))
    sketch1.Line(point1=(xH,h),point2=(0,0))

    # Create the three-dimensional, deformable parts
    part1 = myModel.Part(name='Origami-' + str(i) , dimensionality=THREE_D, type=DEFORMABLE_BODY)

    # Create the parts as planar shells
    part1.BaseShell(sketch=sketch1)

    part1.projectReferencesOntoSketch(filter=
        COPLANAR_EDGES, sketch=sketch1)

    # Partition by sketch
    myModel.ConstrainedSketch(gridSpacing=4.98, name='Fill', sheetSize=200, transform= part1.MakeSketchTransform(
                              sketchPlane=part1.faces[0], sketchPlaneSide=SIDE1, sketchUpEdge=part1.edges[1], 
                              sketchOrientation=BOTTOM, origin=(20, 20, 0.0)))
    
    part1.projectReferencesOntoSketch(filter=COPLANAR_EDGES, sketch=sketch1)
    sketch1.offset(distance=TPUWidth, objectList=(sketch1.geometry[2], sketch1.geometry[3], sketch1.geometry[4]), side=RIGHT)
    part1.PartitionFaceBySketch(faces=part1.faces.getSequenceFromMask(('[#1 ]', ), ), sketch=sketch1, 
                                sketchOrientation=BOTTOM, sketchUpEdge= part1.edges[1])


    # Partition by sketch
    myModel.ConstrainedSketch(gridSpacing=4.61, name='__profile__', sheetSize=184.73, 
                              transform=part1.MakeSketchTransform(sketchPlane=part1.faces[0], 
                                                                  sketchPlaneSide=SIDE1, sketchUpEdge=part1.edges[1], 
                                                                  sketchOrientation=BOTTOM, origin=(14.616666, 21.074907, 0.0)))
    
    part1.projectReferencesOntoSketch(filter= COPLANAR_EDGES, sketch=myModel.sketches['__profile__'])
    myModel.sketches['__profile__'].offset(distance=a/8, objectList=(myModel.sketches['__profile__'].geometry[2], 
                                                                     myModel.sketches['__profile__'].geometry[3], 
                                                                     myModel.sketches['__profile__'].geometry[4]), side=RIGHT)
    part1.PartitionFaceBySketch(faces= part1.faces.getSequenceFromMask(('[#1 ]', ), ), sketch=myModel.sketches['__profile__'],
                                sketchOrientation=BOTTOM, sketchUpEdge=part1.edges[1])
    
    # Create a sketch for the base 
    sketch2 = myModel.ConstrainedSketch(name='PlateProfile',sheetSize=5)

    # Create the square
    sketch2.Line(point1=(0.0, 0.0), point2=(a, 0.0))
    sketch2.radialPattern(centerPoint=(a/2, np.sqrt(R**2-(a/2)**2)), 
                          geomList=(sketch2.geometry[2],), number=n, totalAngle=360.0, vertexList=())

    # Create the three-dimensional, deformable parts
    part2 = myModel.Part(name='Plate-' + str(i) , dimensionality=THREE_D, type=DEFORMABLE_BODY)

    # Create the parts as planar shells
    part2.BaseShell(sketch=sketch2)
    plateID = part2.edges.getMask('PlateProfile')

    mdb.models['Origami'].ConstrainedSketch(gridSpacing=6.98, name='__profile__', 
        sheetSize=279.36, transform=
        mdb.models['Origami'].parts['Plate-1'].MakeSketchTransform(
        sketchPlane=mdb.models['Origami'].parts['Plate-1'].faces[0], 
        sketchPlaneSide=SIDE1, 
        sketchUpEdge=mdb.models['Origami'].parts['Plate-1'].edges[1], 
        sketchOrientation=BOTTOM, origin=(a/2, np.sqrt(R**2-(a/2)**2),0)))
    mdb.models['Origami'].parts['Plate-1'].projectReferencesOntoSketch(filter=
        COPLANAR_EDGES, sketch=mdb.models['Origami'].sketches['__profile__'])
    mdb.models['Origami'].sketches['__profile__'].CircleByCenterPerimeter(center=(0.0, 0.0), point1=(R*4/6, 0))
    mdb.models['Origami'].parts['Plate-1'].PartitionFaceBySketch(faces=
        mdb.models['Origami'].parts['Plate-1'].faces.getSequenceFromMask(('[#1 ]', 
        ), ), sketch=mdb.models['Origami'].sketches['__profile__'], 
        sketchOrientation=BOTTOM, sketchUpEdge=
        mdb.models['Origami'].parts['Plate-1'].edges[1])

    circleID = part2.edges.getMask('__profile__')
    # myModel.ConstrainedSketch(gridSpacing=6.56, name='__profile__', sheetSize=262.49, transform=
    #                           part2.MakeSketchTransform(sketchPlane=part2.faces[0], 
    #                                                     sketchPlaneSide=SIDE1, 
    #                                                     sketchUpEdge=part2.edges[1], 
    #                                                     sketchOrientation=BOTTOM, origin=(29.389263, 40.45085, 0.0)))
    
    # part2.projectReferencesOntoSketch(filter= COPLANAR_EDGES, sketch=myModel.sketches['__profile__'])
    # offsetList = (myModel.sketches['__profile__'].geometry[2],)
    # for i in range(n-1):
    #     offsetList = offsetList + (myModel.sketches['__profile__'].geometry[i+3],)

    
    # myModel.sketches['__profile__'].offset(distance=offsetDist, objectList=(offsetList), side=RIGHT)
    # part2.PartitionFaceBySketch(faces= part2.faces.getSequenceFromMask(('[#1 ]', ), ), sketch=myModel.sketches['__profile__'], 
    #                             sketchOrientation=BOTTOM, sketchUpEdge=part2.edges[1])
    # del myModel.sketches['__profile__']

    #-----------------------------------------------------
    import material

    # Create a material
    paper = myModel.Material(name='CARD')

    # Create the elastic properties of the paper
    elasticProperties = (3745660000e-6, 0.26)
    paper.Elastic(table=(elasticProperties, ) )

    densityProperties = (802.703e-9, 30)
    paper.Density(table=(densityProperties, ) )


    PLA = myModel.Material(name='PLA')

    # Create the elastic properties of the PLA
    elasticProperties = (2346.5, 0.35)
    PLA.Elastic(table=(elasticProperties, ) )

    densityProperties = (1.24e-9, 30)
    PLA.Density(table=(densityProperties, ) )

    TPU = myModel.Material(name='TPU')

    # Create the elastic properties of the TPU
    elasticProperties = (26, 0.45)
    TPU.Elastic(table=(elasticProperties, ) )

    densityProperties = (1.22e-9, 30)
    TPU.Density(table=(densityProperties, ) )


    STEEL = myModel.Material(name='STEEL')

    # Create the elastic properties of the TPU
    elasticProperties = (210e3, 0.32)
    STEEL.Elastic(table=(elasticProperties, ) )

    densityProperties = (7.85e-06, 30)
    STEEL.Density(table=(densityProperties, ) )

    #-------------------------------------------------------

    import section

    # Create the solid section
    mySection = myModel.HomogeneousShellSection(name='OrigamiSection',
        material='PLA', thickness=thickness)
    mySection2 = myModel.HomogeneousShellSection(name='OrigamiSection-TPU',
        material='TPU', thickness=thickness)
    
    # Assign the section to the region. The region refers
    # to the single cell in this model
    region1 = (part1.faces.getSequenceFromMask(('[#3 ]', ), ),)
    part1.SectionAssignment(region=region1, sectionName='OrigamiSection',offsetType=MIDDLE_SURFACE)

    region3 = (part1.faces.getSequenceFromMask(('[#4 ]', ), ),)
    part1.SectionAssignment(region=region3, sectionName='OrigamiSection-TPU',offsetType=MIDDLE_SURFACE)

    mySection3 = myModel.HomogeneousShellSection(name='PlateSection',
        material='PLA', thickness=thickness)

    # Assign the section to the region. The region refers
    # to the single cell in this model
    region2 = (part2.faces,)
    part2.SectionAssignment(region=region2, sectionName='PlateSection',offsetType=MIDDLE_SURFACE)
    #-------------------------------------------------------

    import assembly

    # Number of odd and pair number of rings (N34 and N12)
    N12 = trunc(N/2)
    if NType > 0:
        N12 = N12 + 1
    N34 = N - N12

    # Create the part instances
    myAssembly = myModel.rootAssembly
    myInstancePlate = myAssembly.Instance(name='Plate', part=part2, dependent=ON)
    myAssembly.rotate(angle=-90, axisDirection=(1.0, 
        0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('Plate',))
    myAssembly.translate(instanceList=('Plate',), vector=( 0, N*h3, 0))

    myInstance1 = myAssembly.Instance(name='OrigamiInstance-1', part=part1, dependent=ON)
    myInstance2 = myAssembly.Instance(name='OrigamiInstance-2', part=part1, dependent=ON)

    # Rotations in order to assembly triangles 1 and 2
    myAssembly.rotate(angle=180, axisDirection=(0.0, 
        1.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('OrigamiInstance-2',))

    myAssembly.rotate(angle=180, axisDirection=(1.0, 
        0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('OrigamiInstance-2',))

    myAssembly.rotate(angle=-(rho), axisDirection=(1.0, 
        0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('OrigamiInstance-1',))

    # Radial pattern for instance 1
    myAssembly.RadialInstancePattern(axis=(0.0, 1.0, 0.0), instanceList=('OrigamiInstance-1', ), 
                                     number=n, point=(a/2,0, -np.sqrt(R**2-(a/2)**2)), totalAngle=360.0)

    # Creation of the plane to ubicate the 2nd instance
    plane = myAssembly.DatumPlaneByThreePoints(isDependent=False, 
        point1=
        myAssembly.instances['OrigamiInstance-1'].vertices[6]
        , point2=
        myAssembly.instances['OrigamiInstance-1'].vertices[8]
        , point3=
        myAssembly.instances['OrigamiInstance-1-rad-2'].vertices[6])
    planeId = myAssembly.features['Datum plane-1'].id

    myAssembly.ParallelFace(fixedPlane= myAssembly.datums[planeId], flip=OFF, 
                            movablePlane= myAssembly.instances['OrigamiInstance-2'].faces[0])

    myAssembly.EdgeToEdge(fixedAxis= myAssembly.instances['OrigamiInstance-1'].edges[8], flip=ON, 
                          movableAxis= myAssembly.instances['OrigamiInstance-2'].edges[8])
    
    myAssembly.CoincidentPoint(fixedPoint= myAssembly.instances['OrigamiInstance-1'].vertices[6], 
                               movablePoint= myAssembly.instances['OrigamiInstance-2'].vertices[8])
    
    # Rodial pattern for the 2nd instance
    myAssembly.RadialInstancePattern(axis=(0.0, 1.0, 0.0), instanceList=('OrigamiInstance-2', ), 
                                     number=n, point=(a/2,0, -np.sqrt(R**2-(a/2)**2)), totalAngle=360.0)

    instanceList12 = ('OrigamiInstance-1','OrigamiInstance-2',)
    for j in range(n-1):
        instanceList12 = instanceList12 + ('OrigamiInstance-1-rad-' + str(j+2), 'OrigamiInstance-2-rad-' + str(j+2))

    # Creation of the instances 3 and 4 if N > 1
    if (NType > 0 and N > 1) or N > 1:
        myInstance3 = myAssembly.Instance(name='OrigamiInstance-3', part=part1, dependent=ON)
        myInstance4 = myAssembly.Instance(name='OrigamiInstance-4', part=part1, dependent=ON)

        # Rotations in order to assembly triangles 3 and 4
        myAssembly.rotate(angle=180, axisDirection=(0.0, 
            1.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('OrigamiInstance-3',))

        myAssembly.rotate(angle=180, axisDirection=(1.0, 
            0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('OrigamiInstance-4',))

        myAssembly.rotate(angle=-rho, axisDirection=(-10.0, 
            0.0, 0.0), axisPoint=(0, 0, 0.0), instanceList=('OrigamiInstance-4', ))
        
        # Radial pattern for intance 4
        myAssembly.RadialInstancePattern(axis=(0.0, 1.0, 0.0), 
            instanceList=('OrigamiInstance-4', ), 
            number=n, point=(a/2,0, -np.sqrt(R**2-(a/2)**2)), 
            totalAngle=360.0)

        # Creation of the plane to ubicate the 3rd instance
        plane2 = myAssembly.DatumPlaneByThreePoints(isDependent=False, 
            point1=
            myAssembly.instances['OrigamiInstance-4'].vertices[6]
            , point2=
            myAssembly.instances['OrigamiInstance-4'].vertices[8]
            , point3=
            myAssembly.instances['OrigamiInstance-4-rad-2'].vertices[6])
        plane2Id = myAssembly.features['Datum plane-2'].id

        myAssembly.ParallelFace(fixedPlane= myAssembly.datums[plane2Id], flip=OFF, 
                                movablePlane= myAssembly.instances['OrigamiInstance-3'].faces[0])

        myAssembly.EdgeToEdge(fixedAxis= myAssembly.instances['OrigamiInstance-4'].edges[8], flip=ON, 
                              movableAxis= myAssembly.instances['OrigamiInstance-3'].edges[8])

        myAssembly.CoincidentPoint(fixedPoint= myAssembly.instances['OrigamiInstance-4'].vertices[6] , 
                                   movablePoint= myAssembly.instances['OrigamiInstance-3'].vertices[8])
        
        # Radial pattern for the 3rd instance
        myAssembly.RadialInstancePattern(axis=(0.0, 1.0, 0.0), instanceList=('OrigamiInstance-3', ),
                                         number=n, point=(a/2,0, -np.sqrt(R**2-(a/2)**2)), totalAngle=360.0)

        instanceList34 = ('OrigamiInstance-3','OrigamiInstance-4',)
        for j in range(n-1):
            instanceList34 = instanceList34 + ('OrigamiInstance-3-rad-' + str(j+2), 'OrigamiInstance-4-rad-' + str(j+2))
            
        myAssembly.translate(instanceList=instanceList34, vector=(0.0, 2*h3, 0.0))

        # Linear patter in the case it is required
        if NType > 0:
            if N >= 3:
                myAssembly.LinearInstancePattern(direction1=(1.0, 0.0, 0.0), direction2=(0.0, 1.0, 0.0), 
                                                 instanceList=(instanceList34), number1=1, number2=N34, 
                                                 spacing1=0, spacing2=2*h3)
            
            myAssembly.LinearInstancePattern(direction1=(1.0, 0.0, 0.0), direction2=(0.0, 1.0, 0.0), 
                                             instanceList=(instanceList12), number1=1, number2=N12, 
                                             spacing1=0, spacing2=2*h3)
            
            # Fix the plate to the top
            myAssembly.EdgeToEdge(fixedAxis= myAssembly.instances['OrigamiInstance-2-rad-2-lin-1-'+str(N12)].edges[4], flip=ON, 
                                  movableAxis= myAssembly.instances['Plate'].edges[2])
            
            myAssembly.EdgeToEdge(fixedAxis= myAssembly.instances['OrigamiInstance-2-lin-1-'+str(N12)].edges[4], flip=ON, 
                                  movableAxis= myAssembly.instances['Plate'].edges[1])
            
        elif NType == 0 and N>2:
            instanceListRING = instanceList12 + instanceList34
            myAssembly.LinearInstancePattern(direction1=(1.0, 0.0, 0.0), direction2=(0.0, 1.0, 0.0), 
                                             instanceList=(instanceListRING), number1=1, number2=(N12+N34)/2, 
                                             spacing1=0, spacing2=2*h3)
    
    # Fix the plate to the top (when N = 1)
    elif N == 1:
        myAssembly.EdgeToEdge(fixedAxis= myAssembly.instances['OrigamiInstance-2-rad-2'].edges[4], flip=ON, 
                              movableAxis= myAssembly.instances['Plate'].edges[2])
        myAssembly.EdgeToEdge(fixedAxis= myAssembly.instances['OrigamiInstance-2'].edges[4], flip=ON, 
                              movableAxis=  myAssembly.instances['Plate'].edges[1])
    #-------------------------------------------------------

    import step
    # Create the steps
    # Folding step
    myModel.ExplicitDynamicsStep(name='OriFolding', previous='Initial',
        timePeriod=period*1, nlgeom=ON, maxIncrement=None)

    myModel.fieldOutputRequests['F-Output-1'].setValues(variables=('S', 'SVAVG', 'PE', 'PEVAVG', 'PEEQ', 'PEEQVAVG', 'LE', 'U', 'V', 
                                           'A', 'RF', 'CSTRESS', 'EVF'),timeInterval=nIntervals*2)
    
    # myModel.fieldOutputRequests(createStepName='OriFolding', name= 'F-Output-2',
    #                             variables=('S', 'SVAVG', 'MISES', 'PE', 'PEVAVG', 'PEEQ', 'PEEQVAVG', 'LE', 'U', 'V', 
    #                                        'A', 'RF', 'CSTRESS', 'EVF'),timeInterval=nIntervals*2)

    mdb.models['Origami'].FieldOutputRequest(createStepName='OriFolding', name=
        'F-Output-2', timeInterval=nIntervals, variables=('MISES', ))
    
    myModel.historyOutputRequests['H-Output-1'].setValues(numIntervals=100)

    # Deployment steps
    if stepName == 'INF':
        myModel.ExplicitDynamicsStep(name='OriBistable', previous='OriFolding',
            timePeriod=period, nlgeom=ON, maxIncrement=None)
        
        myModel.ExplicitDynamicsStep(name='OriInflation', previous='OriBistable',
            timePeriod=period, nlgeom=ON, maxIncrement=None)
    #-------------------------------------------------------

    import interaction
    import connectorBehavior

    # Interaction: Contact between the surfaces
    myModel.ContactProperty('ContactProp')
    myModel.interactionProperties['ContactProp'].TangentialBehavior(formulation=FRICTIONLESS)
    myModel.interactionProperties['ContactProp'].NormalBehavior(allowSeparation=ON, constraintEnforcementMethod=DEFAULT, 
                                                                pressureOverclosure=HARD)
    
    myModel.ContactExp(createStepName='Initial', name='Int-1')
    myModel.interactions['Int-1'].includedPairs.setValuesInStep(stepName='Initial', useAllstar=ON)
    myModel.interactions['Int-1'].contactPropertyAssignments.appendInStep(assignments=((GLOBAL, SELF, 'ContactProp'), ), 
                                                                          stepName='Initial')

    # Interaction: Ties and couplings
    # Initialization of the linear pattern
    lin = ''
    # Tie the number of instances 1 and 2
    for k in range(N12):
        if k >= 1:
            lin0 = lin
            lin = '-lin-1-' + str(k+1)

            # Tie between instances 4 and 1
            myAssembly.Set(edges= myAssembly.instances['OrigamiInstance-4'+lin0].edges.getSequenceFromMask(('[#80 ]', ), ), 
                        name='Ori-'+ str(i+3) + lin0 +'-Edge-1')
            myAssembly.Set(edges= myAssembly.instances['OrigamiInstance-1'+lin].edges.getSequenceFromMask(('[#80 ]', ), ), 
                        name='Ori-'+ str(i) + lin +'-Edge-1')

            myModel.Tie(name='Tie-Ori-' + str(i+3) +lin0 + '-' + str(i) +lin + '-Edge-1',
                        main=myAssembly.sets['Ori-'+ str(i+3) + lin0 +'-Edge-1'],
                        secondary=myAssembly.sets['Ori-'+ str(i) + lin +'-Edge-1'],
                        constraintEnforcement=SURFACE_TO_SURFACE)
            
            for j in range(n-1):
                    myAssembly.Set(edges= myAssembly.instances['OrigamiInstance-4-rad-'+str(j+2)+lin0].edges.getSequenceFromMask(('[#80 ]', ), ), 
                                name='Ori-'+ str(i+3) + '-rad-' + str(j+2) + lin0 + '-Edge-1')
                    myAssembly.Set(edges= myAssembly.instances['OrigamiInstance-1-rad-'+str(j+2)+lin].edges.getSequenceFromMask(('[#80 ]', ), ), 
                                name='Ori-'+ str(i) + '-rad-' + str(j+2) + lin +'-Edge-1')

                    myModel.Tie(name='Tie-Ori-' + str(i+3) + '-rad-'+str(j+2) + lin0 + '-' + str(i+2) + '-rad-'+str(j+2) + lin + '-Edge-1',
                                main=myAssembly.sets['Ori-'+ str(i+3) + '-rad-'+str(j+2) + lin0 + '-Edge-1'],
                                secondary=myAssembly.sets['Ori-'+ str(i) + '-rad-'+str(j+2) + lin + '-Edge-1'],
                                constraintEnforcement=SURFACE_TO_SURFACE)
        if k >= 1:        
            lin = '-lin-1-' + str(k+1)
            
        # Tie between instances 1 and 2 (Diagonal edges)
        myAssembly.Surface(side1Edges= myAssembly.instances['OrigamiInstance-1'+lin].edges.getSequenceFromMask(('[#100 ]', ), ), 
                           name='Ori-'+ str(i) + lin +'-Edge-2')
        myAssembly.Surface(side1Edges= myAssembly.instances['OrigamiInstance-2'+lin].edges.getSequenceFromMask(('[#100 ]', ), ), 
                           name='Ori-'+ str(i+1) + lin + '-Edge-2')

        myModel.Tie(name='Tie-Oris-' + str(i) + '-' + str(i+1) + lin + '-Edge-2',
                    main=myAssembly.surfaces['Ori-'+ str(i) + lin +'-Edge-2'],
                    secondary=myAssembly.surfaces['Ori-'+ str(i+1) + lin +'-Edge-2'],
                    constraintEnforcement= SURFACE_TO_SURFACE)

        for j in range(n-1):
            myAssembly.Surface(side1Edges= myAssembly.instances['OrigamiInstance-1-rad-'+str(j+2)+lin].edges.getSequenceFromMask(('[#100 ]', ), ), 
                        name='Ori-'+ str(i) + '-rad-'+ str(j+2) + lin + '-Edge-2')
            myAssembly.Surface(side1Edges= myAssembly.instances['OrigamiInstance-2-rad-'+str(j+2)+lin].edges.getSequenceFromMask(('[#100 ]', ), ), 
                        name='Ori-'+ str(i+1) + '-rad-'+ str(j+2) + lin + '-Edge-2')

            myModel.Tie(name='Tie-Ori-' + str(i) + '-rad-'+ str(j+2) + '-' + str(i+1) + '-rad-' + str(j+2) + lin +'-Edge-2',
                        main=myAssembly.surfaces['Ori-'+ str(i) + '-rad-'+ str(j+2) + lin + '-Edge-2'],
                        secondary=myAssembly.surfaces['Ori-'+ str(i+1) + '-rad-'+ str(j+2) + lin + '-Edge-2'],
                        constraintEnforcement=SURFACE_TO_SURFACE)

        # Tie between instances 1 and 2 (Vertical edges)
        myAssembly.Surface(side1Edges= myAssembly.instances['OrigamiInstance-2'+lin].edges.getSequenceFromMask(('[#40 ]', ), ), 
                        name='Ori-'+ str(i+1) + lin + '-Edge-3')
        myAssembly.Surface(side1Edges= myAssembly.instances['OrigamiInstance-1-rad-'+str(2)+lin].edges.getSequenceFromMask(('[#40 ]', ), ), 
                        name='Ori-'+ str(i) + '-rad-'+ str(1) + lin + '-Edge-3')

        myModel.Tie(name='Tie-Oris-' + str(i+1) + '-' + str(i) + '-rad-'+ str(1) + lin + '-Edge-3',
                    main=myAssembly.surfaces['Ori-'+ str(i+1) + lin + '-Edge-3'],
                    secondary=myAssembly.surfaces['Ori-'+ str(i) + '-rad-'+ str(1) + lin + '-Edge-3'],
                    constraintEnforcement=SURFACE_TO_SURFACE)

        myAssembly.Surface(side1Edges= myAssembly.instances['OrigamiInstance-1'+lin].edges.getSequenceFromMask(('[#40 ]', ), ), 
                        name='Ori-'+ str(i) + lin + '-Edge-3')
        myAssembly.Surface(side1Edges= myAssembly.instances['OrigamiInstance-2-rad-'+str(n)+lin].edges.getSequenceFromMask(('[#40 ]', ), ), 
                        name='Ori-'+ str(i+1) + '-rad-'+ str(n) + lin + '-Edge-3')

        myModel.Tie(name='Tie-Oris-' + str(i) + '-' + str(i+1) + '-rad-'+ str(n) + lin +'-Edge-3',
                    main= myAssembly.surfaces['Ori-'+ str(i+1) + '-rad-'+ str(n) + lin + '-Edge-3'],
                    secondary=myAssembly.surfaces['Ori-'+ str(i) + lin + '-Edge-3'],
                    constraintEnforcement=SURFACE_TO_SURFACE)

        for j in range(n-2):

            myAssembly.Surface(side1Edges= myAssembly.instances['OrigamiInstance-2-rad-'+str(j+2)+lin].edges.getSequenceFromMask(('[#40 ]', ), ), 
                            name='Ori-'+ str(i+1) + '-rad-'+ str(j+2) + lin  + '-Edge-3')
            myAssembly.Surface(side1Edges= myAssembly.instances['OrigamiInstance-1-rad-'+str(j+3)+lin].edges.getSequenceFromMask(('[#40 ]', ), ), 
                            name='Ori-'+ str(i) + '-rad-'+ str(j+3) + lin + '-Edge-3')

            myModel.Tie(name='Tie-Oris-' + str(i+1) + '-rad-' + str(j+2) + '-' +  str(i) + '-rad-'+ str(j+3) + lin + '-Edge-3',
                        main=myAssembly.surfaces['Ori-'+ str(i+1) + '-rad-'+ str(j+2) + lin + '-Edge-3'],
                        secondary=myAssembly.surfaces['Ori-'+ str(i) + '-rad-'+ str(j+3) + lin + '-Edge-3'],
                        constraintEnforcement=SURFACE_TO_SURFACE)

    # Tie the number of instances 3 and 4
    if N > 1:
        lin = ''
        for k in range(N34):
            if k >= 1:
                lin = '-lin-1-' + str(k+1)
                
            # Tie between instances 2 and 3
            myAssembly.Set(edges= myAssembly.instances['OrigamiInstance-2'+lin].edges.getSequenceFromMask(('[#80 ]', ), ), 
                        name='Ori-'+ str(i+1) + lin +'-Edge-1')
            myAssembly.Set(edges= myAssembly.instances['OrigamiInstance-3'+lin].edges.getSequenceFromMask(('[#80 ]', ), ), 
                        name='Ori-'+ str(i+2) + lin +'-Edge-1')

            myModel.Tie(name='Tie-Ori-' + str(i+1) + '-' + str(i+2) + lin + '-Edge-1',
                        main=myAssembly.sets['Ori-'+ str(i+2) + lin +'-Edge-1'],
                        secondary=myAssembly.sets['Ori-'+ str(i+1) + lin +'-Edge-1'],
                        constraintEnforcement=SURFACE_TO_SURFACE)
            
            for j in range(n-1):
                    myAssembly.Set(edges= myAssembly.instances['OrigamiInstance-2-rad-'+str(j+2)+lin].edges.getSequenceFromMask(('[#80 ]', ), ), 
                                name='Ori-'+ str(i+1) + '-rad-' + str(j+2) + lin + '-Edge-1')
                    myAssembly.Set(edges= myAssembly.instances['OrigamiInstance-3-rad-'+str(j+2)+lin].edges.getSequenceFromMask(('[#80 ]', ), ), 
                                name='Ori-'+ str(i+2) + '-rad-' + str(j+2) + lin +'-Edge-1')

                    if j == (n-2):
                        myModel.Tie(name='Tie-Ori-' + str(i+1) + '-rad-'+str(j+2) + '-' + str(i+2) + '-rad-'+str(j+2) + lin + '-Edge-1',
                                    main=myAssembly.sets['Ori-'+ str(i+2) + '-rad-'+str(j+2) + lin + '-Edge-1'],
                                    secondary=myAssembly.sets['Ori-'+ str(i+1) + '-rad-'+str(j+2) + lin + '-Edge-1'],
                                    constraintEnforcement=SURFACE_TO_SURFACE)
                    else:
                        myModel.Tie(name='Tie-Ori-' + str(i+1) + '-rad-'+str(j+2) + '-' + str(i+2) + '-rad-'+str(j+2) + lin + '-Edge-1',
                                    main=myAssembly.sets['Ori-'+ str(i+1) + '-rad-'+str(j+2) + lin + '-Edge-1'],
                                    secondary=myAssembly.sets['Ori-'+ str(i+2) + '-rad-'+str(j+2) + lin + '-Edge-1'],
                                    constraintEnforcement=SURFACE_TO_SURFACE)

            # Tie between instances 3 and 4 (Diagonal edges)
            myAssembly.Set(edges= myAssembly.instances['OrigamiInstance-4'+lin].edges.getSequenceFromMask(('[#100 ]', ), ), 
                        name='Ori-'+ str(i+3) + lin +'-Edge-2')
            myAssembly.Set(edges= myAssembly.instances['OrigamiInstance-3'+lin].edges.getSequenceFromMask(('[#100 ]', ), ), 
                        name='Ori-'+ str(i+2) + lin +'-Edge-2')

            myModel.Tie(name='Tie-Ori-' + str(i+2) + '-' + str(i+3) + '-Edge-2',
                        main=myAssembly.sets['Ori-'+ str(i+3) + lin +'-Edge-2'],
                        secondary=myAssembly.sets['Ori-'+ str(i+2) + lin +'-Edge-2'],
                        constraintEnforcement=SURFACE_TO_SURFACE)

            for j in range(n-1):
                myAssembly.Surface(side1Edges= myAssembly.instances['OrigamiInstance-4-rad-'+str(j+2)+lin].edges.getSequenceFromMask(('[#100 ]', ), ), 
                            name='Ori-'+ str(i+3) + '-rad-'+ str(j+2) + lin + '-Edge-2')
                myAssembly.Surface(side1Edges= myAssembly.instances['OrigamiInstance-3-rad-'+str(j+2)+lin].edges.getSequenceFromMask(('[#100 ]', ), ), 
                            name='Ori-'+ str(i+2) + '-rad-'+ str(j+2) + lin + '-Edge-2')

                myModel.Tie(name='Tie-Ori-' + str(i+2) + '-rad-'+ str(j+2) + '-' + str(i+3) + '-rad-' + str(j+2) + lin + '-Edge-2',
                            main=myAssembly.surfaces['Ori-'+ str(i+3) + '-rad-'+ str(j+2) + lin + '-Edge-2'],
                            secondary=myAssembly.surfaces['Ori-'+ str(i+2) + '-rad-'+ str(j+2) + lin + '-Edge-2'],
                            constraintEnforcement=SURFACE_TO_SURFACE)


            # Tie between instances 3 and 4 (Vertical edges)
            myAssembly.Surface(side1Edges= myAssembly.instances['OrigamiInstance-3'+lin].edges.getSequenceFromMask(('[#40 ]', ), ), 
                            name='Ori-'+ str(i+2) + lin + '-Edge-3')
            myAssembly.Surface(side1Edges= myAssembly.instances['OrigamiInstance-4-rad-'+str(2)+lin].edges.getSequenceFromMask(('[#40 ]', ), ), 
                            name='Ori-'+ str(i+3) + '-rad-'+ str(2) + lin +'-Edge-3')

            myModel.Tie(name='Tie-Oris-' + str(i+2) + '-' + str(i+3) + '-rad-'+ str(1) + lin +'-Edge-3',
                        main=myAssembly.surfaces['Ori-'+ str(i+2) + lin + '-Edge-3'],
                        secondary=myAssembly.surfaces['Ori-'+ str(i+3) + '-rad-'+ str(2) + lin + '-Edge-3'],
                        constraintEnforcement=SURFACE_TO_SURFACE)


            myAssembly.Surface(side1Edges= myAssembly.instances['OrigamiInstance-4'+lin].edges.getSequenceFromMask(('[#40 ]', ), ), 
                            name='Ori-'+ str(i+3) + lin + '-Edge-3')
            myAssembly.Surface(side1Edges= myAssembly.instances['OrigamiInstance-3-rad-'+str(n)+lin].edges.getSequenceFromMask(('[#40 ]', ), ), 
                            name='Ori-'+ str(i+2) + '-rad-'+ str(n) + lin + '-Edge-3')

            myModel.Tie(name='Tie-Oris-' + str(i+3) + '-' + str(i+2) + '-rad-'+ str(n) + lin +'-Edge-3',
                        main= myAssembly.surfaces['Ori-'+ str(i+3) + lin + '-Edge-3'],
                        secondary= myAssembly.surfaces['Ori-'+ str(i+2) + '-rad-'+ str(n) + lin + '-Edge-3'],
                        constraintEnforcement=SURFACE_TO_SURFACE)

            for j in range(n-2):

                myAssembly.Surface(side1Edges= myAssembly.instances['OrigamiInstance-3-rad-'+str(j+2)+lin].edges.getSequenceFromMask(('[#40 ]', ), ), 
                                name='Ori-'+ str(i+2) + '-rad-'+ str(j+2) + lin + '-Edge-3')
                myAssembly.Surface(side1Edges= myAssembly.instances['OrigamiInstance-4-rad-'+str(j+3)+lin].edges.getSequenceFromMask(('[#40 ]', ), ), 
                                name='Ori-'+ str(i+3) + '-rad-'+ str(j+3) + lin + '-Edge-3')

                myModel.Tie(name='Tie-Oris-' + str(i+2) + '-rad-' + str(j+2) + '-' +  str(i+3) + '-rad-'+ str(j+3) +lin + '-Edge-3',
                            main=myAssembly.surfaces['Ori-'+ str(i+2) + '-rad-'+ str(j+2) + lin + '-Edge-3'],
                            secondary=myAssembly.surfaces['Ori-'+ str(i+3) + '-rad-'+ str(j+3) + lin + '-Edge-3'],
                            constraintEnforcement=SURFACE_TO_SURFACE)


    # Bottom coupling contstraint 
    vertices1 = myAssembly.instances['OrigamiInstance-1'].vertices.getSequenceFromMask(mask=('[#10 ]', ), )
    for j in range(n-1):
        vertices1 = vertices1 + myAssembly.instances['OrigamiInstance-1-rad-'+ str(j+2)].vertices.getSequenceFromMask(mask=('[#10 ]', ), )

    edges1 = myAssembly.instances['OrigamiInstance-1'].edges.getSequenceFromMask(mask=('[#80 ]', ), )
    for j in range(n-1):
        edges1 = edges1 + myAssembly.instances['OrigamiInstance-1-rad-'+ str(j+2)].edges.getSequenceFromMask(mask=('[#80 ]', ), ) 

    myAssembly.Set(name='m_Set-21', vertices=vertices1)
    myAssembly.Set(edges=edges1, name='s_Set-21')
    myModel.Coupling(controlPoint= myAssembly.sets['m_Set-21'], couplingType=KINEMATIC, 
                     influenceRadius=WHOLE_SURFACE, localCsys=None, name='Constraint-23', 
                     surface=myAssembly.sets['s_Set-21'], u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)
    
    # Top coupling contstraint 
    # Odd number of rings (N value)
    if NType > 0:
        if N12 > 1:
            lin = '-lin-1-' + str(N12)
        else:
            lin = ''

        vertices2 = myAssembly.instances['OrigamiInstance-2'+lin].vertices.getSequenceFromMask(mask=('[#30 ]', ), ) 
        edges2 = myAssembly.instances['OrigamiInstance-2'+lin].edges.getSequenceFromMask(mask=('[#80 ]', ), )

        myAssembly.Set(name='m_Set-23-', vertices=vertices2)
        myAssembly.Set(edges=edges2, name='s_Set-23-')
        myModel.Coupling(controlPoint=myAssembly.sets['m_Set-23-'], couplingType=KINEMATIC, 
                         influenceRadius=WHOLE_SURFACE, localCsys=None, name='Constraint-24-', 
                         surface=myAssembly.sets['s_Set-23-'], u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)
      
        for j in range(n-1):
            vertices2 = myAssembly.instances['OrigamiInstance-2-rad-'+ str(j+2)+ lin].vertices.getSequenceFromMask(mask=('[#30 ]', ), )
            edges2 = myAssembly.instances['OrigamiInstance-2-rad-'+ str(j+2)+ lin].edges.getSequenceFromMask(mask=('[#80 ]', ), )

            myAssembly.Set(name='m_Set-23-'+str(j), vertices=vertices2)
            myAssembly.Set(edges=edges2, name='s_Set-23-'+str(j))
            myModel.Coupling(controlPoint= myAssembly.sets['m_Set-23-'+str(j)], couplingType=KINEMATIC, 
                             influenceRadius=WHOLE_SURFACE, localCsys=None, name='Constraint-24-'+str(j), 
                             surface=myAssembly.sets['s_Set-23-'+str(j)], u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)
            
        edgesPlate = myAssembly.instances['OrigamiInstance-2'+lin].edges.getSequenceFromMask(mask=('[#80 ]', ), )
        for j in range(n-1):
            edgesPlate = edgesPlate + myAssembly.instances['OrigamiInstance-2-rad-'+ str(j+2)+ lin].edges.getSequenceFromMask(mask=('[#80 ]', ), )

    # Pair number of rings (N value)
    elif NType == 0:
        if N34 > 1:
            lin = '-lin-1-' + str(N34)
        else:
            lin = ''

        # Definition of the regions for the coupling
        vertices2 = myAssembly.instances['OrigamiInstance-4'+lin].vertices.getSequenceFromMask(mask=('[#30 ]', ), ) 
        edges2 = myAssembly.instances['OrigamiInstance-4'+lin].edges.getSequenceFromMask(mask=('[#80 ]', ), )

        myAssembly.Set(name='m_Set-23-', vertices=vertices2)
        myAssembly.Set(edges=edges2, name='s_Set-23-')
        myModel.Coupling(controlPoint= myAssembly.sets['m_Set-23-'], couplingType=KINEMATIC, influenceRadius=WHOLE_SURFACE, 
                         localCsys=None, name='Constraint-24-', surface=myAssembly.sets['s_Set-23-'], u1=ON, u2=ON, 
                         u3=ON, ur1=ON, ur2=ON, ur3=ON)
      
        for j in range(n-1):
            vertices2 = myAssembly.instances['OrigamiInstance-4-rad-'+ str(j+2)+ lin].vertices.getSequenceFromMask(mask=('[#30 ]', ), )
            edges2 = myAssembly.instances['OrigamiInstance-4-rad-'+ str(j+2)+ lin].edges.getSequenceFromMask(mask=('[#80 ]', ), )

            myAssembly.Set(name='m_Set-23-'+str(j), vertices=vertices2)
            myAssembly.Set(edges=edges2, name='s_Set-23-'+str(j))
            myModel.Coupling(controlPoint= myAssembly.sets['m_Set-23-'+str(j)], couplingType=KINEMATIC, 
                             influenceRadius=WHOLE_SURFACE, localCsys=None, name='Constraint-24-'+str(j), 
                             surface=myAssembly.sets['s_Set-23-'+str(j)], u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)
        
        # Definition of the tied Plate region 
        edgesPlate = myAssembly.instances['OrigamiInstance-4'+lin].edges.getSequenceFromMask(mask=('[#80 ]', ), )
        for j in range(n-1):
            edgesPlate = edgesPlate + myAssembly.instances['OrigamiInstance-4-rad-'+ str(j+2)+ lin].edges.getSequenceFromMask(mask=('[#80 ]', ), )


    # Tie Plate with the top region
    # myAssembly.Surface(name='m_Surf-32', side2Faces=myAssembly.instances['Plate'].faces.getSequenceFromMask(('[#3 ]', ), ))
    myAssembly.Surface(name='m_Surf-32', side1Edges=myAssembly.instances['Plate'].edges.getSequenceFromMask(plateID))
    myAssembly.Surface(name='s_Surf-32', side1Edges=edgesPlate)

    myModel.Tie(adjust=ON, main= myAssembly.surfaces['m_Surf-32'], name='Constraint-25', positionToleranceMethod=COMPUTED, 
                secondary= myAssembly.surfaces['s_Surf-32'], thickness=ON, tieRotations=ON)

    
    #-------------------------------------------------------

    import load

    # Define the amplitude
    amp1 = myModel.SmoothStepAmplitude(name='Amp-2',data=((0,0),(period,1)),timeSpan=STEP)
    amp3 = myModel.SmoothStepAmplitude(name='Amp-3',data=((0,0),(period,1)),timeSpan=STEP)
    amp2 = myModel.TabularAmplitude(name='Amp-1',data=((0,0),(period,1)),timeSpan=STEP)

    # Pinned region definition
    pinned = myAssembly.instances['OrigamiInstance-1'].edges.getSequenceFromMask(mask=('[#80 ]', ), )
    for j in range(n-1):
        pinned = (pinned, myAssembly.instances['OrigamiInstance-1-rad-'+str(j+2)].edges.getSequenceFromMask(mask=('[#80 ]', ), ))
        
    pinnedRegion = (pinned,)
    myModel.PinnedBC(name='Pinned',createStepName='OriFolding',region=pinnedRegion)

    ## -----------------------------FOLDING PROCESS ----------------------------------------------
    # Create a displacement
    forceSurface = myAssembly.instances['Plate'].faces.getSequenceFromMask(('[#3 ]', ), )
    forceRegion = ((forceSurface,) )

    disp = -(N*h3 - thickness*10*N)
    myModel.DisplacementBC(name='Disp-1', createStepName='OriFolding',region=forceRegion, 
                           u1=0, u2=disp, u3=0, ur1=0, ur2=0, ur3=0, amplitude='Amp-2')

    # # Create a concentrated force
    # force = 200 # Newtons
    # myModel.DisplacementBC(name='Disp-1', createStepName='OriFolding',region=forceRegion, 
    #                        u1=0, u3=0, ur1=0, ur2=0, ur3=0, amplitude='Amp-1')
    # myModel.ConcentratedForce(name='Force-1', createStepName='OriFolding',region=forceRegion, 
    #                        cf2=-force, amplitude='Amp-1')

    ## -----------------------------INFLATION PROCESS ----------------------------------------------
    if stepName == 'INF':
        # Deactivation of the displacement in both deployment steps
        myModel.boundaryConditions['Disp-1'].deactivate('OriBistable')
        myModel.boundaryConditions['Disp-1'].deactivate('OriInflation')

        # Pressure definition
        pressure = 0.005
        # pressure = 0
        myAssembly.Surface(name='Plate-surf', side2Faces=
                                    myAssembly.instances['Plate'].faces.getSequenceFromMask(('[#3 ]', ), ))
        myModel.Pressure(amplitude='Amp-3', createStepName='OriInflation', 
                    distributionType=UNIFORM, field='', magnitude=pressure, name='INF-Plate', region=
                    myAssembly.surfaces['Plate-surf'])
        
        pair_surf = (myAssembly.instances['OrigamiInstance-3'].faces.getSequenceFromMask(mask=('[#7 ]', ), ) +
                    myAssembly.instances['OrigamiInstance-4'].faces.getSequenceFromMask(mask=('[#7 ]', ), )) 
        for j in range(n-1):
            pair_surf = (pair_surf + myAssembly.instances['OrigamiInstance-3-rad-'+str(j+2)].faces.getSequenceFromMask(mask=('[#7 ]', ), ) +
                    myAssembly.instances['OrigamiInstance-4-rad-'+str(j+2)].faces.getSequenceFromMask(mask=('[#7 ]', ), )) 
        myAssembly.Surface(name='Ori34-surf', side2Faces= pair_surf)
        
        myModel.Pressure(amplitude='Amp-3', createStepName='OriInflation', 
                        distributionType=UNIFORM, field='', magnitude=-pressure, name='INF-Ori34', region=
                        myAssembly.surfaces['Ori34-surf'])
        
        pair_surf = (myAssembly.instances['OrigamiInstance-1'].faces.getSequenceFromMask(mask=('[#7 ]', ), ) +
                    myAssembly.instances['OrigamiInstance-2'].faces.getSequenceFromMask(mask=('[#7 ]', ), )) 
        for j in range(n-1):
            pair_surf = (pair_surf + myAssembly.instances['OrigamiInstance-1-rad-'+str(j+2)].faces.getSequenceFromMask(mask=('[#7 ]', ), ) +
                    myAssembly.instances['OrigamiInstance-2-rad-'+str(j+2)].faces.getSequenceFromMask(mask=('[#7 ]', ), )) 
        myAssembly.Surface(name='Ori12-surf', side1Faces= pair_surf)
        
        myModel.Pressure(amplitude='Amp-3', createStepName='OriInflation', 
                        distributionType=UNIFORM, field='', magnitude=-pressure, name='INF-Ori12', region=
                        myAssembly.surfaces['Ori12-surf'])
        



    #-------------------------------------------------------

    import mesh

    # Assign an element type to the part instance (ORI)
    elemType = mesh.ElemType(elemCode=S3R, elemLibrary=EXPLICIT,secondOrderAccuracy=ON)

    region1 = (myInstance1.faces,)
    part1.setElementType(regions=region1, elemTypes=(elemType,))
    part1.setMeshControls(regions=part1.faces.getSequenceFromMask(('[#3 ]', ), ), elemShape=QUAD_DOMINATED)

    # Part seed by edges
    part1.seedEdgeByBias(biasMethod=DOUBLE, constraint=FINER, endEdges=part1.edges.getSequenceFromMask(('[#1c0 ]', ), ), 
                         minSize=TPUWidth*0.3, maxSize=TPUWidth*1.5)
    part1.seedEdgeByBias(biasMethod=DOUBLE, constraint=FINER, endEdges=part1.edges.getSequenceFromMask(('[#38 ]', ), ), 
                         minSize=TPUWidth*0.5, maxSize=meshSize)
    part1.seedEdgeByBias(biasMethod=DOUBLE, constraint=FINER, endEdges=part1.edges.getSequenceFromMask(('[#7 ]', ), ), 
                         minSize=meshSize, maxSize=meshSize*3.5)
    
    # Mesh the part instance
    part1.generateMesh(regions=(myInstance1,))

    # Assign an element type to the part instance (PLATE)
    elemType2 = mesh.ElemType(elemCode=S3R, elemLibrary=EXPLICIT,secondOrderAccuracy=ON)

    region2 = (myInstancePlate.faces,)
    part2.setElementType(regions=region2, elemTypes=(elemType2,))
    part2.setMeshControls(regions=part2.faces.getSequenceFromMask(('[#3 ]', ), ), elemShape=QUAD_DOMINATED)

    # Part seed by edges
    # part2.seedEdgeByBias(biasMethod=DOUBLE, constraint=FINER, endEdges=part2.edges.getSequenceFromMask(('[#1ff  ]', ), ), 
    #                      minSize=meshSize*0.4, maxSize=meshSize*1)
    # part2.seedEdgeByBias(biasMethod=DOUBLE, constraint=FINER, endEdges=part2.edges.getSequenceFromMask(('[#1ff ]', ), ), 
    #                      minSize=meshSize*6, maxSize=meshSize*10)
    # part2.seedEdgeBySize(constraint=FINER, edges= part2.edges.findAt((0,R*2/3,h3*N)), size=10.0)
    # part2.edges.getSequenceFromMask(plateID)
    part2.seedEdgeBySize(constraint=FINER, edges= part2.edges.getSequenceFromMask(circleID), size=meshSize*5)
    part2.seedEdgeByBias(biasMethod=DOUBLE, constraint=FINER, endEdges=part2.edges.getSequenceFromMask(plateID), 
                         minSize=TPUWidth*0.3, maxSize=TPUWidth*1.5)
        # mdb.models['Origami'].parts['Plate-1'].edges.getSequenceFromMask(('[#100000 ]', ), ), size=10.0)

    # part2.seedPart(size=TPUWidth*0.3)
    # Mesh the part instance
    part2.generateMesh(regions=(myInstancePlate,))

    # part1.Set(name='Set-1', nodes= part1.nodes.getSequenceFromMask(mask=('[#20000 ]', ), ))

    # Display the meshed Origami
    myViewport.assemblyDisplay.setValues(mesh=ON)
    myViewport.assemblyDisplay.meshOptions.setValues(meshTechnique=ON)
    myViewport.setValues(displayedObject=myAssembly)

    #-------------------------------------------------------

    import job

    # Create an analysis job for the model and submit it
    myJob = mdb.Job(name=jobName, model='Origami')#,numCpus=2,multiprocessingMode=MPI,numDomains=2,activateLoadBalancing=ON)

    # Wait for the job to complete
    # myJob.submit()
    # myJob.waitForCompletion()
    mdb.saveAs(folder + jobName)


