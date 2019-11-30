import cv2
import numpy as np
import random
import time
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

img_original = cv2.imread("red-eye2.jpg")
img = img_original

#parameters:
numOfTests = 30
successTolerance = 0.75;
circleToreranceDelta = 0.1
#end of parameters


tamanio = np.shape(img) #[y,x]
tamanio_original = tamanio
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
#cv2.imshow("orignial",img)

cv2.namedWindow("gamma", cv2.WINDOW_NORMAL) 
cv2.imshow("gamma",imgMerged)
cv2.imshow("gamma-gauss",imgGauss)
imgHSV = cv2.cvtColor(imgGauss, cv2.COLOR_BGR2HSV)


#H(0-180) S(0-100) V(0-100)
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

for x in range(0,tamanio[1]):
    for y in range(0, tamanio[0]):
        found = False
        if(imgEdges[y,x] == 255):
            tempCirc = Circle()
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
                    
                    tempRadius = int(tempCirc.radius*0.75)
                    minX = int(tempCirc.center[0] - tempRadius)
                    sizeX = tempRadius
                    
                     #en caso de que se encuentre el posible circulo en un borde
                    if(minX < 0): minX = 0
                    if(tempCirc.center[0] + tempRadius > tamanio[1]): sizeX = tamanio[1]-minX-1

                    for i in range(numOfTests):
                        testX = int(minX + ((sizeX/numOfTests)*(i+1)))
                        testY = circunferencia(testX, tempCirc.center[0], tempCirc.center[1], tempRadius)

                        #en caso de que se encuentre el posible circulo en un borde
                        if(testY < 0): testY = 0
                        if(testY >= tamanio[0]): testY = tamanio[0]-1

                        if(imgReds[testY,testX]):
                            successCount +=1
                        if(imgReds[int(testY-tempRadius),testX]):
                            successCount +=1

                    tempRadius = int(tempCirc.radius*1.25)
                    minX = int(tempCirc.center[0] - tempRadius)
                    sizeX = tempRadius

                     #en caso de que se encuentre el posible circulo en un borde
                    if(minX < 0): minX = 0
                    if(tempCirc.center[0] + tempRadius > tamanio[1]): sizeX = tamanio[1]-minX-1
                    for i in range(numOfTests):
                        testX = int(minX + ((sizeX/numOfTests)*(i+1)))
                        testY = circunferencia(testX, tempCirc.center[0], tempCirc.center[1], tempRadius)

                        #en caso de que se encuentre el posible circulo en un borde
                        if(testY < 0): testY = 0
                        if(testY >= tamanio[0]): testY = tamanio[0]-1

                        if not(imgReds[testY,testX]):
                            successCount +=1
                        if not(imgReds[int(testY-tempRadius),testX]):
                            successCount +=1
            
                    if(successCount/(numOfTests*4) > successTolerance):
                        tempBlock = imgReds[int(tempCirc.center[1] - tempRadius):int(tempCirc.center[1] + tempRadius),int(tempCirc.center[0] - tempRadius):int(tempCirc.center[0] + tempRadius)]
                        tempBlock = tempBlock.astype(np.uint8)
                        tempAvg =  cv2.mean(tempBlock)[0];
                        cv2.circle(tempBlock,(tempRadius,tempRadius),tempCirc.radius,1,-1)
                        tempAvg2 =  cv2.mean(tempBlock)[0];
                        cv2.circle(tempBlock,(tempRadius,tempRadius),tempRadius,0,-1)
                        blackAvg = cv2.mean(tempBlock)[0];
                        if(abs(tempAvg-tempAvg2) < circleToreranceDelta and blackAvg < 0.025): # (0.92/tempRadius) en blackAvg se hace una regla de 3 para no castigar a circulos muy pequeños
                            justCirclesArea[int(tempCirc.center[1] - tempRadius):int(tempCirc.center[1] + tempRadius),int(tempCirc.center[0] - tempRadius):int(tempCirc.center[0] + tempRadius)] = 255
                            imgEdges[int(tempCirc.center[1] - tempRadius):int(tempCirc.center[1] + tempRadius),int(tempCirc.center[0] - tempRadius):int(tempCirc.center[0] + tempRadius)] = 0
                            justCircles[int(tempCirc.center[1] - tempRadius):int(tempCirc.center[1] + tempRadius),int(tempCirc.center[0] - tempRadius):int(tempCirc.center[0] + tempRadius)] = imgReds[int(tempCirc.center[1] - tempRadius):int(tempCirc.center[1] + tempRadius),int(tempCirc.center[0] - tempRadius):int(tempCirc.center[0] + tempRadius)]



cv2.imshow("circle Area", justCirclesArea)

#se añade un blur a la imagen para que los cambios de color no sean tan abruptos y se rescala la imagen al tamaño original
bluryCircles = cv2.GaussianBlur(cv2.resize(justCircles*1.0,(tamanio_original[1],tamanio_original[0])),(21,21),2) # *87 porque se va a usar en el canal V para dar un tono cafe.
cv2.imshow("blury circles", bluryCircles)

imgHSV_original = cv2.cvtColor(img_original, cv2.COLOR_BGR2HSV)

cv2.imshow("Original image", img_original)
imgHSV_original[:,:,0] = (40*bluryCircles) + (imgHSV_original[:,:,0]*(1-bluryCircles))
print(np.min(imgHSV_original[:,:,0]))
imgHSV_original[:,:,1] = imgHSV_original[:,:,1]*(1-(bluryCircles*0.9))
imgHSV_original[:,:,2] = imgHSV_original[:,:,2]*(1-(bluryCircles*0.8))
finalImg = cv2.cvtColor(imgHSV_original,cv2.COLOR_HSV2BGR)

#cv2.namedWindow("Final image", cv2.WINDOW_NORMAL)  
cv2.imshow("Final image", finalImg.astype(np.uint8))
imgReds = imgReds.astype(np.uint8)*255 #convierte a imagen de 8bits


#cv2.namedWindow("reds", cv2.WINDOW_NORMAL)  


#cv2.imwrite("save.jpg",imgChannels[0])
cv2.waitKey(0)



#x^2+y^1+cx+dy+e=0
#https://www.youtube.com/watch?v=J0526-mTn7g
#np.linalg.det(matriz) #para obtener determinante