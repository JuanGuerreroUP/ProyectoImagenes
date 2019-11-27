import cv2
import numpy as np
from circleDetector import Circle

#functions
def gamma(img, gamma):
    invGamma = 1/gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(img, table)

#end of functions

circulo = Circle();
circulo.p1 = [5,8]
circulo.p2 = [10,12]
circulo.p3 = [3,15]

circulo.getEq
#
img = cv2.imread("red-eye0.jpg")

tamanio = np.shape(img)
print("y: ",tamanio[0])
print("x: ",tamanio[1])
#img = cv2.resize(img, None, fx=0.5, fy=0.5,interpolation=cv2.INTER_CUBIC)
#BGR
imgChannels = [img[:,:,0], img[:,:,1], img[:,:,2]]
#cv2.imwrite("save.jpg",imgChannels[0])

#for i in range(3):
#    imgChannels[i] = cv2.GaussianBlur(imgChannels[i],(3,3),2)
#imgFinal = cv2.merge(imgChannels)
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
#imgReds = np.zeros((tamanio[0],tamanio[1]))

#imgReds = (imgHSV[:,:,0]<= 5) & (imgHSV[:,:,1] > 80) & (imgHSV[:,:,2] > 60)
print("H max:", np.max(imgHSV[:,:,0]))
imgReds = (imgHSV[:,:,0] <= 5) & (imgHSV[:,:,1] > 80) & (imgHSV[:,:,2] > 60)
imgPinks = (imgHSV[:,:,0] >= 120) & (imgHSV[:,:,1] > 80) & (imgHSV[:,:,2] > 60)
imgReds = imgReds + imgPinks
imgReds = imgReds.astype(np.uint8)*255

itera = 0
posibles = []
for y in range(0,tamanio[0],5):
    for x in range(0,tamanio[1],5):
        if(imgReds[y,x]==255):
            posibles.append([x,y])#append solo cuando se cumpla el algortimo por tangentes para detectar circulos
#for x in imgReds:
   # for y in x:
       # if(y == 255):
         #   imgReds[x,y]=200

    
#imgReds = cv2.resize(imgReds, None, fx=0.5, fy=0.5,interpolation=cv2.INTER_CUBIC)
cv2.Canny(imgReds, 100,100) #edge detection, cambiar a detector de sobel



#cv2.namedWindow("reds", cv2.WINDOW_NORMAL)  
cv2.imshow("reds", cv2.Canny(imgReds,100,100))
#mask = cv2.inRange(imgHSV, lowerRed, upperRed)
#cv2.imshow("mask",mask)

cv2.waitKey(0)

#x^2+y^1+cx+dy+e=0
#https://www.youtube.com/watch?v=J0526-mTn7g
#np.linalg.det(matriz) #para obtener determinante