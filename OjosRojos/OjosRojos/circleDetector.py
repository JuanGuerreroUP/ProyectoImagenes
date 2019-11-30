import numpy as np
class Circle:
    p1 = []
    p2 = []
    p3 = []
    center = []
    radius = 0
    def __init__(self, _p1): #Constructor
        self.p1 = _p1
        self.mat = [[],[],[]]
        self.ds, self.dc, self.dd, self.de = 0,0,0,0
        self.c,self.d,self.e = 0,0,0
    #Funciones que dan solucion a un sistema de ecuaciones con 3 incogintas a partir de la regla de Cramer
    def getDs(self):
        self.ds = np.linalg.det([ [self.mat[0][0],self.mat[0][1],self.mat[0][2]],
                                  [self.mat[1][0],self.mat[1][1],self.mat[1][2]],
                                  [self.mat[2][0],self.mat[2][1],self.mat[2][2]] ])
    def getDc(self):
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
        #Funcion que defina la eucación de una circunferencia a partir de 3 puntos. Ejemplo del metodo utilizado: https://www.youtube.com/watch?v=gkQUyBf2VC8 
        self.createMat()
        self.getDs()
        self.getDc()
        self.getDd()
        self.getDe()
        self.c = self.dc/(2*self.ds) #completa el cuadrado
        self.d = self.dd/(2*self.ds) #completa el cuadrado
        self.e = self.de/self.ds 
        self.center = [int(self.c*-1),int(self.d*-1)]
        self.radius = int(pow((-1*self.e)+pow(self.c,2)+pow(self.d,2),0.5))