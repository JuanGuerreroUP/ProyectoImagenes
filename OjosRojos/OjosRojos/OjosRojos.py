import cv2
import numpy as np
import random
import time
from circleDetector import Circle

#parameters:
imageSource = "red-eye6.jpg"

minBrightness = 15
numOfTests = 30
successTolerance = 0.75
circleToreranceDelta = 0.1
outerCircTolerance =  0.025




#end of parameters


#functions
def gamma(img, gamma):
    invGamma = 1/gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(img, table)

def circunferencia(x,h,k,r):
    return int(pow(pow(r,2)-pow(x-h,2),0.5)+k)
#end of functions



img_original = cv2.imread(imageSource)
cv2.imshow("Original image", img_original)

img = img_original



tamanio = np.shape(img) #[y,x]
tamanio_original = tamanio
if(tamanio[0] > 800): #en caso de que la imagen sea muy grande, se escala proporcionalmente para agilizar su procesamiento.
    img = cv2.resize(img, (800, int(tamanio[0]*800/tamanio[1])))
    tamanio = np.shape(img)
if(tamanio[1] > 800):
    img = cv2.resize(img, ((int(tamanio[1]*800/tamanio[0])),800))
    tamanio = np.shape(img)

print("y: ",tamanio[0])
print("x: ",tamanio[1])

#BGR
imgChannels = [img[:,:,0], img[:,:,1], img[:,:,2]]


imgChannels[2] = gamma(imgChannels[2],0.8) #se aplica función gamma en el canal R (de BGR) para disminuir los tonos rojizos

imgMerged = cv2.merge(imgChannels) #se concatenan los tres canales con gamma en canal R

imgGauss = cv2.GaussianBlur(imgMerged,(9,9),5) #se hace un blur a la imagen para reducir el ruido





cv2.imshow("gamma",imgMerged)
cv2.imshow("gamma-gauss",imgGauss)
imgHSV = cv2.cvtColor(imgGauss, cv2.COLOR_BGR2HSV)


#H(0-180) S(0-100) V(0-100)
imgReds = (imgHSV[:,:,0] <= 5) & (imgHSV[:,:,1] > 80) & (imgHSV[:,:,2] > minBrightness) #se hace un threshold para los pixeles con hue correspondiente a un rojo con valores cercanos a 0°
imgPinks = (imgHSV[:,:,0] >= 120) & (imgHSV[:,:,1] > 80) & (imgHSV[:,:,2] > minBrightness)#se hace un threshold para los pixeles con hue correspondiente a un rojo con valores cercanos a 179°
imgReds = imgReds + imgPinks #se juntan los 2 umbrales para crear una mascara de las zonas de la imagen que tienen rojos

imgEdges = cv2.Canny(imgReds.astype(np.uint8)*255, 100,100);#edge detection, crea una imagen con los bordes del umbral

posibleCircleBlocks = np.zeros((tamanio[0],tamanio[1]),int).astype(np.uint8) #solo para mostrar el proceso
justCircles = np.zeros((tamanio[0],tamanio[1]),int).astype(np.uint8)
justCirclesArea = np.zeros((tamanio[0],tamanio[1]),int).astype(np.uint8)


cv2.imshow("redEdges", imgEdges) #muestra los bordes del umbral

