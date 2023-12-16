import phidl.geometry as pg
from phidl import quickplot as qp, Device, Path
import numpy as np
import matplotlib.pyplot as plt

def makeWireGrid(angle, wirePitch,wireWidth, sideLength):
    D = Device()
    R = pg.rectangle(size = (wireWidth,sideLength*2))
    numWires = int(np.floor(2* sideLength / wirePitch))
    for i in range(numWires):
        ref = D.add_ref(R)
        ref.move((i*wirePitch,0))
    D.move(-1*D.center)
    D.rotate(angle)
    square = pg.rectangle(size=(sideLength,sideLength))
    square.move(-1*square.center)
    A = pg.boolean(A = D, B = square,operation='and')
    return A

if __name__ == "__main__":
    sideLength = 200
    D1 = makeWireGrid(0,10,5,sideLength)
    D2 = makeWireGrid(45,10,5,sideLength)
    D3 = makeWireGrid(90,10,5,sideLength)
    D4 = makeWireGrid(135,10,5,sideLength)

    R = pg.rectangle(size = (sideLength/2,sideLength/2),layer=-1)
    R.move(-1*R.center)

    D = Device()
    r = D.add_ref(D1)
    r.move((-1*sideLength/2,sideLength/2))
    r = D.add_ref(D2)
    r.move((sideLength/2,sideLength/2))
    r = D.add_ref(D3)
    r.move((sideLength/2,-1*sideLength/2))
    r = D.add_ref(D4)
    r.move((-1*sideLength/2,-1*sideLength/2))

    r = D.add_ref(R)
    r.move((-1*sideLength/2,sideLength/2))
    r = D.add_ref(R)
    r.move((sideLength/2,sideLength/2))
    r = D.add_ref(R)
    r.move((sideLength/2,-1*sideLength/2))
    r = D.add_ref(R)
    r.move((-1*sideLength/2,-1*sideLength/2))

    qp(D)
    input("Press <enter> to close")
