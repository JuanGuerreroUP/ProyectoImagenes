import cv2
import numpy as np
import random
from circleDetector import Circle


#functions
def gamma(img, gamma):
    invGamma = 1/gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(img, table)

def circunferencia(x,h,k,r):
    return int(pow(pow(r,2)-pow(x-h,2),0.5)+k)
#end of functions


img = cv2.imread("red-eye2.jpg")

tamanio = np.shape(img) #[y,x]
if(tamanio[0] > 800):
    img = cv2.resize(img, (800, int(tamanio[0]*800/tamanio[1])))
    tamanio = np.shape(img)
if(tamanio[1] > 800):
    img = cv2.resize(img, (int(tamanio[1]*800/tamanio[0])),800)
    tamanio = np.shape(img)

print("y: ",tamanio[0])
print("x: ",tamanio[1])

#BGR
imgChannels = [img[:,:,0], img[:,:,1], img[:,:,2]]


imgChannels[2] = gamma(imgChannels[2],0.8) #se aplica función gamma en el canal R (de BGR)

imgMerged = cv2.merge(imgChannels) #se concatenan los tres canales con gamma en canal R

imgGauss = cv2.GaussianBlur(imgMerged,(9,9),5) #se hace un blur a la imagen


cv2.namedWindow("orignial", cv2.WINDOW_NORMAL)  
cv2.imshow("orignial",img)

cv2.namedWindow("gamma", cv2.WINDOW_NORMAL) 
cv2.imshow("gamma",imgMerged)
cv2.imshow("gamma-gauss",imgGauss)
imgHSV = cv2.cvtColor(imgGauss, cv2.COLOR_BGR2HSV)
print(np.max(imgHSV[:,:,2]))

print("H max:", np.max(imgHSV[:,:,0]))
imgReds = (imgHSV[:,:,0] <= 5) & (imgHSV[:,:,1] > 80) & (imgHSV[:,:,2] > 60)
imgPinks = (imgHSV[:,:,0] >= 120) & (imgHSV[:,:,1] > 80) & (imgHSV[:,:,2] > 60)
imgReds = imgReds + imgPinks




itera = 0
imgEdges = cv2.Canny(imgReds.astype(np.uint8)*255, 100,100);#edge detection, cambiar a detector de sobel
imgEdgesCenters = np.zeros((tamanio[0],tamanio[1]),int).astype(np.uint8)
justCircles = np.zeros((tamanio[0],tamanio[1]),int).astype(np.uint8)
justCirclesArea = np.zeros((tamanio[0],tamanio[1]),int).astype(np.uint8)
cv2.imwrite("save.jpg",imgReds.astype(np.uint8)*255)

cv2.imshow("redEdges", imgEdges)
tempCirc = Circle()
for x in range(0,tamanio[1]):
    for y in range(0, tamanio[0]):
        found = False
        if(imgEdges[y,x] == 255):
            tempCirc.p1 = [x,y]
            for x in range(tempCirc.p1[0]+1, tamanio[1]):
                if not(imgReds[y,x]):
                    tempCirc.p2 = [x,y]
                    found = True
                    break;
                found = False
            if(found):
                x = int((tempCirc.p1[0]+tempCirc.p2[0])/2) # ahora se va a mover el eje x = (la mitad de los extremos)
                if(x == tempCirc.p1[0]): continue #en caso de que el circulo detectado se de 2x2
                for y in range(tempCirc.p1[1]+1, tamanio[0]):
                    if not(imgReds[y,x]):
                        tempCirc.p3 = [x,y]
                        found = True
                        break;
                    found = False
                if(found):
                    tempCirc.getEq()
                    imgEdgesCenters[tempCirc.center[1],tempCirc.center[0]] = 200
                    if(tempCirc.radius > (tamanio[0]+tamanio[1])/4): continue #en caso de que encuentre un circulo muy grande
                    successCount = 0
                    numOfTests = 10
                    tempRadius = int(tempCirc.radius*0.75)
                    minX = int(tempCirc.center[0] - tempRadius)
                    sizeX = tempRadius

                     #en caso de que se encuentre el posible circulo en un borde
                    if(minX < 0): minX = 0
                    if(tempCirc.center[0] + tempRadius > tamanio[1]): sizeX = tamanio[1]-minX-1

                    for i in range(20):
                        testX= random.randint(minX, minX+sizeX) #genera un numero aleatorio dentro del dominio de un circulo con la 3/4 del radio original
                        testY = circunferencia(testX, tempCirc.center[0], tempCirc.center[1], tempRadius)

                        #en caso de que se encuentre el posible circulo en un borde
                        if(testY < 0): testY = 0
                        if(testY >= tamanio[0]): testY = tamanio[0]-1

                        if(imgReds[testY,testX]):
                            successCount +=1
                        if(imgReds[int(testY-tempRadius),testX]):
                            successCount +=1

                    tempRadius = int(tempCirc.radius*1.25)
                    for i in range(20):
                        testX= random.randint(int(tempCirc.center[0] - tempRadius), int(tempCirc.center[0] + tempRadius)) #genera un numero aleatorio dentro del dominio de un circulo con la 3/4 del radio original
                        testY = circunferencia(testX, tempCirc.center[0], tempCirc.center[1], tempRadius)

                        #en caso de que se encuentre el posible circulo en un borde
                        if(testX < 0): testX = 0
                        if(testX >= tamanio[1]): testX = tamanio[1]-1
                        if(testY < 0): testY = 0
                        if(testY >= tamanio[0]): testY = tamanio[0]-1

                        if not(imgReds[testY,testX]):
                            successCount +=1
                        if not(imgReds[int(testY-tempRadius),testX]):
                            successCount +=1

                    if(successCount > 65):
                        justCirclesArea[int(tempCirc.center[1] - tempRadius):int(tempCirc.center[1] + tempRadius),int(tempCirc.center[0] - tempRadius):int(tempCirc.center[0] + tempRadius)] = 255
                        imgEdges[int(tempCirc.center[1] - tempRadius):int(tempCirc.center[1] + tempRadius),int(tempCirc.center[0] - tempRadius):int(tempCirc.center[0] + tempRadius)] = 0
                        justCircles[int(tempCirc.center[1] - tempRadius):int(tempCirc.center[1] + tempRadius),int(tempCirc.center[0] - tempRadius):int(tempCirc.center[0] + tempRadius)] = imgReds[int(tempCirc.center[1] - tempRadius):int(tempCirc.center[1] + tempRadius),int(tempCirc.center[0] - tempRadius):int(tempCirc.center[0] + tempRadius)]



cv2.imshow("circle Area", justCirclesArea)
cv2.imshow("circle threshold", justCircles*255)
imgReds = imgReds.astype(np.uint8)*255 #convierte a imagen de 8bits


#cv2.namedWindow("reds", cv2.WINDOW_NORMAL)  



#cv2.imwrite("save.jpg",imgChannels[0])
cv2.waitKey(0)



#x^2+y^1+cx+dy+e=0
#https://www.youtube.com/watch?v=J0526-mTn7g
#np.linalg.det(matriz) #para obtener determinante