for x in range(0,tamanio[1]):
    for y in range(0, tamanio[0]):
        found = False
        if(imgEdges[y,x] == 255): 
            #se ejecuta cuando encuentra un pixel de un borde del umbral
            tempCirc = Circle([x,y]) #se crea un objeto Circle, el cual puede calcular las propiedades de un circulo dados tres puntos[x,y]
                                     #y se pasa en el parametro del constructor el primer pixel encontrado de un borde figura dentro del umbral
            for x in range(tempCirc.p1[0]+1, tamanio[1]):
                if not(imgReds[y,x]):
                    tempCirc.p2 = [x,y]
                    found = True
                    break; #se hace un sliding-window de 1x1 hacia la derecha, hasta que sale de la figura, y a ese punto se le asigna como el segundo punto de la circunferencia
                found = False
            if(found):
                x = int((tempCirc.p1[0]+tempCirc.p2[0])/2) # ahora se va a mover el eje x = (la mitad de los extremos)
                if(x == tempCirc.p1[0]): continue #en caso de que el circulo detectado se de 2x2
                for y in range(tempCirc.p1[1]+1, tamanio[0]):
                    if not(imgReds[y,x]):
                        tempCirc.p3 = [x,y]
                        found = True
                        break; #se hace un sliding-window de 1x1 hacia abajo hasta que sale de la figura, y a ese punto se le asigna como el tercer punto de la circunferencia
                    found = False
                if(found):
                    tempCirc.getEq() #si se encuentran 3 puntos, entonces se encuentra la circunferencia que pasa por esos 3 puntos
                    if(tempCirc.radius > (tamanio[0]+tamanio[1])/4): continue #en caso de que encuentre un circulo muy grande


                    successCount = 0 #contador que ayuda a calificar que tanto se parece la figura a un circulo
                    
                    tempRadius = int(tempCirc.radius*0.75) #reduce el radio del posible circulo para comprobar valores dentro del circulo, los cuales deben valer 1
                    minX = int(tempCirc.center[0] - tempRadius)
                    sizeX = tempRadius
                    
                     #en caso de que se encuentre en un borde el posible circulo
                    if(minX < 0): minX = 0
                    if(tempCirc.center[0] + tempRadius > tamanio[1]): sizeX = tamanio[1]-minX-1

                    for i in range(numOfTests):
                        testX = int(minX + ((sizeX/numOfTests)*(i+1)))
                        testY = circunferencia(testX, tempCirc.center[0], tempCirc.center[1], tempRadius)

                        #en caso de que se encuentre en un borde el posible circulo
                        if(testY < 0): testY = 0
                        if(testY >= tamanio[0]): testY = tamanio[0]-1

                        if(imgReds[testY,testX]):
                            successCount +=1 #la imagen del umbral tiene un pixel con valor de 1 dentro de lo que corresponde al posible circulo en la parte superior
                        if(imgReds[int(testY-tempRadius),testX]):
                            successCount +=1 #la imagen del umbral tiene un pixel con valor de 1 dentro de lo que corresponde al posible circulo en la parte inferior

                    tempRadius = int(tempCirc.radius*1.25) #aumenta el radio del posible circulo para comprobar valores fuera del circulo, los cuales deben valer 0
                    minX = int(tempCirc.center[0] - tempRadius)
                    sizeX = tempRadius

                     #en caso de que se encuentre en un borde el posible circulo
                    if(minX < 0): minX = 0
                    if(tempCirc.center[0] + tempRadius > tamanio[1]): sizeX = tamanio[1]-minX-1
                    for i in range(numOfTests):
                        testX = int(minX + ((sizeX/numOfTests)*(i+1))) # se fracciona en puntos del eje x que esten dentro del dominio del posible circulo 
                        testY = circunferencia(testX, tempCirc.center[0], tempCirc.center[1], tempRadius) #se obtiene su posición en y, de acuerdo con la funcion de una circunferencia

                        #en caso de que se encuentre en un borde el posible circulo
                        if(testY < 0): testY = 0
                        if(testY >= tamanio[0]): testY = tamanio[0]-1

                        if not(imgReds[testY,testX]):
                            successCount +=1 #la imagen del umbral tiene un pixel con valor de 0 fuera de lo que corresponde al posible circulo en la parte superior
                        if not(imgReds[int(testY-tempRadius),testX]): #propiedad de simetria de una circunferencia
                            successCount +=1 #la imagen del umbral tiene un pixel con valor de 0 fuera de lo que corresponde al posible circulo en la parte inferior
            
                    if(successCount/(numOfTests*4) > successTolerance):
                        posibleCircleBlocks[int(tempCirc.center[1] - tempRadius):int(tempCirc.center[1] + tempRadius),int(tempCirc.center[0] - tempRadius):int(tempCirc.center[0] + tempRadius)] = 255
                        tempBlock = imgReds[int(tempCirc.center[1] - tempRadius):int(tempCirc.center[1] + tempRadius),int(tempCirc.center[0] - tempRadius):int(tempCirc.center[0] + tempRadius)]
                        tempBlock = tempBlock.astype(np.uint8) #se va a crear un bloque que sustrae el posible circulo de la imagen
                        tempAvg =  cv2.mean(tempBlock)[0]; #calcula el promedio de valores de los pixeles
                        cv2.circle(tempBlock,(tempRadius,tempRadius),tempCirc.radius,1,-1) #añade un circulo de unos al bloque del tamaño teorico del ojo
                        tempAvg2 =  cv2.mean(tempBlock)[0]; #nuevamente calcula el promedio del bloque pero ahora concatenado con la mascara del circulo
                        #si es un circulo, no se debieron de haber remplazado muchos valores, por lo que los promedios(tempAvg y tempAvg2) deben de ser muy similares
                        cv2.circle(tempBlock,(tempRadius,tempRadius),tempRadius,0,-1) #posteriormente se borra un circulo del tamaño del bloque
                        blackAvg = cv2.mean(tempBlock)[0]; #ahora al calcular el promedio con el circulo borrado
                        #si es un circulo, el bloque debería ser casi negro.
                        if(abs(tempAvg-tempAvg2) < circleToreranceDelta and blackAvg < outerCircTolerance): #en esta comparación se confirma que la figura es un circulo
                            #se crean mascaras que sustraen los circulos del resto de la imagen
                            justCirclesArea[int(tempCirc.center[1] - tempRadius):int(tempCirc.center[1] + tempRadius),int(tempCirc.center[0] - tempRadius):int(tempCirc.center[0] + tempRadius)] = 255
                            imgEdges[int(tempCirc.center[1] - tempRadius):int(tempCirc.center[1] + tempRadius),int(tempCirc.center[0] - tempRadius):int(tempCirc.center[0] + tempRadius)] = 0 #se borra el circulo de la imagen de bordes para evitar que se recalcule
                            justCircles[int(tempCirc.center[1] - tempRadius):int(tempCirc.center[1] + tempRadius),int(tempCirc.center[0] - tempRadius):int(tempCirc.center[0] + tempRadius)] = imgReds[int(tempCirc.center[1] - tempRadius):int(tempCirc.center[1] + tempRadius),int(tempCirc.center[0] - tempRadius):int(tempCirc.center[0] + tempRadius)]



