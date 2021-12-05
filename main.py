import numpy as np
from numpy import random
import warnings
from matplotlib import pyplot as plt
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)

class Lamina():
    def __init__(self):
        self.x=100
        self.y=100
        self.lamina = np.zeros ((10, 10))

    def sobrante(self):
        sobra=0
        for i in np.nditer(self.lamina, order='C'):
            if(i==0):
                sobra+=1         
        return sobra*100
#################################################

class Piezas():
    def __init__(self):
        self.x=0
        self.y=0
        self.piezas = np.array([
            [80,30,1,0],
            [50,10,2,0],
            [20,20,3,0],
            [10,10,4,0],
            [90,40,5,0],
            [60,20,6,0],
            [40,30,7,0],
            [50,70,8,0],
            [30,20,9,0],
            [40,20,10,0]]
        )

        p0= np.full((int(self.piezas[0][0]/10),int(self.piezas[0][1]/10)),self.piezas[0][2])
        p1= np.full((int(self.piezas[1][0]/10),int(self.piezas[1][1]/10)),self.piezas[1][2])
        p2= np.full((int(self.piezas[2][0]/10),int(self.piezas[2][1]/10)),self.piezas[2][2])
        p3= np.full((int(self.piezas[3][0]/10),int(self.piezas[3][1]/10)),self.piezas[3][2])
        p4= np.full((int(self.piezas[4][0]/10),int(self.piezas[4][1]/10)),self.piezas[4][2])
        p5= np.full((int(self.piezas[5][0]/10),int(self.piezas[5][1]/10)),self.piezas[5][2])
        p6= np.full((int(self.piezas[6][0]/10),int(self.piezas[6][1]/10)),self.piezas[6][2])
        p7= np.full((int(self.piezas[7][0]/10),int(self.piezas[7][1]/10)),self.piezas[7][2])
        p8= np.full((int(self.piezas[8][0]/10),int(self.piezas[8][1]/10)),self.piezas[8][2])
        p9= np.full((int(self.piezas[9][0]/10),int(self.piezas[9][1]/10)),self.piezas[9][2])

        self.pieces=[p0,p1,p2,p3,p4,p5,p6,p7,p8,p9]
        self.height = 0
        self.width = 0
        self.id=0
        self.auxiliar= []

        self.area=[]
        for i in range(len(self.pieces)):
            temp = self.pieces[i]
            areaTemp = (len(temp)*len(temp[0])*100)
            self.area=np.append(self.area, areaTemp)    
        self.auxArea=[]
        #heuristica numero de piezas faltantes por cortar, inicia en 10, toda solucion tine una h=0
        self.h = len(self.pieces)

    def getPieza(self, id):
        piece = self.pieces[id]
        self.height = len(piece)
        self.width = len(piece[0])
        self.id=id
        return piece

    def getRandomPiece(self):
        nodo0 = random.randint(len(self.pieces))
        piece = self.pieces[nodo0]
        self.height = len(piece)
        self.width = len(piece[0])
        self.id=nodo0
        return piece

    def rotar(self, id):
        piece = np.transpose(self.getPieza(id))
        self.height = len(piece)
        self.width = len(piece[0])
        self.id=id
        self.pieces[id]=piece
        return piece

    def nextLamin(self):
        self.pieces=self.auxiliar
        self.area=self.auxArea

    def remove(self, id):
        self.auxiliar.append(self.pieces[id])
        self.pieces=np.delete(self.pieces, id)
        self.auxArea.append(self.area[id])
        self.area=np.delete(self.area, id)

    def cutPiece(self, id, lamina, ejex, ejey):
        piece=self.getPieza(id)
        for y in range(self.height):
            for x in range(self.width):
                if(piece[y][x]!=0):
                    lamina[ejey + y][ejex + x] = piece[0][0]
        self.pieces=np.delete(self.pieces, id)
        self.area=np.delete(self.area, id)
        self.h-=1

    def canCut(self, id, lamina, ejex, ejey):
        piece=self.getPieza(id)
        result = True
        if(ejex+self.width>len(lamina) or ejey+self.height>len(lamina[0])):
            result = False
        else:
            for x in range(self.width):
                for y in range(self.height):
                    if(lamina[ejey + y][ejex + x] != 0):
                        return False        
        return result
#################################################

def hillclimbing():
    orient=random.randint(2)
    piezas = Piezas()
    laminas=[]
    laminCount=1
    while(piezas.h!=0):
        lamin = Lamina()
        l1=lamin
        laminas.append(l1)
        count=0
        #nodo0 es elegido aleatoriamente entre las piesas posibles y colocado en 0,0
        piezas.getRandomPiece()
        #nodo0 se elige la pieza mas grande
        ##piezas.getPieza(np.argmax(piezas.area))
        if(orient != 0):
            piezas.rotar(piezas.id)
        #se corta la primera pieza
        piezas.cutPiece(piezas.id,laminas[laminCount-1].lamina,0,0)
        #se trata de meter piezas
        while(count<100):
            if(len(piezas.pieces)==0):
                break
            if(np.amax(piezas.area)<=laminas[laminCount-1].sobrante()):
                id=np.argmax(piezas.area)
                ejex=random.randint(10)
                ejey=random.randint(10)
                if(piezas.canCut(id,laminas[laminCount-1].lamina,ejex,ejey)):
                    piezas.cutPiece(id,laminas[laminCount-1].lamina,ejex,ejey)
                    if(len(piezas.pieces)==0):
                        break
                    count=0
                    continue
                else:
                    piezas.rotar(id)
                    if(piezas.canCut(id,laminas[laminCount-1].lamina,ejex,ejey)):
                        piezas.cutPiece(id,laminas[laminCount-1].lamina,ejex,ejey)
                        if(len(piezas.pieces)==0):
                            break
                        count=0
                        continue
                    else:
                        piezas.rotar(id)
                        count+=1
                        if(count==100):
                            piezas.remove(id)
                            count=0
            else:
                id=np.argmax(piezas.area)
                piezas.remove(id)
                count=0
                continue
        laminCount+=1
        piezas.nextLamin()
    #printResult(laminas)
    return laminas

def printResult(laminas):
    colormap = plt.cm.nipy_spectral#nipy_spectral #I suggest to use nipy_spectral, Set1,Paired
    for i in range(len(laminas)):
        print('Lamina #', i+1)
        print(laminas[i].lamina)
        sobra=laminas[i].sobrante()
        print('Sobran ',sobra,'cm^2 de la lamina #',i+1)

        plt.figure(figsize=(6,6))
        plt.pcolor(laminas[i].lamina[::-1],cmap=colormap,edgecolors='k', linewidths=3)
    plt.show()

def optimo(intentos):
    lamina=hillclimbing()
    optim=lamina
    sobra1=lamina[0].sobrante()
    count1=0
    while(count1<intentos-1):
        lamina=hillclimbing()
        sobral1=lamina[0].sobrante()
        sobral2=lamina[1].sobrante()
        if(sobral1<sobra1):
            sobra1=sobral1
            optim=lamina
        count1+=1
    printResult(optim)

optimo(50)
