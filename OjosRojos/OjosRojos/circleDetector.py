import numpy as np
class Circle:
    p1 = []
    p2 = []
    p3 = []
    mat = [[],[],[]]
    ds, dc, dd, de = 0,0,0,0
    c,d,e = 0,0,0
    center = []
    radius = 0
    def getDs():
        self.ds = np.linalg.det([[mat[0,0],mat[1,0],mat[2,0]],
                                 [mat[0,1],mat[1,1],mat[2,1]],
                                 [mat[0,2],mat[1,2],mat[2,0]]])
    def getDc():
        self.dc = np.linalg.det([[mat[3,0],mat[1,0],mat[2,0]],
                                 [mat[3,1],mat[1,1],mat[2,1]],
                                 [mat[3,2],mat[1,2],mat[2,0]]])
    def getDd():
        self.dd = np.linalg.det([[mat[0,0],mat[3,0],mat[2,0]],
                                 [mat[0,1],mat[3,1],mat[2,1]],
                                 [mat[0,2],mat[3,2],mat[2,0]]])
    def getDe():
        self.de = np.linalg.det([[mat[0,0],mat[1,0],mat[3,0]],
                                 [mat[0,1],mat[1,1],mat[3,1]],
                                 [mat[0,2],mat[1,2],mat[3,0]]])
    def ti(x,y):
        return (pow(x,2)+pow(y,2))*-1
    def createMat():
        self.mat = [[p1,1,ti(p1[0],p1[1])],[p2,1,ti(p2[0],p2[1])],[p3,ti(p3[0],p3[1])]]
    def calcCenter(z):
        return pow(z,2)/(z*(z/2))
    def getEq():
        self.c = self.dc/self.ds
        self.d = self.dd/self.ds
        self.e = self.de/self.ds
        self.center = [calcCenter(self.c),calcCenter(self.d)]
        self.radius = (-1*self.e)+(self.c/2)+(self.d/2)
    def setCircle():#[x,y] input

        return