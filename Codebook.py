import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import math
import pickle

class Codeword:

    def __init__(self, xt, aux):
        self.v = xt
        self.aux = aux

# funções
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
    alpha = 0.4
    beta = 1.1
    Ilow = alpha * Imax
    Ihi = min(beta*Imax, (Imin/alpha))
    norma_xt = (xt[0]**2+xt[1]**2+xt[2]**2)**(1/2)
    if Ilow <= norma_xt and norma_xt <= Ihi:
        return True
    else:
        return False

L=0
e1 = 12
N = 30


for m in range(1, N+1):
    n = 20 + m
    nome = '000000'+str(n)
    img = cv.imread(nome +'.jpg')
    print("primeira imagem")


    C =[]
    for row in range(img.shape[0]):
        C.append([])
        for col in range (img.shape[1]):
            C[row].append([])

    # Algoritmo do Codebook
    for t in range(1, N+1):
        for row in range (img.shape[0]):
            for col in range(img.shape[1]):
                xt = img[row, col, :]
                R = xt[0]
                G = xt[1]
                B = xt[2]
                I =(R**2 + G**2 + B**2)**(1/2) 

                match = False

                for cw in C[row][col]:
                    if (colordist(xt, cw.v) <= e1) and (brightness(xt, cw.aux[0], cw.aux[1])):
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
                new_lamb = max(codeword.aux[3], (N-codeword.aux[5]+codeword.aux[4]-1))
                codeword.aux[3] = new_lamb

pickle.dump(C, open( "treino.p", "wb" ) )