cv2.imshow("posible circle Area", posibleCircleBlocks) #solo para mostrar las zonas donde hubieron figuras con borde similar a una circunferencia
cv2.imshow("circle Area", justCirclesArea) #solo para mostrar las zonas donde detecto circulos
cv2.imshow("isolated circles", justCircles*255) #una matriz boolanea donde se aislan todos los circulos rojos del resto de la imagen

#se añade un blur a la imagen para que los cambios de color no sean tan abruptos y se rescala la imagen al tamaño original
bluryCircles = cv2.GaussianBlur(cv2.resize(justCircles*1.0,(tamanio_original[1],tamanio_original[0])),(21,21),2) # *1.0 para hacerlo float y que el blur sea entre 0 y 1
cv2.imshow("blury circles", bluryCircles)

imgHSV_original = cv2.cvtColor(img_original, cv2.COLOR_BGR2HSV) #convierte la imagen original (sin ninguna operación) a HSV para modificar las tonalidades de los ojos


imgHSV_original[:,:,0] = (40*bluryCircles) + (imgHSV_original[:,:,0]*(1-bluryCircles)) #que tanto aporta el Hue original en los ojos
imgHSV_original[:,:,1] = imgHSV_original[:,:,1]*(1-(bluryCircles*0.9)) #vuelve la zona de los ojos en casi blanco y negro
imgHSV_original[:,:,2] = imgHSV_original[:,:,2]*(1-(bluryCircles*0.8)) #oscurece la zona de los ojos
finalImg = cv2.cvtColor(imgHSV_original,cv2.COLOR_HSV2BGR)

#cv2.namedWindow("Final image", cv2.WINDOW_NORMAL)  
cv2.imshow("Final image", finalImg.astype(np.uint8))



cv2.imwrite("result.jpg",finalImg)
cv2.waitKey(0)


