from re import L, X
import numpy as np
from OpenGL.GL import *
import constants
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from grafica.assets_path import getAssetPath


SIZE_IN_BYTES = constants.SIZE_IN_BYTES



class Shape:
    def __init__(self, vertices, indices):
        self.vertices = vertices
        self.indices = indices

    def __str__(self):
        return "vertices: " + str(self.vertices) + "\n"\
            "indices: " + str(self.indices)


def merge(destinationShape, strideSize, sourceShape):

    # current vertices are an offset for indices refering to vertices of the new shape
    offset = len(destinationShape.vertices)
    destinationShape.vertices += sourceShape.vertices
    destinationShape.indices += [(offset/strideSize) + index for index in sourceShape.indices]

def applyOffset(shape, stride, offset):

    numberOfVertices = len(shape.vertices)//stride

    for i in range(numberOfVertices):
        index = i * stride
        shape.vertices[index]     += offset[0]
        shape.vertices[index + 1] += offset[1]
        shape.vertices[index + 2] += offset[2]


def scaleVertices(shape, stride, scaleFactor):

    numberOfVertices = len(shape.vertices) // stride

    for i in range(numberOfVertices):
        index = i * stride
        shape.vertices[index]     *= scaleFactor[0]
        shape.vertices[index + 1] *= scaleFactor[1]
        shape.vertices[index + 2] *= scaleFactor[2]





def createCube():#Cubo azul, y para no mostar las diagonales, se hicieron triangulos muy finos, que son las arista del cubo
    
    vertexData = np.array([
        # positions        # colors
        -0.5, -0.5,  0.5,  0.0, 0.0, 1.0,
         0.5, -0.5,  0.5,  0.0, 0.0, 1.0,
         0.5,  0.5,  0.5,  0.0, 0.0, 1.0,
        -0.5,  0.5,  0.5,  0.0, 0.0, 1.0,
 
        -0.5, -0.5, -0.5,  0.0, 0.0, 1.0,
         0.5, -0.5, -0.5,  0.0, 0.0, 1.0,
         0.5,  0.5, -0.5,  0.0, 0.0, 1.0,
        -0.5,  0.5, -0.5,  0.0, 0.0, 1.0
    ], dtype=np.float32)

    indexData = np.array([
        0, 1, 0, 1, 2, 1,
        2, 3, 2, 3, 0, 3,
        0, 4, 0, 1, 5, 1,
        2, 6, 2, 3, 7, 3,
        4, 5, 4, 5, 6, 5,
        6, 7, 6, 7, 4, 7
    ])#"Triangulos" que forman las aristas

    return Shape(vertexData, indexData)

def createSphere(Ratio,N,r,g,b,c_x,c_y,c_z):#N es la cantidad de puntos al aumentar phi, cuanto mayor N mejor la definicion de la esfera
    vertexData = [
        # posicion     # texture    #normals
        c_x, c_y, c_z, 1, 1,        0, 0, 1
    ]

    indexData = []

    dtheta =2*np.pi / N
    dphi= np.pi / N
    R = Ratio

    for i in range(N+1):#Se aumenta el theta en cada interacion, con el siguiente for se forman todos los puntos de phi=0 hasta phi=pi
        theta = i * dtheta
        #r=np.random.random()
        #g=np.random.random()
        #b=np.random.random()
        for j in range(N+1):
            phi = j * dphi

            x = R * np.cos(theta) * np.sin(phi) + c_x
            y = R * np.sin(theta) * np.sin(phi) + c_y
            z = R * np.cos(phi) + c_z

            vertexData += [
            # pos       # texture   #normals
                x, y, z, 1, 1,      0, 0, 1
            ]
            
            indexData += [j, j+N*i, j+1+i*N,j,j+1,j+1+i*N] #Uniendo los puntos en los que va aumentando phi, estos forman triangulos con el centro
            if i>=1:
               indexData += [N*i+j,N*i+j+1,N*(i+1)+j,N*(i+1)+j,N*i+j+1,N*(i+1)+j+1] #Estos son para unir los puntos de una columna de un cierto theta de phi=0 hasta phi=pi,
               #con los del siguiente phi, para que asi no hayan hoyos en la esfera y esta se vea rellena y suave 

    


    


    return Shape(vertexData, indexData)



#Servira para leer el auto que llevara a escena
def readOFF(filename, color):
    vertices = []
    normals= []
    faces = []

    with open(filename, 'r') as file:
        line = file.readline().strip()
        assert line=="OFF"

        line = file.readline().strip()
        aux = line.split(' ')

        numVertices = int(aux[0])
        numFaces = int(aux[1])

        for i in range(numVertices):
            aux = file.readline().strip().split(' ')
            vertices += [float(coord) for coord in aux[0:]]
        
        vertices = np.asarray(vertices)
        vertices = np.reshape(vertices, (numVertices, 3))
        #print(f'Vertices shape: {vertices.shape}')

        normals = np.zeros((numVertices,3), dtype=np.float32)
        #print(f'Normals shape: {normals.shape}')

        for i in range(numFaces):
            aux = file.readline().strip().split(' ')
            aux = [int(index) for index in aux[0:]]
            faces += [aux[1:]]
            
            vecA = [vertices[aux[2]][0] - vertices[aux[1]][0], vertices[aux[2]][1] - vertices[aux[1]][1], vertices[aux[2]][2] - vertices[aux[1]][2]]
            vecB = [vertices[aux[3]][0] - vertices[aux[2]][0], vertices[aux[3]][1] - vertices[aux[2]][1], vertices[aux[3]][2] - vertices[aux[2]][2]]

            res = np.cross(vecA, vecB)
            normals[aux[1]][0] += res[0]  
            normals[aux[1]][1] += res[1]  
            normals[aux[1]][2] += res[2]  

            normals[aux[2]][0] += res[0]  
            normals[aux[2]][1] += res[1]  
            normals[aux[2]][2] += res[2]  

            normals[aux[3]][0] += res[0]  
            normals[aux[3]][1] += res[1]  
            normals[aux[3]][2] += res[2]  
        #print(faces)
        norms = np.linalg.norm(normals,axis=1)
        normals = normals/norms[:,None]

        color = np.asarray(color)
        color = np.tile(color, (numVertices, 1))

        vertexData = np.concatenate((vertices, color), axis=1)
        vertexData = np.concatenate((vertexData, normals), axis=1)

        #print(vertexData.shape)

        indices = []
        vertexDataF = []
        index = 0

        for face in faces:
            vertex = vertexData[face[0],:]
            vertexDataF += vertex.tolist()
            vertex = vertexData[face[1],:]
            vertexDataF += vertex.tolist()
            vertex = vertexData[face[2],:]
            vertexDataF += vertex.tolist()
            
            indices += [index, index + 1, index + 2]
            index += 3        



        return Shape(vertexDataF, indices)


