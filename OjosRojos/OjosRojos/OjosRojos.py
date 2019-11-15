import cv2
import numpy as np
import circleDetector

#functions
def gamma(img, gamma):
    invGamma = 1/gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(img, table)

#end of functions


img = cv2.imread("ojos-rojos.jpg")

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
imgChannels[2] = gamma(imgChannels[2],0.5)
imgMerged = cv2.merge(imgChannels)
imgGauss = cv2.GaussianBlur(imgMerged,(9,9),15)

cv2.namedWindow("orignial", cv2.WINDOW_NORMAL)  
cv2.imshow("orignial",img)

cv2.namedWindow("gamma", cv2.WINDOW_NORMAL) 
cv2.imshow("gamma",imgMerged)
imgHSV = cv2.cvtColor(imgGauss, cv2.COLOR_BGR2HSV)
lowerRed = np.array([0,60,30])
upperRed = np.array([3,255,255])
print(np.max(imgHSV[:,:,2]))
#imgReds = np.zeros((tamanio[0],tamanio[1]))
imgReds = (imgHSV[:,:,0]< 5) & (imgHSV[:,:,1] > 40) & (imgHSV[:,:,2] > 80)
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
cv2.namedWindow("reds", cv2.WINDOW_NORMAL)  
cv2.imshow("reds",imgReds)
mask = cv2.inRange(imgHSV, lowerRed, upperRed)
#cv2.imshow("mask",mask)

cv2.waitKey(0)

#x^2+y^1+cx+dy+e=0
#https://www.youtube.com/watch?v=J0526-mTn7g
#np.linalg.det(matriz) #para obtener determinante