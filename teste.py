import pickle
import cv2 as cv

C = pickle.load( open( "treino.p", "rb" ) )
e2 = 8

img = cv.imread('00000001.jpg')

# funções
def colordist(xt, vi):
    norma_xt = (xt[0]**2+xt[1]**2+xt[2]**2)
    norma_vi = (vi[0]**2+vi[1]**2+vi[2]**2)
    xv = (float(vi[0])*float(xt[0]) + float(vi[1])*float(xt[1]) + float(vi[2])*float(xt[2]))

    if norma_vi < 0:
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