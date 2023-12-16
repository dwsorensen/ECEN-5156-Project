import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def rotationMatrix(theta):
    thetarad = np.deg2rad(theta)
    M = np.zeros((4,4))
    M[0,0] = 1
    M[1,1] = np.cos(2*thetarad)
    M[1,2] = np.sin(2*thetarad)
    M[2,1] = -1 * np.sin(2*thetarad)
    M[2,2] = np.cos(2*thetarad)
    M[3,3] = 1
    return M

def linPolarizer_notRotated(re):
    M = np.zeros((4,4))
    M[0,0] = re + 1
    M[0,1] = re - 1
    M[1,0] = re - 1
    M[1,1] = re + 1
    M[2,2] = 2 * np.sqrt(re)
    M[3,3] = 2 * np.sqrt(re)
    M = (1 / (2 * re)) * M
    return M

def linPolarizer(re, theta):
    M = np.matmul(linPolarizer_notRotated(re),rotationMatrix(theta))
    M = np.matmul(rotationMatrix(-1*theta),M)
    return M

def rhcPolarizer(re):
    M = np.zeros((4,4))
    M[0,0] = 1 + re
    M[0,3] = re - 1
    M[1,1] = 2 * np.sqrt(re)
    M[2,2] = 2 * np.sqrt(re)
    M[3,0] = re - 1
    M[3,3] = re + 1
    M = (1 / (2 * re)) * M
    return M

def lhcPolarizer(re):
    M = np.zeros((4,4))
    M[0,0] = 1 + re
    M[0,3] = 1 - re
    M[1,1] = 2 * np.sqrt(re)
    M[2,2] = 2 * np.sqrt(re)
    M[3,0] = 1 - re
    M[3,3] = re + 1
    M = (1 / (2 * re)) * M
    return M

def polToCart(theta,phi):
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    return (x,y,z)

def plotPoincare(stokes,ax,arrow=True):

    #Draw wireframe sphere for display
    res = 100
    theta = np.linspace(0,np.pi,2*res)
    phi = np.linspace(0,2*np.pi,2*res)

    #Sphere surface
    phimesh,thetamesh = np.meshgrid(phi,theta)
    xs = np.sin(thetamesh) * np.cos(phimesh)
    ys = np.sin(thetamesh) * np.sin(phimesh)
    zs = np.cos(thetamesh)

    zeros = np.full(np.shape(phi),0)
    pis = np.full(np.shape(phi),np.pi)
    (x1,y1,z1) = polToCart(pis/2,phi)
    (x2,y2,z2) = polToCart(theta,zeros)
    (x3,y3,z3) = polToCart(theta,pis/2)
    (x4,y4,z4) = polToCart(theta,pis)
    (x5,y5,z5) = polToCart(theta,3*pis/2)

    ax.plot(x1,y1,z1,'black',linestyle="dashed")
    ax.plot(x2,y2,z2,'black')
    ax.plot(x3,y3,z3,'black')
    ax.plot(x4,y4,z4,'black')
    ax.plot(x5,y5,z5,'black')
    if np.shape(stokes) == (4,):
        stokes = (stokes,) #Genius move right here
    for s in stokes:
        #Normalize the vector
        s[1] = s[1] / s[0]
        s[2] = s[2] / s[0]
        s[3] = s[3] / s[0]
        ax.scatter(s[1],s[2],s[3],color='b',marker="X")
        if arrow:
            ax.quiver(0, 0, 0, s[1], s[2], s[3], length=1.0, color='b', arrow_length_ratio=0.1)
    ax.plot_wireframe(xs, ys, zs, color='black', alpha=0.05)
    ax.set_box_aspect([1,1,1])
    ax.quiver(0,0,0, 1,0,0,length=1.1,color='black',linestyle="dashed",arrow_length_ratio=0.05)
    ax.quiver(0,0,0, 0,1,0,length=1.1,color='black',linestyle="dashed",arrow_length_ratio=0.05)
    ax.quiver(0,0,0, 0,0,1,length=1.1,color='black',linestyle="dashed",arrow_length_ratio=0.05)
    
    ax.grid(False)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])

    return ax

if __name__ == "__main__":
    reconstructedVectors = np.loadtxt("reconstructedVectors.csv",delimiter=',')
    fig = plt.figure()
    ax1 = fig.add_subplot(121,projection='3d')
    ax2 = fig.add_subplot(122,projection='3d')
    plotPoincare([np.sqrt(3),-1,-1,1],ax1)
    plotPoincare(reconstructedVectors,ax2,arrow=True)
    plt.show()
    input("Press <enter> to close")