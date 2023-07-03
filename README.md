# Parametric analysis and Optimization of Kresling Origami structures

This code has been based on the willing to develope a tool for designing and optimization a Kresling origami pattern by structural simualtions based in Abaqus CAE. Simulations has been launched from python scrpting thanks to `abqpy` library https://github.com/haiiliin/abqpy. Whereas optimization has been made using free software Dakota Sandia https://dakota.sandia.gov/ and the surrogate model was developed thanks to `smt` library https://github.com/SMTorg/smt.

Implemented code is listed by order and explained as follows:
- 
- ___LHSampling__: Code which generates the LH sampling from a given array of number of sides desired to be sampled. Showing the limits and the result sampled. Output: txt file named "_sampling_data.txt"
- _LHS2geo: Generates the geometry from the samples obtained and calculus the parameters required to launch the simulation. This codes can be runned without the previous sampled, here it can be imposed the n and R values as well as the number of samples desired. Output: txt file named "_kresling_data.txt"
- _runAbq: Launch Abaqus CAE, generates the model using 'geo2abq' with the parameters obtained from "_kresling_data.txt"
- _geo2abq: creates the model in Abaqus CAE with its own sintaxis and run the simulation.
- _kreslingGeometry: Solve the mathematical equations that model the Kresling geometry.
- _newton: Newton model for solving the equation required.
