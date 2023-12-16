import phidl.geometry as pg
from phidl import quickplot as qp, Device, Path
import numpy as np
import matplotlib.pyplot as plt

from make_quadarray import makeWireGrid

def makeSpiral(sideLength,numTurns,wireWidth,chirality):
    res = 100

    totalRes = int(numTurns * res)
    theta = np.linspace(0,2*numTurns*np.pi,totalRes)
    thetaMax = np.max(theta)
    rSlope = chirality *(sideLength/2 - 1.5*wireWidth)/thetaMax
    r = rSlope * theta

    x = r * np.cos(theta)
    y = r * np.sin(theta)

    points = np.zeros((totalRes,2))
    points[:,0] = x
    points[:,1] = y
    
    P = Path(points)
    D = P.extrude(wireWidth)
    return D
    

if __name__ == "__main__":
    sideLength = 200
    D1 = makeWireGrid(0,10,5,sideLength)
    D2 = makeWireGrid(45,10,5,sideLength)
    D3 = makeWireGrid(90,10,5,sideLength)
    D4 = makeWireGrid(135,10,5,sideLength)
    D5 = makeSpiral(200,10,5,1)
    D6 = makeSpiral(200,10,5,-1)

    R = pg.rectangle(size = (sideLength/2,sideLength/2),layer=-1)
    R.move(-1*R.center)

    D = Device()
    r = D.add_ref(D1)
    r.move((-1*sideLength,0.5*sideLength))
    r = D.add_ref(D2)
    r.move((0,0.5*sideLength))
    r = D.add_ref(D3)
    r.move((1*sideLength,0.5*sideLength))
    r = D.add_ref(D4)
    r.move((-1*sideLength,-0.5*sideLength))
    r = D.add_ref(D5)
    r.move((0,-0.5*sideLength))
    r = D.add_ref(D6)
    r.move((1*sideLength,-0.5*sideLength))

    r = D.add_ref(R)
    r.move((-1*sideLength,0.5*sideLength))
    r = D.add_ref(R)
    r.move((0,0.5*sideLength))
    r = D.add_ref(R)
    r.move((1*sideLength,0.5*sideLength))
    r = D.add_ref(R)
    r.move((-1*sideLength,-0.5*sideLength))
    r = D.add_ref(R)
    r.move((0,-0.5*sideLength))
    r = D.add_ref(R)
    r.move((1*sideLength,-0.5*sideLength))

    qp(D)
    input("Press <Enter> to close")
