from osmiumtester import *
from numpy import inf, zeros, argmax
from copy import copy

class nestList():
    # En klass som gör att mina listor kan indexeras med 
    # VAD SOM HELST (så länge det är en int, alltså)
    # men returnerar -1 om indexet ligger utanför listan
    def __init__(self, nlist):
        self.nlist = nlist

    def get(self, i, j):
        if i >= 0 and i < len(self.nlist):
            if j >= 0 and j < len(self.nlist[0]):
                return self.nlist[i][j]
        return -1

    def sätt(self, i, j, item):
        if i >= 0 and i < len(self.nlist):
            if j >= 0 and j < len(self.nlist):
                self.nlist[i][j] = item
            else:
                pass
        else:
            pass


def init_kumMat(rader, kolumner):
    #Initiera nestlade listor
    mat = []
    for i in range(rader):
        mat.append([])
        for j in range(kolumner):
            mat[i].append(0)
    return mat


def trött_robot(OSMat, kum1, kum2, kum3):
    # i kum1 har jag aldrig backat
    # i kum2 har jag backat 1 gång
    # i kum3 har jag backat 2 gånger
    
    n = len(kum1.nlist)

    kum1.sätt(0,0,OSMat.get(0,0))
    kum2.sätt(0,0,OSMat.get(0,0))
    kum3.sätt(0,0,OSMat.get(0,0))         
            
    
    # Stega igenom saker som befinners sig på samma manhattanavstånd
    for md in range(1,(2*n)): 
        for k in range(md):
            i = md - k - 1
            j = k
            if i == 0 and j == 0:
                continue
            if i > n-1 or j > n-1:
                continue

            mp1 = max(kum1.get(i-1,j), kum1.get(i,j-1))
            kum1.sätt(i,j, mp1 + OSMat.get(i,j))


            mp2= max(kum2.get(i-1,j), kum2.get(i,j-1), 
                                kum1.get(i,j-1)+OSMat.get(i+1,j-1),
                                kum1.get(i-1,j)+OSMat.get(i-1,j+1))
            kum2.sätt(i,j,mp2 + OSMat.get(i,j))
           

            mp3 = max(kum3.get(i-1,j), kum3.get(i,j-1),
                    kum2.get(i-1,j) + OSMat.get(i-1, j+1),
                    kum2.get(i,j-1) + OSMat.get(i+1, j-1),
                    kum1.get(i-1, j) + OSMat.get(i-1, j+1) + OSMat.get(i-1, j+2),
                    kum1.get(i, j-1) + OSMat.get(i+1, j-1) + OSMat.get(i+2, j-1))
            kum3.sätt(i,j,(mp3 + OSMat.get(i,j)))

            
    return kum1, kum2, kum3

def stegmap(i,j):
    sm = [[2,i-1,j],[2,i,j-1],[1,i-1,j],[1,i,j-1],[0,i-1,j],[0,i,j-1]]
    return sm

inOS = test9
currentOS = nestList(inOS)
n = len(inOS)
kumMat1 = nestList(init_kumMat(n,n))
kumMat2 = nestList(init_kumMat(n,n))
kumMat3 = nestList(init_kumMat(n,n))


for row in currentOS.nlist:
    print(row)

slutmat1, slutmat2, slutmat3 = trött_robot(currentOS, kumMat1, kumMat2, kumMat3)

print("Q1:")
for row in slutmat1.nlist:
    print(row)

print("Q2:")
for row in slutmat2.nlist:
    print(row)

print("Q3:")
for row in slutmat3.nlist:
    print(row)

bp = []
nbp = [2,n-1,n-1]
bp.append(nbp)
m = nbp[0]
i = nbp[1]
j = nbp[2]

while i > -1 and j > -1:
    if m == 2:
        prev_ruta = [slutmat3.get(i-1,j), slutmat3.get(i,j-1),
                    slutmat2.get(i-1,j) + currentOS.get(i-1, j+1),
                    slutmat2.get(i,j-1) + currentOS.get(i+1, j-1),
                    slutmat1.get(i-1, j) + currentOS.get(i-1, j+1) + currentOS.get(i-1, j+2),
                    slutmat1.get(i, j-1) + currentOS.get(i+1, j-1) + currentOS.get(i+2, j-1)]
    if m == 1:
        prev_ruta = [-1,-1,slutmat2.get(i,j-1), slutmat2.get(i,j-1),
                    slutmat1.get(i-1, j) + currentOS.get(i-1, j+1),
                    slutmat1.get(i, j-1) + currentOS.get(i+1, j-1)] 
                    # vi kan aldrig gå till matris 3 från matris 2 när vi backar
    if m == 0:
        prev_ruta = [-1,-1,-1,-1,slutmat1.get(i-1,j), slutmat1.get(i,j-1)] 
                # vi kan aldrig gå till matris 2 eller 3 från matris 1 när vi backar
    
    ind = argmax(prev_ruta)
    sm = [[2,i-1,j],[2,i,j-1],[1,i-1,j],[1,i,j-1],[0,i-1,j],[0,i,j-1]]
    nbp = sm[ind]
    m = nbp[0]
    i = nbp[1]
    j = nbp[2]
    bp.append(nbp)

bp.reverse()
print(bp)
ebp = bp.copy()
ebp.append([-1,-1])
ebp = ebp[1:]

path = []
steps = zip(bp, ebp)

for step in steps:
    path.append([step[0][1],step[0][2]])
    if step[0][0] != step[1][0]:
        if step[1][0] - step[0][0]  == 2:
            #vi tog två baksteg på en gång
            if step[1][1] - step[0][1]  == 1:
                #skillnad i rader: baksteget togs åt vänster
                path.append([step[0][1],step[0][2]+1])
                path.append([step[0][1],step[0][2]+2])
                path.append([step[0][1],step[0][2]+1])
                path.append([step[0][1],step[0][2]])
            else:
                #skillnad i kolumner: baksteget togs uppåt
                path.append([step[0][1]+1,step[0][2]])
                path.append([step[0][1]+2,step[0][2]])
                path.append([step[0][1]+1,step[0][2]])
                path.append([step[0][1],step[0][2]])
        if step[1][0] - step[0][0] == 1:
            #vi tog ett baksteg
            if step[1][1] - step[0][1]  == 1:
                #skillnad i rader: baksteget togs åt vänster
                path.append([step[0][1],step[0][2]+1])
                path.append([step[0][1],step[0][2]])        
            else:
                #skillnad i kolumner: baksteget togs uppåt
                path.append([step[0][1]+1,step[0][2]])
                path.append([step[0][1],step[0][2]])
    

print(path)
print("max:")
print(slutmat3.get(n-1,n-1)) 