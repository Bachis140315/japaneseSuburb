# coding=utf-8
import copy

import sys


from pyrsistent import v
from assets_path import getAssetPath
from math import *
from operator import mod
import scene_graph as sg
import glfw
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from OpenGL.GL import *
from easy_shaders import *
from basic_shapes import *
import numpy as np
import transformations as tr
import lighting_shaders as ls
from constants import *
from elemento_basicos import *

#Esta clase tiene los parametros para mover la camara, saber si esta mirando para abajo y si se esta en proyeccion aerea 
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.camara_polar_theta=np.pi/4
        self.camara_polar_pos=[-3.0,-1.0,0.55]
        self.camara_polar_radio=1.5
        self.mirar_abajo=0
        self.proyeccion_aerea=0

#Esta clase se encarga de tener los parametros de una luz tipo linterna en unos arrays, con tal de que estos sean pasados a la gpu
#con el shader de multiples luces y estas aparezcan en escena, ademas de que son mas facilmente manipulables
class Spotlight:
    def __init__(self):
        self.ambient = np.array([0,0,0])
        self.diffuse = np.array([0,0,0])
        self.specular = np.array([0,0,0])
        self.constant = 0
        self.linear = 0
        self.quadratic = 0
        self.position = np.array([0,0,0])
        self.direction = np.array([0,0,0])
        self.cutOff = 0
        self.outerCutOff = 0


controller = Controller()

#En este diccionario se guardaran todas las luces tipo linterna
spotlightsPool = dict()

def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return   #
    global controller

    if key == glfw.KEY_M:
       controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
       glfw.set_window_should_close(window, True)

    
    elif key == glfw.KEY_W:#Desactivas el "mirar abajo", directamente debajo, recomiendo usar solo para revisar pisos y cosas asi
        if controller.mirar_abajo==1:
            controller.mirar_abajo=0

    elif key == glfw.KEY_Q: #Activa el mirar abajo
        if controller.mirar_abajo==0:
            controller.mirar_abajo=1

    
    elif key == glfw.KEY_P: #Activa proyeccion aerea estatica sobre el barrio
        if controller.proyeccion_aerea==0:
            controller.proyeccion_aerea=1

    
    elif key == glfw.KEY_O: #Desactiva proyeccion aerea estatica sobre el barrio
        if controller.proyeccion_aerea==1:
            controller.proyeccion_aerea=0


#Esta funcion contendra la luces de los faroles de la calles y del auto
def setLights():
    #Primera luz spotlight que sera la luz para el primer farol
    luz_Farol_1 = Spotlight()
    luz_Farol_1.ambient = np.array([0.02, 0.02, 0.02])
    luz_Farol_1.diffuse = np.array([218/255, 165/255, 91/255])
    luz_Farol_1.specular = np.array([0.0, 0.0, 0.0])
    luz_Farol_1.constant = 0.5
    luz_Farol_1.linear = 0.09
    luz_Farol_1.quadratic = 0.01
    luz_Farol_1.position = np.array([0.0, 0.32-1.0, 1.2*0.5]) # la luz del farol esta ubicado en esta posición
    luz_Farol_1.direction = np.array([0, 0, -1]) #la luz del farol está apuntando perpendicularmente hacia el terreno (Y-, o sea hacia abajo)
    luz_Farol_1.cutOff = np.cos(np.radians(15)) #corte del ángulo para la luz del farol|
    luz_Farol_1.outerCutOff = np.cos(np.radians(45)) #la apertura permitida de la luz es de 45°
                                                #mientras más alto es este ángulo, más se difumina su efecto
    
    spotlightsPool['Luz Farol 1'] = luz_Farol_1 

    luz_Farol_2 = Spotlight()
    luz_Farol_2.ambient = np.array([0.02, 0.02, 0.02])
    luz_Farol_2.diffuse = np.array([218/255, 165/255, 91/255])
    luz_Farol_2.specular = np.array([0.0, 0.0, 0.0])
    luz_Farol_2.constant = 0.5
    luz_Farol_2.linear = 0.09
    luz_Farol_2.quadratic = 0.01
    luz_Farol_2.position = np.array([-2.5, 0.32-1.0, 1.2*0.5])
    luz_Farol_2.direction = np.array([0, 0, -1]) 
    luz_Farol_2.cutOff = np.cos(np.radians(15)) 
    luz_Farol_2.outerCutOff = np.cos(np.radians(45))
                                                
    spotlightsPool['Luz Farol 2'] = luz_Farol_2

    luz_Farol_3 = Spotlight()
    luz_Farol_3.ambient = np.array([0.02, 0.02, 0.02])
    luz_Farol_3.diffuse = np.array([218/255, 165/255, 91/255])
    luz_Farol_3.specular = np.array([0.0, 0.0, 0.0])
    luz_Farol_3.constant = 0.5
    luz_Farol_3.linear = 0.09
    luz_Farol_3.quadratic = 0.01
    luz_Farol_3.position = np.array([3.0, 0.32-1.0, 1.2*0.5]) 
    luz_Farol_3.direction = np.array([0, 0, -1]) 
    luz_Farol_3.cutOff = np.cos(np.radians(15)) 
    luz_Farol_3.outerCutOff = np.cos(np.radians(45)) 
                                                
    spotlightsPool['Luz Farol 3'] = luz_Farol_3

    luz_Farol_4 = Spotlight()
    luz_Farol_4.ambient = np.array([0.02, 0.02, 0.02])
    luz_Farol_4.diffuse = np.array([218/255, 165/255, 91/255])
    luz_Farol_4.specular = np.array([0.0, 0.0, 0.0])
    luz_Farol_4.constant = 0.5
    luz_Farol_4.linear = 0.09
    luz_Farol_4.quadratic = 0.01
    luz_Farol_4.position = np.array([-8.65-0.32, 3.45 , 1.2*0.5]) 
    luz_Farol_4.direction = np.array([0, 0, -1]) 
    luz_Farol_4.cutOff = np.cos(np.radians(15)) 
    luz_Farol_4.outerCutOff = np.cos(np.radians(45)) 
                                                
    spotlightsPool['Luz Farol 4'] = luz_Farol_4

    luz_Farol_5 = Spotlight()
    luz_Farol_5.ambient = np.array([0.02, 0.02, 0.02])
    luz_Farol_5.diffuse = np.array([218/255, 165/255, 91/255])
    luz_Farol_5.specular = np.array([0.0, 0.0, 0.0])
    luz_Farol_5.constant = 0.5
    luz_Farol_5.linear = 0.09
    luz_Farol_5.quadratic = 0.01
    luz_Farol_5.position = np.array([-4.5, 0.38 , 1.2*0.5]) 
    luz_Farol_5.direction = np.array([0, 0, -1]) 
    luz_Farol_5.cutOff = np.cos(np.radians(15)) 
    luz_Farol_5.outerCutOff = np.cos(np.radians(45)) 
                                                
    spotlightsPool['Luz Farol 5'] = luz_Farol_5

    #Luz derecha del auto
    luz_Farol_6 = Spotlight()
    luz_Farol_6.ambient = np.array([0.05, 0.05, 0.05])
    luz_Farol_6.diffuse = np.array([0/255, 0/255, 255/255])
    luz_Farol_6.specular = np.array([1.0, 1.0, 1.0])
    luz_Farol_6.constant = 0.01
    luz_Farol_6.linear = 0.09
    luz_Farol_6.quadratic = 0.0001
    luz_Farol_6.position = np.array([0.0, 0.0, 0.2]) 
    luz_Farol_6.direction = np.array([0.0, 1.0, -0.25]) 
    luz_Farol_6.cutOff = np.cos(np.radians(25)) 
    luz_Farol_6.outerCutOff = np.cos(np.radians(25)) 
                                                
    spotlightsPool['Luz Farol 6'] = luz_Farol_6 

    #Luz izquierda del auto
    luz_Farol_7 = Spotlight()
    luz_Farol_7.ambient = np.array([0.05, 0.05, 0.05])
    luz_Farol_7.diffuse = np.array([255/255, 0/255, 0/255])
    luz_Farol_7.specular = np.array([1.0, 1.0, 1.0])
    luz_Farol_7.constant = 0.01
    luz_Farol_7.linear = 0.09
    luz_Farol_7.quadratic = 0.0001
    luz_Farol_7.position = np.array([0.0, 0.0, 0.2]) 
    luz_Farol_7.direction = np.array([0, 1.0, -0.25]) 
    luz_Farol_7.cutOff = np.cos(np.radians(25)) 
    luz_Farol_7.outerCutOff = np.cos(np.radians(25)) 
                                                
    spotlightsPool['Luz Farol 7'] = luz_Farol_7    
    


