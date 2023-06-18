""""
Kresling Geometry generation
------------------------------------------------------
 Generates the parameters needed to generate the Kresling pattern
    
    - INPUTS: structure named 'geoInputs' where
                n = geoInputs['n'] - Number of polygon sides
                h = geoInputs['h'] - Flat pattern height
                R = geoInputs['R'] - Polygon inscribed radius
              
    - OUTPUTS: structure named 'geoOutputs' where
                'n': n - Number of polygon sides
                'h': h - Flat pattern height
                'R': R - Polygon inscribed radius
                'xH': xH - x axis projection of the 3D height 
                'a': a - side lenght
                'h3': h3 - 3D height for stable configuration
                'delta': delta - angle between XY plane and h3 vector

"""
import numpy as np
import mpmath as mp
from _newton import newton

def Geometry(geoInputs):

    n = geoInputs['n']
    h = geoInputs['h']
    R = geoInputs['R']

    # Angles given by the parallelogram
    phi = 360/(n)
    phi2 = phi/2
    eta = 180 - (360/(2*n) + 90)

    # Parallelogram side
    a = 2*R*np.sin(np.deg2rad(phi2))

    # Newton variable initialization
    init = R/4
    # Definition of the flat pattern
    p = lambda d: d*(d*1/mp.tan(np.deg2rad(phi2)) + (a**2 - d**2)**(0.5)) - a*h
    Dp = lambda d: -d**2/(a**2-d**2)**0.5 + (a**2 - d**2)**0.5 + 2*d/mp.tan(np.deg2rad(phi2))
    dsol = np.double(newton(p,Dp,init,1e-8,100000))


    # Angles of the flat pattern
    beta = np.rad2deg(np.arcsin(dsol/a))
    theta = 90 - phi2 - beta

    # Flat triangle definition
    b = h/np.cos(np.deg2rad(theta))
    c = h/np.sin(np.deg2rad(beta))
    xH = -h*np.tan(np.deg2rad(theta))

    # 3D sketch definition
    p1 = lambda heq: mp.asin((c**2-heq**2)**(0.5)/2/R) - mp.asin((b**2-heq**2)**(0.5)/2/R) - mp.pi/n 
    dp1 = lambda heq: 0.5*heq/(R*(b**2-heq**2)**0.5*(1-(b**2-heq**2)/4/R**2)**0.5) \
                      - 0.5*heq/(R*(c**2-heq**2)**0.5*(1-(c**2-heq**2)/4/R**2)**0.5)
    h3 = np.double(newton(p1,dp1,h,1e-8,100000))
    

    # Projections in the horizontal plane
    b1 = np.sqrt(np.power(b,2) - np.power(h3,2))
    alpha = 2*np.rad2deg(np.arcsin(b1/(2*R)))
    c1 = 2*R*np.sin(np.deg2rad((alpha + phi)/2))
    d3 = np.sqrt(np.power(h3,2) + np.power(c1,2))

    # Angle between the horizontal plane and the flat pattern
    delta = 90 - np.rad2deg(np.arcsin(h3/h))

    # Print the values to check its performance
    # print("a = " + str(a))
    # print("xH = " + str(xH))
    # print("Delta = " + str(delta))
    # print("h3 = " + str(h3))

    # Outputs generation
    geoOutputs = {
    'n': n, 'h': h, 'R': R,
    'xH': xH, 'a': a, 'h3': h3, 'delta': delta,
    }

    return(geoOutputs)
