import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import math
import pickle

C = pickle.load(open("treino.p", "rb" ))
e2 = 1000

img = cv.imread('00000001.jpg')


img_preta = np.zeros([img.shape[0],img.shape[1],3])


def colordist(xt, vi):
    norma_xt = (xt[0]**2+xt[1]**2+xt[2]**2)
    norma_vi = (vi[0]**2+vi[1]**2+vi[2]**2)
    xv = (float(vi[0])*float(xt[0]) + float(vi[1])*float(xt[1]) + float(vi[2])*float(xt[2]))

    if norma_vi <= 0:
        p = 0
    else:
        p = xv/norma_vi
    
    return math.sqrt(abs(norma_xt - p))

def brightness(xt, Imin, Imax):
    alpha = 0.7
    beta = 1.5
    Ilow = alpha * Imax
    Ihi = min(beta*Imax, (Imin/alpha))
    norma_xt = (xt[0]**2+xt[1]**2+xt[2]**2)**(1/2)
    if Ilow <= norma_xt and norma_xt <= Ihi:
        return True
    else:
        return False

def fBGS(xt, cw):
    R = xt[0]
    G = xt[1]
    B = xt[2]
    I =(R**2 + G**2 + B**2)**(1/2) 


    for cw in C[row][col]:
        if (colordist(xt, cw.v) <= e2) and (brightness(xt, cw.aux[0], cw.aux[1])== True):
            #background
            cw.v[0] = (cw.aux[2]*cw.v[0]+xt[0])/(cw.aux[2]+1)
            cw.v[1] = (cw.aux[2]*cw.v[1]+xt[1])/(cw.aux[2]+1)
            cw.v[2] = (cw.aux[2]*cw.v[2]+xt[2])/(cw.aux[2]+1)
            Imin = min(I, cw.aux[0])
            Imax = max(I, cw.aux[1])
            #ainda não determinamos o valor de t
            t = 1
            cw.aux = (Imin, Imax, cw.aux[2]+1, max(cw.aux[3],t-cw.aux[5]), cw.aux[4], t)

            return True

        else:
        #foreground
            return False



for row in range (img.shape[0]):
    for col in range(img.shape[1]):
        pessoa = fBGS(img[row, col, :], C)
        if pessoa == False:
            for i in range(3):
                img_preta[row, col, i] = 255

plt.imshow(np.uint32(img_preta))
plt.show()