#Esto crea las calles que estan alrededor de las casas y en el suburbio
def creando_calles(pipeline, en_y_positivo,cuantas_calles):

    vertices_calle=[
        -0.5, 0.4, 0.0001, 0, 0,    0, 0, 1,
         0.5, 0.4, 0.0001, 1, 0,    0, 0, 1,
        -0.5,-0.4, 0.0001, 0, 1,    0, 0, 1,
         0.5,-0.4, 0.0001, 1, 1,    0, 0, 1
    ]
    indices_calle=[
        0, 1, 2,
        2, 3, 1
    ]

    vertices_puntita=[
         0.0, 0.0,0.0001, 0,0,      0, 0, 1,
         0.0,-0.4,0.0001, 0,1/2,    0, 0, 1,
        -0.2,-0.4,0.0001, 1/2,1/2,  0, 0, 1   
    ]
    indices_puntita=[
        0,1,2
    ]

    shape_puntita=Shape(vertices_puntita, indices_puntita)
    gpu_puntita=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_puntita)
    gpu_puntita.fillBuffers(shape_puntita.vertices,shape_puntita.indices)
    gpu_puntita.texture = textureSimpleSetup(
        getAssetPath("textura_calle.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    shape_calle=Shape(vertices_calle, indices_calle)
    gpu_calle=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_calle)
    gpu_calle.fillBuffers(shape_calle.vertices,shape_calle.indices)
    gpu_calle.texture = textureSimpleSetup(
        getAssetPath("textura_calle.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    Escena_calle=sg.SceneGraphNode("Calles en Y positivo")
    union=sg.SceneGraphNode("Union de las calles")
    calle_diagonal=sg.SceneGraphNode("Calle Diagonal")
    puntita=sg.SceneGraphNode("Puntita")


    for k in range(cuantas_calles):
        calle=sg.SceneGraphNode("Calle")
        calle.transform=tr.matmul([tr.translate(
                -9.25+k*0.5, en_y_positivo, 0.0), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])
        calle.childs +=[gpu_calle]
        union.childs+=[calle]

    for k in range(9):
        calle=sg.SceneGraphNode("Calle")
        calle.transform=tr.matmul([tr.translate(
                3.70, en_y_positivo-0.5*k, 0.001), tr.uniformScale(0.5),tr.rotationZ((np.pi)/2), tr.translate(0.0, 0.0, 0.0)])
        calle.childs +=[gpu_calle]
        union.childs+=[calle]
    
    for k in range(13):
        calle=sg.SceneGraphNode("Calle")
        calle.transform=tr.matmul([tr.translate(
                3.65-k*0.5, -0.75, 0.001), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])
        calle.childs +=[gpu_calle]
        union.childs+=[calle]
    
    for k in range(16):
        calle=sg.SceneGraphNode("Calle")
        calle.transform=tr.matmul([tr.translate(
                (k+1)*-0.5, 0.0, 0.001), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])
        calle.childs +=[gpu_calle]
        calle_diagonal.childs+=[calle]
    
    calle_diagonal.transform=tr.matmul([tr.translate(
                -2.45, -0.885, 0.0), tr.uniformScale(1.0),tr.rotationZ(-(np.pi)/5.5) ,tr.translate(0.0, 0.0, 0.0)])
    union.childs+=[calle_diagonal]

    puntita.transform=tr.matmul([tr.translate(
                -2.60, -0.515, 0.0), tr.uniformScale(1.0) ,tr.translate(0.0, 0.0, 0.0)])
    puntita.childs +=[gpu_puntita]

    union.childs +=[puntita]

    Escena_calle.childs+=[union]    
    return Escena_calle



def main():
    

    
    if not glfw.init():
        glfw.set_window_should_close(window, True)
        return -1

    width = SCREEN_WIDTH
    height = SCREEN_HEIGHT

    window = glfw.create_window(width, height, "Suburbio Japones", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)
        return -1

    glfw.make_context_current(window)

    glfw.set_key_callback(window, on_key)

    #Este pipleine sera unicamente para los ejes de tamaño uno para el X, Y e Z
    pipeline = SimpleModelViewProjectionShaderProgram()

    #Este shader se encarga de darle las insutrcciones correctas con las que debe usar la GPU,
    #en este caso de tienen disintas instrucciones, para la proyeccion, el view y el model.
    #El siguiente es el pipeline para todas las casas y el ambiente general, pues todo tiene texturas
    texPipeline = ls.MultipleLightTexturePhongShaderProgram()
    #Este pipeline es unicamente para el auto, pues es unicamente de color rojo y no tiene texturas
    auto_pipeline = ls.MultipleLightPhongShaderProgram()

    
    

#------------------------------------------------Algunos objetos de la escena------------------------------------


    #Es el piso donde estan los arboles
    vertexData_piso = np.array([
        # positions        # colors     #normals
        -9.5,  3.15,  0.001,  0, 0,     0, 0, 1,
        -9.5, -1.5,   0.001,  0, 1,     0, 0, 1,
        -2.0, -1.5,   0.001,  1, 1,     0, 0, 1

    ], dtype=np.float32)

    indexData_piso = np.array([
        0, 1, 2 

    ])
    #El mapa completo, que se fue ajustando a como iba distribuyendo las casas, muy ineficiente
    vertexData_imagen_asfalto = np.array([
        # positions        
        -9.5, -1.5, 0.0,  0, 1,     0, 0, 1,
         3.9, -1.5, 0.0,  1, 1,     0, 0, 1,
         3.9,  3.5, 0.0,  1, 0,     0, 0, 1,
        -9.5,  3.5, 0.0,  0, 0,     0, 0, 1]
    , dtype=np.float32)

    indexData_imagen_asfalto = np.array([
        0, 1, 2, 
        0, 3, 2

    ])

    #Pequeño jardin para la casa 21 y 7, que son las que tienen un pequeño verde alrededor de ellas
    vertices_pasto_casa_21 = np.array([
        # positions        
        -1.025,   1.25, 0.001,  0, 0,   0, 0, 1,
        -1.025,  -0.5,  0.001,  0, 1,   0, 0, 1,
         -0.225,   1.25,  0.001,  1, 0,  0, 0, 1,
         -0.225,   -0.5,  0.001,  1, 1,  0, 0, 1

    ], dtype=np.float32)

    indices_pasto_casa_21 = np.array([
        0, 1, 2,
        2, 3 ,1 

    ])

    vertices_pasto_casa_7 = np.array([
        # positions        # textura        #normals
        -2.85,    3.1, 0.001,  0, 0,        0, 0, 1,
        -2.85,    2.0,   0.001,  0, 1,      0, 0, 1,
        -2.15,    3.1, 0.001,  1, 0,        0, 0, 1,
        -2.15,    2.0,   0.001,  1, 1,      0, 0, 1

    ], dtype=np.float32)

    indices_pasto_casa_7 = np.array([
        0, 1, 2,
        2, 3 ,1 

    ])

    shape_piso=Shape(vertexData_imagen_asfalto, indexData_imagen_asfalto)
    gpu_piso=GPUShape().initBuffers()
    texPipeline.setupVAO(gpu_piso)
    gpu_piso.fillBuffers(shape_piso.vertices,shape_piso.indices)
    gpu_piso.texture = textureSimpleSetup(
        getAssetPath("textura-asfatica.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    shape_pasto_verde=Shape(vertexData_piso, indexData_piso)
    gpu_pasto_verde=GPUShape().initBuffers()
    texPipeline.setupVAO(gpu_pasto_verde)
    gpu_pasto_verde.fillBuffers(shape_pasto_verde.vertices,shape_pasto_verde.indices)
    gpu_pasto_verde.texture = textureSimpleSetup(
        getAssetPath("pasto_verde.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    

    shape_pasto_casa_21=Shape(vertices_pasto_casa_21, indices_pasto_casa_21)
    gpu_pasto_casa_21=GPUShape().initBuffers()
    texPipeline.setupVAO(gpu_pasto_casa_21)
    gpu_pasto_casa_21.fillBuffers(shape_pasto_casa_21.vertices,shape_pasto_casa_21.indices)
    gpu_pasto_casa_21.texture = textureSimpleSetup(
        getAssetPath("pasto_verde.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
   
    shape_pasto_casa_7=Shape(vertices_pasto_casa_7, indices_pasto_casa_7)
    gpu_pasto_casa_7=GPUShape().initBuffers()
    texPipeline.setupVAO(gpu_pasto_casa_7)
    gpu_pasto_casa_7.fillBuffers(shape_pasto_casa_7.vertices,shape_pasto_casa_7.indices)
    gpu_pasto_casa_7.texture = textureSimpleSetup(
        getAssetPath("pasto_verde.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    shapeauto = readOBJ(getAssetPath('datsun280Z.obj'), (1.0, 0.0, 0.0))
    gpuauto = GPUShape().initBuffers()
    auto_pipeline.setupVAO(gpuauto)
    gpuauto.fillBuffers(shapeauto.vertices, shapeauto.indices)

    
    

#-------------------------------Fin de algunos objetos de la escena------------------------------------------------

#------------------------------------------Ejes hechos a manos de largo 1------------------------------------------

    #Se dibujaron los ejes x/y/z para tener una mejor persepcion de donde esta uno
    eje_x=Shape([0.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0],[0,1,0])
    gpu_eje_x=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_eje_x)
    gpu_eje_x.fillBuffers(eje_x.vertices,eje_x.indices)

    eje_y=Shape([0.0,0.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0],[0,1,0])
    gpu_eje_y=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_eje_y)
    gpu_eje_y.fillBuffers(eje_y.vertices,eje_y.indices)

    eje_z=Shape([0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0],[0,1,0])
    gpu_eje_z=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_eje_z)
    gpu_eje_z.fillBuffers(eje_z.vertices,eje_z.indices)
    

#---------------------------------Fin de los ejes hechos a mano--------------------------------------------

#   glClearColor(0.450, 0.756, 0.909, 1.0)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    setLights()



    #----------------------------------------Calles---------------------------------------------
    Calles_y_positivo=creando_calles(texPipeline,3.7,26)


    #----------------------------------------ARBOLES--------------------------------------------
    Arbol1=creandoArbol(texPipeline,"verde_azulado.jpg")
    Arbol1.transform = tr.matmul([tr.translate(
                -9.5+6.75, -1.25, 0.001), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])
    Arbol2=creandoArbol(texPipeline,"hojas_rojas.jpg")
    Arbol2.transform = tr.matmul([tr.translate(
                -9.5+4.75, -1.25, 0.001), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])
    Arbol3=creandoArbol(texPipeline,"hojas_amarillas.jpg")
    Arbol3.transform = tr.matmul([tr.translate(
                -9.5+2.75, -1.25, 0.001), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])
    Arbol4=creandoArbol(texPipeline,"verde.jpg")
    Arbol4.transform = tr.matmul([tr.translate(
                -9.5+0.75, -1.25, 0.001), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])
    Arbol5=creandoArbol(texPipeline,"naranjo_otono.jpg")
    Arbol5.transform = tr.matmul([tr.translate(
                -9.5+4.75, -0.5, 0.001), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])
    Arbol6=creandoArbol(texPipeline,"verde.jpg")
    Arbol6.transform = tr.matmul([tr.translate(
                -9.5+2.75, -0.5, 0.001), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])
    Arbol7=creandoArbol(texPipeline,"hojas_amarillas.jpg")
    Arbol7.transform = tr.matmul([tr.translate(
                -9.5+0.75, -0.5, 0.001), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])
    Arbol8=creandoArbol(texPipeline,"verde_azulado.jpg")
    Arbol8.transform = tr.matmul([tr.translate(
                -9.5+0.75, 0.75, 0.001), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])
    Arbol9=creandoArbol(texPipeline,"verde_grisaseo.jpg")
    Arbol9.transform = tr.matmul([tr.translate(
                -9.5+0.75, 1.75, 0.001), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])
    Arbol10=creandoArbol(texPipeline,"verde.jpg")
    Arbol10.transform = tr.matmul([tr.translate(
                -9.5+1.75, 1.75, 0.001), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])
    Arbol11=creandoArbol(texPipeline,"hojas_amarillas.jpg")
    Arbol11.transform = tr.matmul([tr.translate(
                -9.5+0.75, 1.25, 0.001), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])
    Arbol12=creandoArbol(texPipeline,"verde_azulado.jpg")
    Arbol12.transform = tr.matmul([tr.translate(
                -9.5+1.75, 1.25, 0.001), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])
    Arbol13=creandoArbol(texPipeline,"verde_grisaseo.jpg")
    Arbol13.transform = tr.matmul([tr.translate(
                -9.5+1.75, 0.75, 0.001), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])
    Arbol14=creandoArbol(texPipeline,"hojas_rojas.jpg")
    Arbol14.transform = tr.matmul([tr.translate(
                -9.5+1.75, 0.25, 0.001), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])
    Arbol15=creandoArbol(texPipeline,"naranjo_otono.jpg")
    Arbol15.transform = tr.matmul([tr.translate(
                -9.5+0.75, 0.25, 0.001), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])
    Arbol16=creandoArbol(texPipeline,"verde_azulado.jpg")
    Arbol16.transform = tr.matmul([tr.translate(
                -9.5+1.75, -0.5, 0.001), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])
    Arbol17=creandoArbol(texPipeline,"pasto_verde.jpg")
    Arbol17.transform = tr.matmul([tr.translate(
                -9.5+1.75, -1.25, 0.001), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])
    #------------------------------------ARBOLITOS PARA CASAS----------------------------------
    Arbol18=creandoArbol(texPipeline,"verde.jpg")
    Arbol18.transform = tr.matmul([tr.translate(
                -2.55, 2.55, 0.001), tr.uniformScale(0.2), tr.translate(0.0, 0.0, 0.0)])
    Arbol19=creandoArbol(texPipeline,"verde.jpg")
    Arbol19.transform = tr.matmul([tr.translate(
                -2.35, 2.55, 0.001), tr.uniformScale(0.2), tr.translate(0.0, 0.0, 0.0)])
    Arbol20=creandoArbol(texPipeline,"verde.jpg")
    Arbol20.transform = tr.matmul([tr.translate(
                -0.6, 0.35, 0.001), tr.uniformScale(0.2), tr.translate(0.0, 0.0, 0.0)])
    Arbol21=creandoArbol(texPipeline,"verde.jpg")
    Arbol21.transform = tr.matmul([tr.translate(
                -0.5, 0.0, 0.001), tr.uniformScale(0.2), tr.translate(0.0, 0.0, 0.0)])
    Arbol22=creandoArbol(texPipeline,"verde.jpg")
    Arbol22.transform = tr.matmul([tr.translate(
                -0.7, 0.0, 0.001), tr.uniformScale(0.2), tr.translate(0.0, 0.0, 0.0)])



    #----------------------------------------CASAS----------------------------------------------
    Casa_1=creandoParedes(texPipeline,1,"pared_casa_1.jpg","pared_casa_1.jpg","plano",1,1)
    Casa_1.transform = tr.matmul([tr.translate(
                -8.0+1.75, 0.85, 0.001), tr.uniformScale(0.5),tr.rotationZ(-(np.pi)/6.0) ,tr.translate(0.0, 0.0, 0.0)])

    Casa_2=creandoParedes(texPipeline,2,"pared_casa_2.jpg","pared_casa_2.jpg","plano",1,2)
    Casa_2.transform = tr.matmul([tr.translate(
                -8.0+0.5, 3.25, 0.0), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])

    Casa_3=creandoParedes(texPipeline,2,"pared_casa_3.jpg","techo_casa_3.jpg","triangular",1)
    Casa_3.transform = tr.matmul([tr.translate(
                -8.0+1.5, 3.25, 0.0), tr.uniformScale(0.5),tr.rotationZ((np.pi/2)) ,tr.translate(0.0, 0.0, 0.0)])

    Casa_4=creandoParedes(texPipeline,2,"pared_casa_4.jpg","techo_casa_4.jpg","triangular",1)
    Casa_4.transform = tr.matmul([tr.translate(
                -8.0+2.5, 3.25, 0.0), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])
    agregado_Casa_4=creando_techo_triangular_chico(texPipeline,"techo_japones_antiguo.jpg")
    agregado_Casa_4.transform=tr.matmul([tr.translate(
                -8.0+2.5, 3.45, 0.0), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])

    Casa_5=creandoParedes(texPipeline,1,"pared_casa_5.jpg","techo_casa_5.jpg","triangular",1,5)
    Casa_5.transform = tr.matmul([tr.translate(
                -8.0+3.5, 3.25, 0.0), tr.uniformScale(0.5),tr.rotationZ((np.pi)/2),tr.translate(0.0, 0.0, 0.0)])

    Casa_6=creandoParedes(texPipeline,2,"pared_casa_6.jpg","techo_casa_6.jpg","plano",1)
    Casa_6.transform = tr.matmul([tr.translate(
                -8.0+4.5, 3.25, 0.0), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])

    Casa_7=creandoParedes(texPipeline,2,"pared_casa_7.jpg","techo_casa_7.jpg","triangular",1)
    Casa_7.transform = tr.matmul([tr.translate(
                -8.0+5.5, 3.25, 0.0), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])
    
    Casa_8=creandoParedes(texPipeline,2,"pared_madera.jpg","techo_casa_8.jpg","triangular",1)
    Casa_8.transform = tr.matmul([tr.translate(
                -8.0+6.5, 3.25, 0.0), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])

    Casa_9=creandoParedes(texPipeline,2,"pared_casa_9.jpg","techo_casa_9.jpg","triangular",1,9)
    Casa_9.transform = tr.matmul([tr.translate(
                -8.0+7.5, 3.25, 0.0), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])
    agregado_Casa_9=creando_techo_triangular_chico(texPipeline,"techo_japones_antiguo.jpg")
    agregado_Casa_9.transform=tr.matmul([tr.translate(
                -8.0+7.5, 3.4, -0.05), tr.uniformScale(0.6), tr.translate(0.0, 0.0, 0.0)])

    Casa_10=creandoParedes(texPipeline,2,"pared_casa_10.jpg","techo_casa_10.jpg","triangular",1,10)
    Casa_10.transform = tr.matmul([tr.translate(
                -8.0+9.25, 2.85, 0.0), tr.uniformScale(0.8), tr.translate(0.0, 0.0, 0.0)])
    
    Casa_11=creandoParedes(texPipeline,2,"pared_casa_11.jpg","techo_casa_11.jpg","triangular",1,11)
    Casa_11.transform = tr.matmul([tr.translate(
                -8.0+10.5, 3.25, 0.0), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])
    agregado_Casa_11=creandoParedes(texPipeline,1,"pared_casa_11.jpg","pared_casa_11.jpg","triangular",1,11)
    agregado_Casa_11.transform=tr.matmul([tr.translate(
                -8.0+10.75, 3.25, 0.0), tr.uniformScale(0.3), tr.translate(0.0, 0.0, 0.0)])
    
    Casa_12=creandoParedes(texPipeline,2,"pared_casa_12.jpg","techo_casa_12.jpg","triangular",1,12)
    Casa_12.transform = tr.matmul([tr.translate(
                -8.0+10.5, 3.25-1.0, 0.0), tr.uniformScale(0.5),tr.rotationZ(-(np.pi/2)) , tr.translate(0.0, 0.0, 0.0)])
    agregado_Casa_12=creando_techo_triangular_chico(texPipeline,"techo_japones_antiguo.jpg")
    agregado_Casa_12.transform=tr.matmul([tr.translate(
                -8.0+10.7, 3.25-0.9, 0.005), tr.uniformScale(0.25),tr.rotationZ(-(np.pi/2)), tr.translate(0.0, 0.0, 0.0)])

    Casa_13=creandoParedes(texPipeline,2,"pared_casa_13.jpg","techo_casa_13.jpg","triangular",1,13)
    Casa_13.transform = tr.matmul([tr.translate(
                -8.0+10.5, 3.25-2.0, 0.0), tr.uniformScale(0.5), tr.rotationZ(-(np.pi/2)) ,tr.translate(0.0, 0.0, 0.0)])

    Casa_14=creandoParedes(texPipeline,2,"pared_casa_14.jpg","techo_casa_14.jpg","triangular",1,14)
    Casa_14.transform = tr.matmul([tr.translate(
                -8.0+10.5, 3.25-3.0, 0.0), tr.uniformScale(0.5),tr.rotationZ(-(np.pi/2)) , tr.translate(0.0, 0.0, 0.0)])
    
    Casa_15=creandoParedes(texPipeline,2,"pared_casa_15.jpg","techo_casa_15.jpg","plano",1,15)
    Casa_15.transform = tr.matmul([tr.translate(
                -8.0+9.5, 3.25-3.0, 0.0), tr.uniformScale(0.5),tr.rotationZ((np.pi)) , tr.translate(0.0, 0.0, 0.0)])

    Casa_16=creandoParedes(texPipeline,2,"pared_casa_16.jpg","techo_casa_16.jpg","triangular",2)
    Casa_16.transform = tr.matmul([tr.translate(
                -8.0+8.5, 3.25-3.0, 0.0), tr.uniformScale(0.5) , tr.translate(0.0, 0.0, 0.0)])

    Casa_17=creandoParedes(texPipeline,2,"pared_casa_17.jpg","techo_casa_17.jpg","triangular",2)
    Casa_17.transform = tr.matmul([tr.translate(
                -8.0+6.0, 3.25-3.0, 0.0), tr.uniformScale(0.5) , tr.translate(0.0, 0.0, 0.0)])
    agregado_Casa_17=creandoParedes(texPipeline,1,"pared_casa_17.jpg","techo_casa_17.jpg","triangular",1,17)
    agregado_Casa_17.transform=tr.matmul([tr.translate(
                -8.0+6.15, 3.25-2.825, 0.5), tr.uniformScale(0.4),tr.rotationZ((np.pi)/2) , tr.translate(0.0, 0.0, 0.0)])

    Casa_18=creandoParedes(texPipeline,2,"pared_casa_18.jpg","techo_casa_18.jpg","triangular",1,18)
    Casa_18.transform = tr.matmul([tr.translate(
                -8.0+4.5, 3.25-2.5, 0.0), tr.uniformScale(0.5),tr.rotationZ((np.pi)) , tr.translate(0.0, 0.0, 0.0)])

    Casa_19=creandoParedes(texPipeline,2,"pared_casa_19.jpg","techo_casa_19.jpg","triangular",1,19)
    Casa_19.transform = tr.matmul([tr.translate(
                -8.0+3.0, 3.25-1.75, 0.0), tr.uniformScale(0.5),tr.rotationZ((np.pi)) , tr.translate(0.0, 0.0, 0.0)])
        
    Casa_20=creandoParedes(texPipeline,2,"pared_casa_20.jpg","techo_casa_20.jpg","triangular",1)
    Casa_20.transform = tr.matmul([tr.translate(
                -8.0+1.75, 3.25-1.0, 0.0), tr.uniformScale(0.5),tr.rotationZ((np.pi)) , tr.translate(0.0, 0.0, 0.0)])
    Casa_21=creandoParedes(texPipeline,2,"pared_tatami.jpg","techo_casa_21.jpg","triangular",1)
    Casa_21.transform = tr.matmul([tr.translate(
                -8.0+7.375, 3.25-2.0, 0.0), tr.uniformScale(0.8),tr.rotationZ((np.pi)) , tr.translate(0.0, 0.0, 0.0)])
    Casa_22=creandoParedes(texPipeline,1,"division_pisos.jpg","techo_casa_22.jpg","triangular",1)
    Casa_22.transform = tr.matmul([tr.translate(
                -8.0+8.25, 2.85, 0.0), tr.uniformScale(0.4), tr.translate(0.0, 0.0, 0.0)])
    

    #-----------------------------------------------Objetos con luz---------------------------------
    Farol_1=creandoFarol(texPipeline)
    Farol_1.transform = tr.matmul([tr.translate(
                0.0, -1.0, 0.0), tr.scale(1.0, 1.0, 0.5), tr.translate(0.0, 0.0, 0.0)])
    Farol_2=creandoFarol(texPipeline)
    Farol_2.transform = tr.matmul([tr.translate(
                -2.5, -1.0, 0.0), tr.scale(1.0, 1.0, 0.5), tr.translate(0.0, 0.0, 0.0)])
    Farol_3=creandoFarol(texPipeline)
    Farol_3.transform = tr.matmul([tr.translate(
                3.0, -1.0, 0.0), tr.scale(1.0, 1.0, 0.5), tr.translate(0.0, 0.0, 0.0)])
    Farol_4=creandoFarol(texPipeline)
    Farol_4.transform = tr.matmul([tr.translate(
                -8.65, 3.45, 0.0), tr.scale(1.0, 1.0, 0.5), tr.rotationZ((np.pi/2)) ,tr.translate(0.0, 0.0, 0.0)])
    Farol_5=creandoFarol(texPipeline)
    Farol_5.transform = tr.matmul([tr.translate(
                -4.25, 0.65, 0.0), tr.scale(1.0, 1.0, 0.5), tr.rotationZ((np.pi/2 + np.pi/4)) ,tr.translate(0.0, 0.0, 0.0)])
    

    #Estas variables son para mover las luces que son parte del auto y tener directamente su posicion y direccion
    luz_auto_izq_pos = np.append(spotlightsPool['Luz Farol 7'].position, 1)
    luz_auto_der_pos = np.append(spotlightsPool['Luz Farol 6'].position, 1)
    luz_auto_izq_direc = np.append(spotlightsPool['Luz Farol 7'].direction, 1)
    luz_auto_der_direc = np.append(spotlightsPool['Luz Farol 6'].direction, 1)
    
    
    #-------------------------------------------------------------------------------------------------
    t0 = glfw.get_time()

    #Este es el angulo para el periodo del sol y la luna
    theta_ciclo_sol=(2*np.pi)/48
    
    #Estas variables son para el movimiento del auto alrededor de una escena a traves de una curva Hermite
    N=50
    curva_auto=generateCurveT5(N)
    step=0
    

    #Variables que nos serviran para printear la hora
    horario=0
    hora_anterior=0



    while not glfw.window_should_close(window):


        glfw.poll_events()

        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        horario=int(t1%48)
        hora=int(horario/2) + 6

        #Estas condiciones son para que las luces se prendan a las 18:00
        #que es la hora en donde cae el sol, ademas de que barrido pi
        if (20*np.sin(theta_ciclo_sol*(t1%48)))>0:
            for i in range(5):
                baseString = "Luz Farol " +str(i+1)
                spotlightsPool[baseString].diffuse=np.array([0,0,0])

            spotlightsPool["Luz Farol 6"].diffuse=np.array([0,0,0])
            spotlightsPool["Luz Farol 7"].diffuse=np.array([0,0,0])
            spotlightsPool["Luz Farol 6"].direction[2]=1.0
            spotlightsPool["Luz Farol 7"].direction[2]=1.0
    
        else:
            for i in range(5):
                baseString = "Luz Farol " +str(i+1)
                spotlightsPool[baseString].diffuse=np.array([218/255, 165/255, 91/255])

            spotlightsPool["Luz Farol 6"].diffuse=np.array([0,0,1.0])
            spotlightsPool["Luz Farol 7"].diffuse=np.array([1.0,0,0])
            spotlightsPool["Luz Farol 6"].direction[2]=-0.25
            spotlightsPool["Luz Farol 7"].direction[2]=-0.25

        #Condicion para printear la hora en un periodo de 48 segundos; 6:00 amanece,
        #12:00 en lo mas alto el sol, 18:00 se esconde el sol, 24:00 en lo mas alto la luna,
        #que en este caso de hizo roja para que diferencie un poco del sol y finalmente vuelve a 
        #las 6:00 donde amanece nuevamente
        if (horario)%2 ==0 and hora_anterior!=hora :
            print(str((hora%24))+":00")
            hora_anterior=hora

        
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        

        #Con esto aumentamos el theta que esta en controller que es el theta de la camara polar
        if (glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS):
            controller.camara_polar_theta += 2 * dt

        if (glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS):
            controller.camara_polar_theta -= 2 * dt
        #Con esto hacemos avanzar al "ojo" y el hacia donde estamos mirando al mismo tiempo
        if (glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS):
            controller.camara_polar_pos[0] += np.cos(controller.camara_polar_theta) * dt 
            controller.camara_polar_pos[1] += np.sin(controller.camara_polar_theta) * dt

        if (glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS):
            controller.camara_polar_pos[0] -= np.cos(controller.camara_polar_theta) * dt 
            controller.camara_polar_pos[1] -= np.sin(controller.camara_polar_theta) * dt     
        #Sube la camara
        if (glfw.get_key(window, glfw.KEY_Z) == glfw.PRESS):
            controller.camara_polar_pos[2] +=  dt/2
        #Baja la camara
        if (glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS):
            controller.camara_polar_pos[2] -=  dt/2

        
        
        #Para cambiar de la camara polar a proyeccion aerea
        if controller.proyeccion_aerea==1:
            
            view = tr.lookAt(
            np.array([-4.0, 0.0, 30.0]),
            np.array([-4.0, 1.0, 0.0]),
            np.array([0,0,1]))
        else:
            view = tr.lookAt(
            np.array([controller.camara_polar_pos[0], controller.camara_polar_pos[1], controller.camara_polar_pos[2]]),
            np.array([controller.camara_polar_pos[0] + np.cos(controller.camara_polar_theta)*controller.camara_polar_radio,
            controller.camara_polar_pos[1] + np.sin(controller.camara_polar_theta)*controller.camara_polar_radio,
            controller.camara_polar_pos[2]-controller.mirar_abajo*5]),
            np.array([0,0,1]))
         
  
        projection = tr.perspective(20, float(width)/float(height), 0.1, 100)


        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    
        
        glUseProgram(texPipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(texPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
    
        #Estas matrices son mandadas al pipeline y luego a la gpu, con los parametros de las luces ambientes
        #Estos son matrices pertenecientes al sol
        glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].ambient"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].diffuse"), 255/255, 241/255, 164/255)
        glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].specular"), 1.0, 1.0, 1.0)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].constant"), 0.0001)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].linear"), 0.0009)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].quadratic"), 0.0015)
        glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].position"), 20*np.cos(theta_ciclo_sol*(t1%48)), 0, 20*np.sin(theta_ciclo_sol*(t1%48)))
        #Estos son matrices pertenecientes a la luna

        glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[1].ambient"), 0.1, 0.1, 0.1)
        glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[1].diffuse"), 131/255, 0/255, 0/255)
        glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[1].specular"), 0.1, 0.1, 0.1)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[1].constant"), 0.1)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[1].linear"), 0.1)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[1].quadratic"), 0.01)
        glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[1].position"), -20*np.cos(theta_ciclo_sol*(t1%48)), 0, -20*np.sin(theta_ciclo_sol*(t1%48)))

        #Estas ultimas son los parametros de los materiales, es decir las casas y objetos que son parte de la escena
        glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "material.ambient"), 0.1, 0.1, 0.1)
        glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "material.diffuse"), 0.9, 0.0, 0.0)
        glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "material.specular"), 1.0, 1.0, 1.0)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "material.shininess"), 32)

        #Este for manda las instrucciones y parametros de las luces tipo linterna que se crearon en setLights
        for i, (k,v) in enumerate(spotlightsPool.items()):
                baseString = "spotLights[" + str(i) + "]."
                glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "ambient"), 1, v.ambient)
                glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "diffuse"), 1, v.diffuse)
                glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "specular"), 1, v.specular)
                glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "constant"), v.constant)
                glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "linear"), 0.09)
                glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "quadratic"), 0.032)
                glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "position"), 1, v.position)
                glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "direction"), 1, v.direction)
                glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "cutOff"), v.cutOff)
                glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "outerCutOff"), v.outerCutOff)

        

        glUseProgram(texPipeline.shaderProgram)

        #Caso para que no se salga del numero de N que divide a cada curva Hermite
        if step >= N*8-2:
            step=0
       
        #Esta variable crea el angulo de rotacion cuando se encuentra en una curva de Hermite para el auto y sus luces
        rotando_auto=np.arctan2(curva_auto[step+1,0]-curva_auto[step,0], curva_auto[step+1,1]-curva_auto[step,1])

        #Estas variables crean las nuevas direcciones hacia donde apuntan las luces dependiendo de la curvatura de la curva de Hermite en la que se esta
        #y se redefinen la direccion de las luces
        direccion_7 = tr.matmul([tr.rotationZ(-rotando_auto), luz_auto_izq_direc])
        direccion_6 = tr.matmul([tr.rotationZ(-rotando_auto), luz_auto_der_direc])
        spotlightsPool["Luz Farol 7"].direction = direccion_7
        spotlightsPool["Luz Farol 6"].direction = direccion_6

        #Mismo caso con la direccion de las luces, pero en este caso con respecto a sus posicion en la curva de Hermite
        nueva_posicion = tr.matmul([tr.translate(curva_auto[step,0],curva_auto[step,1],curva_auto[step,2]),
                                        tr.rotationZ(rotando_auto)])
        posicion_7 = tr.matmul([nueva_posicion, luz_auto_izq_pos])
        posicion_6 = tr.matmul([nueva_posicion, luz_auto_der_pos])
        spotlightsPool["Luz Farol 7"].position = posicion_7
        spotlightsPool["Luz Farol 6"].position = posicion_6

        
        #Caso en que durante 1 frame el angulo que hay en una curva se diferencia mucho de los anteriores, debido normalmente al cambio de rectas
        if abs(rotando_auto-np.arctan2(curva_auto[step+2,0]-curva_auto[step+1,0], curva_auto[step+2,1]-curva_auto[step+1,1]))>0.5:
            step+=1
            
        
        #Paso para hacer avanzar los objetos que siguen la curva de Hermite antes creada
        step +=1


    #---------------------------Fin Configuracion Luces-------------------------------------------------

    #---------------------------Inicio Dibujo Ejes y Objetos--------------------------------------------

        glUseProgram(pipeline.shaderProgram)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection )

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)



        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([
            tr.translate(0.0, 0.0, 0.0),          
            tr.scale(1.0, 1.0, 1.0)
        ]))

        pipeline.drawCall(gpu_eje_x)
        
        pipeline.drawCall(gpu_eje_y)

        pipeline.drawCall(gpu_eje_z)


        glUseProgram(auto_pipeline.shaderProgram)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        #------------------------------------------Auto--------------------------------------------------------
        #Aca se define todo para que el auto, que es sin texturas, salga en escena y las luces que hay creadas incidan sobre el
        glUniformMatrix4fv(glGetUniformLocation(auto_pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection )

        glUniformMatrix4fv(glGetUniformLocation(auto_pipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        glUniform3f(glGetUniformLocation(auto_pipeline.shaderProgram, "pointLights[0].ambient"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(auto_pipeline.shaderProgram, "pointLights[0].diffuse"), 255/255, 241/255, 164/255)
        glUniform3f(glGetUniformLocation(auto_pipeline.shaderProgram, "pointLights[0].specular"), 1.0, 1.0, 1.0)
        glUniform1f(glGetUniformLocation(auto_pipeline.shaderProgram, "pointLights[0].constant"), 0.0001)
        glUniform1f(glGetUniformLocation(auto_pipeline.shaderProgram, "pointLights[0].linear"), 0.0009)
        glUniform1f(glGetUniformLocation(auto_pipeline.shaderProgram, "pointLights[0].quadratic"), 0.0015)
        glUniform3f(glGetUniformLocation(auto_pipeline.shaderProgram, "pointLights[0].position"), 20*np.cos(theta_ciclo_sol*(t1%48)), 0, 20*np.sin(theta_ciclo_sol*(t1%48)))

        glUniform3f(glGetUniformLocation(auto_pipeline.shaderProgram, "pointLights[1].ambient"), 0.1, 0.1, 0.1)
        glUniform3f(glGetUniformLocation(auto_pipeline.shaderProgram, "pointLights[1].diffuse"), 131/255, 0/255, 0/255)
        glUniform3f(glGetUniformLocation(auto_pipeline.shaderProgram, "pointLights[1].specular"), 0.1, 0.1, 0.1)
        glUniform1f(glGetUniformLocation(auto_pipeline.shaderProgram, "pointLights[1].constant"), 0.1)
        glUniform1f(glGetUniformLocation(auto_pipeline.shaderProgram, "pointLights[1].linear"), 0.1)
        glUniform1f(glGetUniformLocation(auto_pipeline.shaderProgram, "pointLights[1].quadratic"), 0.01)
        glUniform3f(glGetUniformLocation(auto_pipeline.shaderProgram, "pointLights[1].position"), -20*np.cos(theta_ciclo_sol*(t1%48)), 0, -20*np.sin(theta_ciclo_sol*(t1%48)))

        glUniform3f(glGetUniformLocation(auto_pipeline.shaderProgram, "material.ambient"), 0.1, 0.1, 0.1)
        glUniform3f(glGetUniformLocation(auto_pipeline.shaderProgram, "material.diffuse"), 0.9, 0.0, 0.0)
        glUniform3f(glGetUniformLocation(auto_pipeline.shaderProgram, "material.specular"), 1.0, 1.0, 1.0)
        glUniform1f(glGetUniformLocation(auto_pipeline.shaderProgram, "material.shininess"), 32)

        for i, (k,v) in enumerate(spotlightsPool.items()):
                baseString = "spotLights[" + str(i) + "]."
                glUniform3fv(glGetUniformLocation(auto_pipeline.shaderProgram, baseString + "ambient"), 1, v.ambient)
                glUniform3fv(glGetUniformLocation(auto_pipeline.shaderProgram, baseString + "diffuse"), 1, v.diffuse)
                glUniform3fv(glGetUniformLocation(auto_pipeline.shaderProgram, baseString + "specular"), 1, v.specular)
                glUniform1f(glGetUniformLocation(auto_pipeline.shaderProgram, baseString + "constant"), v.constant)
                glUniform1f(glGetUniformLocation(auto_pipeline.shaderProgram, baseString + "linear"), 0.09)
                glUniform1f(glGetUniformLocation(auto_pipeline.shaderProgram, baseString + "quadratic"), 0.032)
                glUniform3fv(glGetUniformLocation(auto_pipeline.shaderProgram, baseString + "position"), 1, v.position)
                glUniform3fv(glGetUniformLocation(auto_pipeline.shaderProgram, baseString + "direction"), 1, v.direction)
                glUniform1f(glGetUniformLocation(auto_pipeline.shaderProgram, baseString + "cutOff"), v.cutOff)
                glUniform1f(glGetUniformLocation(auto_pipeline.shaderProgram, baseString + "outerCutOff"), v.outerCutOff)


        #Aca se transporta el auto seguna la curva de Hermite
        glUniformMatrix4fv(glGetUniformLocation(auto_pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([
            tr.translate(curva_auto[step,0],curva_auto[step,1],curva_auto[step,2]), 
            tr.rotationZ(-rotando_auto),          
            tr.uniformScale(0.1),
            tr.rotationZ(np.pi),
            tr.rotationX(np.pi/2)
            
        ]))
        auto_pipeline.drawCall(gpuauto)

       #--------------------------------------Dibujo de casas, pastos, entre otras cosas...-----------------------------------------------
        glUseProgram(texPipeline.shaderProgram) 
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glUniformMatrix4fv(glGetUniformLocation(
            texPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(
            texPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(
            texPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([
            tr.translate(0.0, 0.0, 0.0),          
            tr.scale(1.0, 1.0, 1.0)
        ]))
        texPipeline.drawCall(gpu_piso)
        texPipeline.drawCall(gpu_pasto_verde)
        texPipeline.drawCall(gpu_pasto_casa_21)
        texPipeline.drawCall(gpu_pasto_casa_7)
        
    
        

        sg.drawSceneGraphNode(Calles_y_positivo, texPipeline, "model")
        sg.drawSceneGraphNode(Arbol1, texPipeline, "model")
        sg.drawSceneGraphNode(Arbol2, texPipeline, "model")
        sg.drawSceneGraphNode(Arbol3, texPipeline, "model")
        sg.drawSceneGraphNode(Arbol4, texPipeline, "model")
        sg.drawSceneGraphNode(Arbol5, texPipeline, "model")
        sg.drawSceneGraphNode(Arbol6, texPipeline, "model")
        sg.drawSceneGraphNode(Arbol7, texPipeline, "model")
        sg.drawSceneGraphNode(Arbol8, texPipeline, "model")
        sg.drawSceneGraphNode(Arbol9, texPipeline, "model")
        sg.drawSceneGraphNode(Arbol10, texPipeline, "model")
        sg.drawSceneGraphNode(Arbol11, texPipeline, "model")
        sg.drawSceneGraphNode(Arbol12, texPipeline, "model")
        sg.drawSceneGraphNode(Arbol13, texPipeline, "model")
        sg.drawSceneGraphNode(Arbol14, texPipeline, "model")
        sg.drawSceneGraphNode(Arbol15, texPipeline, "model")
        sg.drawSceneGraphNode(Arbol16, texPipeline, "model")
        sg.drawSceneGraphNode(Arbol17, texPipeline, "model")
        sg.drawSceneGraphNode(Arbol18, texPipeline, "model")
        sg.drawSceneGraphNode(Arbol19, texPipeline, "model")
        sg.drawSceneGraphNode(Arbol20, texPipeline, "model")
        sg.drawSceneGraphNode(Arbol21, texPipeline, "model")
        sg.drawSceneGraphNode(Arbol22, texPipeline, "model")
        sg.drawSceneGraphNode(Casa_1, texPipeline, "model")
        sg.drawSceneGraphNode(Casa_2, texPipeline, "model")
        sg.drawSceneGraphNode(Casa_3, texPipeline, "model")
        sg.drawSceneGraphNode(Casa_4, texPipeline, "model")
        sg.drawSceneGraphNode(agregado_Casa_4, texPipeline, "model")
        sg.drawSceneGraphNode(Casa_5, texPipeline, "model")
        sg.drawSceneGraphNode(Casa_6, texPipeline, "model")
        sg.drawSceneGraphNode(Casa_7, texPipeline, "model")
        sg.drawSceneGraphNode(Casa_8, texPipeline, "model")
        sg.drawSceneGraphNode(Casa_9, texPipeline, "model")
        sg.drawSceneGraphNode(agregado_Casa_9, texPipeline, "model")
        sg.drawSceneGraphNode(Casa_10, texPipeline, "model")
        sg.drawSceneGraphNode(Casa_11, texPipeline , "model")
        sg.drawSceneGraphNode(agregado_Casa_11, texPipeline,"model")
        sg.drawSceneGraphNode(Casa_12, texPipeline, "model")
        sg.drawSceneGraphNode(agregado_Casa_12, texPipeline, "model")
        sg.drawSceneGraphNode(Casa_13, texPipeline, "model")
        sg.drawSceneGraphNode(Casa_14, texPipeline, "model")
        sg.drawSceneGraphNode(Casa_15, texPipeline, "model")
        sg.drawSceneGraphNode(Casa_16, texPipeline, "model")
        sg.drawSceneGraphNode(Casa_17, texPipeline, "model")
        sg.drawSceneGraphNode(agregado_Casa_17, texPipeline, "model")
        sg.drawSceneGraphNode(Casa_18, texPipeline, "model")
        sg.drawSceneGraphNode(Casa_19, texPipeline, "model")
        sg.drawSceneGraphNode(Casa_20, texPipeline, "model")
        sg.drawSceneGraphNode(Casa_21, texPipeline, "model")
        sg.drawSceneGraphNode(Casa_22, texPipeline, "model")

        sg.drawSceneGraphNode(Farol_1, texPipeline, "model")
        sg.drawSceneGraphNode(Farol_2, texPipeline, "model")
        sg.drawSceneGraphNode(Farol_3, texPipeline, "model")
        sg.drawSceneGraphNode(Farol_4, texPipeline, "model")
        sg.drawSceneGraphNode(Farol_5, texPipeline, "model")


        glfw.swap_buffers(window)




    gpu_eje_x.clear()

    gpu_eje_y.clear()

    gpu_eje_z.clear()

    gpu_piso.clear()







    glfw.terminate()

    return 0

if __name__ == "__main__":
    main()


            