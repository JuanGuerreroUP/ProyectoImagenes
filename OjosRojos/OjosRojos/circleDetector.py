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
    def getDs(self):
        self.ds = np.linalg.det([ [self.mat[0][0],self.mat[0][1],self.mat[0][2]],
                                  [self.mat[1][0],self.mat[1][1],self.mat[1][2]],
                                  [self.mat[2][0],self.mat[2][1],self.mat[2][2]] ])
    def getDc(self):
        #print(self.mat)
        self.dc = np.linalg.det([ [self.mat[0][3],self.mat[0][1],self.mat[0][2]],
                                  [self.mat[1][3],self.mat[1][1],self.mat[1][2]],
                                  [self.mat[2][3],self.mat[2][1],self.mat[2][2]] ])
    def getDd(self):
        self.dd = np.linalg.det([ [self.mat[0][0],self.mat[0][3],self.mat[0][2]],
                                  [self.mat[1][0],self.mat[1][3],self.mat[1][2]],
                                  [self.mat[2][0],self.mat[2][3],self.mat[2][2]] ])
    def getDe(self):
        self.de = np.linalg.det([ [self.mat[0][0],self.mat[0][1],self.mat[0][3]],
                                  [self.mat[1][0],self.mat[1][1],self.mat[1][3]],
                                  [self.mat[2][0],self.mat[2][1],self.mat[2][3]] ])
    def ti(self,x,y):
        return (pow(x,2)+pow(y,2))*-1
    def createMat(self):
        self.mat = [[self.p1[0],self.p1[1],1,self.ti(self.p1[0],self.p1[1])],[self.p2[0], self.p2[1],1,self.ti(self.p2[0],self.p2[1])],[self.p3[0], self.p3[1], 1,self.ti(self.p3[0],self.p3[1])]]
    def calcCenter(self,z):
        return pow(z/2,2)
    def getEq(self):
        self.createMat()
        self.getDs()
        self.getDc()
        self.getDd()
        self.getDe()
        self.c = self.dc/(2*self.ds)
        self.d = self.dd/(2*self.ds)
        self.e = self.de/self.ds
        self.center = [int(self.c*-1),int(self.d*-1)]
        self.radius = int(pow((-1*self.e)+pow(self.c,2)+pow(self.d,2),0.5))
#    def setCircle(_p1, _p2, _p3):#[x,y] input