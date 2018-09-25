import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import math

class Codeword:

    def __init__(self, xt, aux):
        self.v = xt
        self.aux = aux

img = cv.imread('background.jpg')

L=0
e1 = 10

t = img.shape[0]*img.shape[1]

C =[]
for row in range(img.shape[0]):
    C.append([])
    for col in range (img.shape[1]):
        C[row].append([])

# funções
def colordist(xt, vi):
    norma_xt = (xt[0]**2+xt[1]**2+xt[2**2])
    p = ((vi[0]*xt[0]) + (vi[1]*xt[1]) + (vi[2]*xt[2]))
    return (norma_xt)-(p)

def brightness(xt, Imin, Imax):
    if Imin <= xt and xt<= Imax:
        return True
    else:
        return False


# Algoritmo do Codebook
for t in (1, N+1):
    for row in range (img.shape[0]):
        for col in range(img.shape[1]):
            xt = img[row, col, :]
            R = xt[0]
            G = xt[1]
            B = xt[2]
            I =(R**2 + G**2 + B**2)**(1/2) 

            match = False

            for cw in C[row][col]:
                if (colordist(xt, cw.v)<=e1) and (brightness(xt, (cw.aux[0], cw.au[1]))):
                    cw.v[0] = (cw.aux[2]*cw.v[0]+xt[0])/(cw.aux[2]+1)
                    cw.v[1] = (cw.aux[2]*cw.v[1]+xt[1])/(cw.aux[2]+1)
                    cw.v[2] = (cw.aux[2]*cw.v[2]+xt[2])/(cw.aux[2]+1)
                    Imin = min(I, cw.aux[0])
                    Imax = max(I, cw.aux[1])
                    cw.aux = (Imin, Imax, cw.aux[2]+1, max(cw.aux[3],t-cw.aux[5]), cw.aux[4], t)

                    match = True
                    break 

            if match == False:
                C[row][col].append(Codeword(xt, [I,I,1,t-1,t,t]))

for row in C:
    for col in row:
        for codeword in col:
            new_lamb = max(codeword[3], (N-codeword[5]+codeword[4]-1))
            codeword[3] = new_lamb