def generateT(t):
    return np.array([[1, t, t**2, t**3]]).T


#Matriz de hermite para poder mover al auto
def hermiteMatrix(P1, P2, T1, T2):
    # Generate a matrix concatenating the columns
    G = np.concatenate((P1, P2, T1, T2), axis=1)

    # Hermite base matrix is a constant
    Mh = np.array([[1, 0, -3, 2], [0, 0, 3, -2], [0, 1, -2, 1], [0, 0, -1, 1]])

    return np.matmul(G, Mh)



#Aca se divide cada curva en una cantidad N para que el auto se mueva con el tiempo
# M is the cubic curve matrix, N is the number of samples between 0 and 1
def evalCurve(M, N):
    # The parameter t should move between 0 and 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in T2 for each sample will be stored here
    curve = np.ndarray(shape=(N, 3), dtype=float)
    
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(M, T).T
        
    return curve


#TAREA5: Función para generar la curva de la aplicación
def generateCurveT5(N):
    
    #Linea Recta en Y positivo a lo largo de X
    P1 = np.array([[-8.25, 3.7, 0]]).T
    P2 = np.array([[3.5, 3.7, 0]]).T
    T1 = np.array([[1, 0, 0]]).T
    T2 = np.array([[1, 0, 0]]).T
    
    H1 = hermiteMatrix(P1, P2, T1, T2)
    hermiteRecta1 = evalCurve(H1, N)

    #Linea curva 1
    P1 = np.array([[3.5, 3.7, 0]]).T
    P2 = np.array([[3.7, 3.2, 0]]).T
    T1 = np.array([[1, 0, 0]]).T
    T2 = np.array([[0, -1, 0]]).T
    
    H2 = hermiteMatrix(P1, P2, T1, T2)
    hermiteCurva1 = evalCurve(H2, N)

    #Recta en X positivo a lo largo de Y
    P1 = np.array([[3.7, 3.2, 0]]).T
    P2 = np.array([[3.7, -0.3, 0]]).T
    T1 = np.array([[0, -1, 0]]).T
    T2 = np.array([[0, -1, 0]]).T
    
    H3 = hermiteMatrix(P1, P2, T1, T2)
    hermiteRecta2 = evalCurve(H3, N)


    #segunda curva
    P1 = np.array([[3.7, -0.3, 0]]).T
    P2 = np.array([[3.15, -0.75, 0]]).T
    T1 = np.array([[0, -1, 0]]).T
    T2 = np.array([[-1, 0, 0]]).T
    
    H4 = hermiteMatrix(P1, P2, T1, T2)
    hermiteCurva2 = evalCurve(H4, N)

    #Recta en Y negativo a lo largo de X
    P1 = np.array([[3.15, -0.75, 0]]).T
    P2 = np.array([[-2.35, -0.75, 0]]).T
    T1 = np.array([[-1, 0, 0]]).T
    T2 = np.array([[-1, 0, 0]]).T
    
    H5 = hermiteMatrix(P1, P2, T1, T2)
    hermiteRecta3 = evalCurve(H5, N)

    #Curva 3
    P1 = np.array([[-2.35, -0.75, 0]]).T
    P2 = np.array([[-3.45, -0.3, 0]]).T
    T1 = np.array([[-1, 0, 0]]).T
    T2 = np.array([[-1, 1, 0]]).T
    
    H6 = hermiteMatrix(P1, P2, T1, T2)
    hermiteCurva3 = evalCurve(H6, N)

    #Recta diagonal
    P1 = np.array([[-3.45, -0.3, 0]]).T
    P2 = np.array([[-8.95, 3.25, 0]]).T
    T1 = np.array([[-1, 1, 0]]).T
    T2 = np.array([[-1, 1, 0]]).T
    
    H7 = hermiteMatrix(P1, P2, T1, T2)
    hermiteRecta4 = evalCurve(H7, N)

    #Curva 4
    P1 = np.array([[-8.95, 3.25, 0]]).T
    P2 = np.array([[-8.25, 3.7, 0]]).T
    T1 = np.array([[-1, 1, 0]]).T
    T2 = np.array([[1, 0, 0]]).T
    
    H8 = hermiteMatrix(P1, P2, T1, T2)
    hermiteCurva4 = evalCurve(H8, N)

    # Concatenamos las curvas
    C = np.concatenate((hermiteRecta1, hermiteCurva1, hermiteRecta2, hermiteCurva2, hermiteRecta3, hermiteCurva3, hermiteRecta4, hermiteCurva4 ), axis=0)

    return C

