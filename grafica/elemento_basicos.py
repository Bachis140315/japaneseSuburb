from __future__ import division
from cmath import log10
from turtle import shape
from venv import create
from basic_shapes import *
import scene_graph as sg
from easy_shaders import *
from assets_path import getAssetPath
import transformations as tr

#Crea paralelepidpedo de largo 2l_x, ancho 2l_y y altura l_z
def creandoParalelepipedo(l_x,l_y,l_z):

    
    vertices = [
        #    positions    textura   normal
        -l_x, -l_y,  0.0,  0, 0,    0, 0, -1,
         l_x, -l_y,  0.0,  1, 0,    0, 0, -1,
        -l_x,  l_y,  0.0,  0, 1,    0, 0, -1,
         l_x,  l_y,  0.0,  1, 1,    0, 0, -1,

        -l_x, -l_y,  l_z,  0, 0,    0, 0,  1,
         l_x, -l_y,  l_z,  1, 0,    0, 0,  1,
        -l_x,  l_y,  l_z,  0, 1,    0, 0,  1,
         l_x,  l_y,  l_z,  1, 1,    0, 0,  1,
        
         l_x, -l_y, l_z,  0, 0,     1, 0, 0,
         l_x,  l_y, l_z,  1, 0,     1, 0, 0,
         l_x, -l_y, 0.0,  0, 1,     1, 0, 0,
         l_x,  l_y, 0.0,  1, 1,     1, 0, 0,

        -l_x, l_y, l_z,  0, 0,      -1, 0, 0,
        -l_x,-l_y, l_z,  1, 0,      -1, 0, 0,
        -l_x, l_y, 0.0,  0, 1,      -1, 0, 0,
        -l_x,-l_y, 0.0,  1, 1,      -1, 0, 0,

        -l_x,-l_y, l_z,  0, 0,      0, -1, 0,
         l_x,-l_y, l_z,  1, 0,      0, -1, 0,
        -l_x,-l_y, 0.0,  0, 1,      0, -1, 0,
         l_x,-l_y, 0.0,  1, 1,      0, -1, 0,

         l_x, l_y, l_z,  0, 0,      0, 1, 0,
        -l_x, l_y, l_z,  1, 0,      0, 1, 0,
         l_x ,l_y, 0.0,  0, 1,      0, 1, 0,
        -l_x, l_y, 0.0,  1, 1,      0, 1, 0

        ]


    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 1,
        4, 5, 6, 6, 7, 5,
        8, 9, 10, 10, 11, 9,
        12, 13, 14, 14, 15, 13,
        16, 17, 18, 18, 19, 17,
        20, 21, 22, 22, 23, 21]

    return Shape(vertices, indices)

#Crea ventana con paralelepipedos
def creandoVentana2(pipeline):
    #creando bordes de la ventana
    shape_Ventana_baja=creandoParalelepipedo(0.05,0.15,0.1)
    gpu_Ventana_baja=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_Ventana_baja)
    gpu_Ventana_baja.fillBuffers(shape_Ventana_baja.vertices, shape_Ventana_baja.indices)
    gpu_Ventana_baja.texture=textureSimpleSetup(
        getAssetPath("pared_madera.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    shape_Ventana_laterales=creandoParalelepipedo(0.05,0.025,0.3)
    gpu_Ventana_laterales=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_Ventana_laterales)
    gpu_Ventana_laterales.fillBuffers(shape_Ventana_laterales.vertices, shape_Ventana_laterales.indices)
    gpu_Ventana_laterales.texture=textureSimpleSetup(
        getAssetPath("pared_madera.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    shape_Vidrio=creandoParalelepipedo(0.0,0.1,0.3)
    gpu_Vidrio=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_Vidrio)
    gpu_Vidrio.fillBuffers(shape_Vidrio.vertices, shape_Vidrio.indices)
    gpu_Vidrio.texture=textureSimpleSetup(
        getAssetPath("ventana_minecraft.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)        

    
    escena_ventana_completa=sg.SceneGraphNode("Ventana")
    union=sg.SceneGraphNode("Union de todo")

    marco_abajo=sg.SceneGraphNode("Marco Bajo")
    marco_arriba=sg.SceneGraphNode("Marco Arriba")
    marco_lateral_izquierdo=sg.SceneGraphNode("Marco Laterial Izquierdo")
    marco_lateral_derecho=sg.SceneGraphNode("Marco Laterial Derecho")
    vidrio=sg.SceneGraphNode("Vidrio")

    marco_abajo.childs += [gpu_Ventana_baja]
    marco_arriba.transform=tr.matmul([tr.translate(
                0.0, 0.0, 0.4), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
    marco_arriba.childs += [gpu_Ventana_baja]
    marco_lateral_izquierdo.transform=tr.matmul([tr.translate(
                0.0, -0.125, 0.1), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
    marco_lateral_izquierdo.childs += [gpu_Ventana_laterales]
    marco_lateral_derecho.transform=tr.matmul([tr.translate(
                0.0, 0.125, 0.1), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
    marco_lateral_derecho.childs += [gpu_Ventana_laterales]
    vidrio.transform=tr.matmul([tr.translate(
                0.0, 0.0, 0.1), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
    vidrio.childs += [gpu_Vidrio]

    union.childs += [marco_abajo]            
    union.childs += [marco_arriba] 
    union.childs += [marco_lateral_izquierdo]
    union.childs += [marco_lateral_derecho]
    union.childs += [vidrio]
    

    escena_ventana_completa.childs += [union]

    return escena_ventana_completa 

#Crea el balcon que tiene algunas casas
def creando_Balcon(pipeline,textura_balcon):
    shape_Pilares=creandoParalelepipedo(0.0125,0.0125,0.65)
    gpu_Pilares=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_Pilares)
    gpu_Pilares.fillBuffers(shape_Pilares.vertices, shape_Pilares.indices)
    gpu_Pilares.texture=textureSimpleSetup(
        getAssetPath(textura_balcon), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    shape_Base=creandoParalelepipedo(0.175,0.05,0.025)
    gpu_Base=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_Base)
    gpu_Base.fillBuffers(shape_Base.vertices, shape_Base.indices)
    gpu_Base.texture=textureSimpleSetup(
        getAssetPath(textura_balcon), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    shape_Pared=creandoParalelepipedo(0.0125,0.05,0.025)
    gpu_Pared=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_Pared)
    gpu_Pared.fillBuffers(shape_Pared.vertices, shape_Pared.indices)
    gpu_Pared.texture=textureSimpleSetup(
        getAssetPath(textura_balcon), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    shape_Barra=creandoParalelepipedo(0.175,0.0125,0.025)
    gpu_Barra=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_Barra)
    gpu_Barra.fillBuffers(shape_Barra.vertices, shape_Barra.indices)
    gpu_Barra.texture=textureSimpleSetup(
        getAssetPath(textura_balcon), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    Escena_completa_balcon=sg.SceneGraphNode("Balcon Completo")
    union=sg.SceneGraphNode("Union de todo")

    Pilar1=sg.SceneGraphNode("Pilar 1")
    Pilar2=sg.SceneGraphNode("Pilar 2")
    Base=sg.SceneGraphNode("Base Balcon")
    Pared1=sg.SceneGraphNode("Pegado a pared 1")
    Pared2=sg.SceneGraphNode("Pegado a pared 2")
    Barra=sg.SceneGraphNode("Barra")

    Pilar1.transform=tr.matmul([tr.translate(
                0.175, 0.075, 0.0), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
    Pilar1.childs += [gpu_Pilares]
    Pilar2.transform=tr.matmul([tr.translate(
                -0.175, 0.075, 0.0), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
    Pilar2.childs += [gpu_Pilares]
    Base.transform=tr.matmul([tr.translate(
                0.0, 0.025, 0.5), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
    Base.childs += [gpu_Base]
    Pared1.transform=tr.matmul([tr.translate(
                0.175, 0.025, 0.625), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
    Pared1.childs += [gpu_Pared]
    Pared2.transform=tr.matmul([tr.translate(
                -0.175, 0.025, 0.625), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
    Pared2.childs += [gpu_Pared]
    Barra.transform=tr.matmul([tr.translate(
                0.0, 0.075, 0.625), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
    Barra.childs += [gpu_Barra]

    union.childs +=[Pilar1]
    union.childs +=[Pilar2]
    union.childs +=[Base]
    union.childs +=[Pared1]
    union.childs +=[Pared2]
    union.childs +=[Barra]

    Escena_completa_balcon.childs += [union]

    return Escena_completa_balcon




#Crea un techo triangular que se le puso arriba de las puertas de las casas
def creando_techo_triangular_chico(pipeline,textura_arriba):
    vertices_techo_triangular_chico_arriba=[
        -0.5 , 0.0, 0.55,  0, 0,   0, (0.05/(0.05**2 + 0.05**2)**(1/2)), (0.05/(0.05**2 + 0.05**2)**(1/2)),
         0.5 , 0.0, 0.55,  1, 0,   0, (0.05/(0.05**2 + 0.05**2)**(1/2)), (0.05/(0.05**2 + 0.05**2)**(1/2)),
        -0.5 , 0.05,0.50,  0, 1,   0, (0.05/(0.05**2 + 0.05**2)**(1/2)), (0.05/(0.05**2 + 0.05**2)**(1/2)),
        0.5 ,  0.05, 0.50, 1, 1,   0, (0.05/(0.05**2 + 0.05**2)**(1/2)), (0.05/(0.05**2 + 0.05**2)**(1/2))
    ]
    indices_techo_triangular_chico_arriba=[
        0, 1, 2,
        2, 3, 1
    ]

    vertices_techo_triangular_chico_abajo=[
        -0.5 , 0.0,  0.50, 0, 0,    0, 0, -1,
         0.5 , 0.0,  0.50, 1, 0,    0, 0, -1,
        -0.5 , 0.05, 0.50, 0, 1,    0, 0, -1,
         0.5 ,  0.05, 0.50, 1, 1,   0, 0, -1
    ]
    indices_techo_triangular_chico_abajo=[
        0, 1, 2,
        2, 3, 1
    ]

    vertices_techo_triangular_chico_laterales=[
        -0.5 , 0.0,  0.55,  0, 0,   -1, 0, 0,
        -0.5 , 0.0,  0.50,  0, 1,   -1, 0, 0,
        -0.5 , 0.05, 0.50,  1, 1,   -1, 0, 0,

         0.5 , 0.0,  0.55,  0, 0,   1, 0, 0,
         0.5 , 0.0,  0.50,  0, 1,   1, 0, 0,
         0.5 , 0.05, 0.50,  1, 1,   1, 0, 0

    ]
    indices_techo_triangular_chico_laterales=[
        0, 1, 2,
        3, 4, 5
    ]

    #Creando objetos
    shape_techo_triangular_chico_arriba=Shape(vertices_techo_triangular_chico_arriba,indices_techo_triangular_chico_arriba)
    gpu_techo_triangular_chico_arriba=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_techo_triangular_chico_arriba)
    gpu_techo_triangular_chico_arriba.fillBuffers(shape_techo_triangular_chico_arriba.vertices, shape_techo_triangular_chico_arriba.indices)
    gpu_techo_triangular_chico_arriba.texture=textureSimpleSetup(
        getAssetPath(textura_arriba), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    shape_techo_triangular_chico_abajo=Shape(vertices_techo_triangular_chico_abajo,indices_techo_triangular_chico_abajo)
    gpu_techo_triangular_chico_abajo=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_techo_triangular_chico_abajo)
    gpu_techo_triangular_chico_abajo.fillBuffers(shape_techo_triangular_chico_abajo.vertices, shape_techo_triangular_chico_abajo.indices)
    gpu_techo_triangular_chico_abajo.texture=textureSimpleSetup(
        getAssetPath("pared_madera.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    shape_techo_triangular_chico_laterales=Shape(vertices_techo_triangular_chico_laterales,indices_techo_triangular_chico_laterales)
    gpu_techo_triangular_chico_laterales=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_techo_triangular_chico_laterales)
    gpu_techo_triangular_chico_laterales.fillBuffers(shape_techo_triangular_chico_laterales.vertices, shape_techo_triangular_chico_laterales.indices)
    gpu_techo_triangular_chico_laterales.texture=textureSimpleSetup(
        getAssetPath("pared_madera.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    escena_completa_techito=sg.SceneGraphNode("Techo Triangular Chico")
    union=sg.SceneGraphNode("Union de Todo")

    parte_arriba=sg.SceneGraphNode("Parte Arriba")
    parte_abajo=sg.SceneGraphNode("Parte Abajo")
    parte_lateral=sg.SceneGraphNode("Parte Lateral")

    parte_arriba.transform=tr.matmul([tr.translate(
                0.0, 0.0, 0.0), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
    parte_arriba.childs += [gpu_techo_triangular_chico_arriba]
    parte_abajo.transform=tr.matmul([tr.translate(
                0.0, 0.0, 0.0), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
    parte_abajo.childs += [gpu_techo_triangular_chico_abajo]
    parte_lateral.transform=tr.matmul([tr.translate(
                0.0, 0.0, 0.0), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
    parte_lateral.childs += [gpu_techo_triangular_chico_laterales]

    union.childs +=[parte_arriba]
    union.childs +=[parte_abajo]
    union.childs +=[parte_lateral]

    escena_completa_techito.childs += [union]

    return escena_completa_techito

#PAREDES SON DE LARGO(EJE X) 1.0, DE ANCHO (EJE Y) 0.8 Y DE ALTURA 0.5
#Va a tener varios parametros, el numero de pisos, textura_paredes, textura_techo, tipo de techo(plano o triangular), y la opcion de casa que se desea crear
#solo seran casas de 2 pisos, pues en el suburbio japones no hay de mas pisos, al menos lo que identifique-
#Ademas de que cada casa tiene una especialidad que se le agrega aquí, como balcon, techos triangulares chicos, etc...
def creandoParedes(pipeline,nr_pisos,textura_paredes,textura_techo,tipo_techo,opcion_de_casa,especialidad_casa_nr=0):

    # Definiendo los vertices de la pared y las coordenadas para la textura
    vertices_pared = [
        #   positions         texture coordinates

        # X+: pared perpendicular al eje x positivo
        0.5, -0.4, 0.0,  1, 1,  1, 0, 0,
        0.5,  0.4, 0.0,  0, 1,  1, 0, 0,
        0.5, -0.4, 0.5,  1, 0,  1, 0, 0,
        0.5,  0.4, 0.5,  0, 0,  1, 0, 0,

        # X-: pared perpendicular al eje x negativo
        -0.5, -0.4, 0.0, 1, 1,  -1, 0, 0,
        -0.5,  0.4, 0.0, 0, 1,  -1, 0, 0,
        -0.5, -0.4, 0.5, 1, 0,  -1, 0, 0,
        -0.5,  0.4, 0.5, 0, 0,  -1, 0, 0,

        # Y+: pared perpendicular al eje y positivo
         0.5,  0.4, 0.0, 1, 1,  0, 1, 0,
        -0.5,  0.4, 0.0, 0, 1,  0, 1, 0,
         0.5,  0.4, 0.5, 1, 0,  0, 1, 0,
        -0.5,  0.4, 0.5, 0, 0,  0, 1, 0,

        # Y-: pared perpendicular al eje y negativo
        -0.5, -0.4, 0.0, 1, 1,  0, -1, 0,
         0.5, -0.4, 0.0, 0, 1,  0, -1, 0,
        -0.5, -0.4, 0.5, 1, 0,  0, -1, 0,
         0.5, -0.4, 0.5, 0, 0,  0, -1, 0 
    ]
    indices_pared = [
        0, 1, 2, 2, 3, 1,  # X+
        4, 5, 6, 6, 7, 5,  # X-
        8, 9, 10,10,11, 9,  # Y+
        12,13,14,14,15,13]  # Y-
    
    #Estos vertices e indices son para el piso de un 2do piso, o de un techo plano de una casa de un piso
    vertices_techo_o_piso=[
        -0.5,  0.4, 0.5, 0, 0,  0, 0, 1,
         0.5,  0.4, 0.5, 1, 0,  0, 0, 1,
        -0.5, -0.4, 0.5, 0, 1,  0, 0, 1,
         0.5, -0.4, 0.5, 1, 1,  0, 0, 1
    ]
    indices_techo_o_piso=[
        0, 1, 2,
        2, 3, 1  
    ]

    #-------------------------------------------------o-----------------------------------------
    #Parte dirigida a los techos para que sean 3D

    vertices_techo_triangular=[
        0.0, -0.4, 0.8, 0, 0,   ((0.55)/((0.55**2 + 0.23**2)**(1/2))), 0, ((0.23)/((0.55**2 + 0.23**2)**(1/2))),
        0.0,  0.4, 0.8, 1, 0,   ((0.55)/((0.55**2 + 0.23**2)**(1/2))), 0, ((0.23)/((0.55**2 + 0.23**2)**(1/2))),
        0.55,-0.4, 0.47, 0, 1,  ((0.55)/((0.55**2 + 0.23**2)**(1/2))), 0, ((0.23)/((0.55**2 + 0.23**2)**(1/2))),
        0.55, 0.4, 0.47, 1, 1,  ((0.55)/((0.55**2 + 0.23**2)**(1/2))), 0, ((0.23)/((0.55**2 + 0.23**2)**(1/2))),

        0.0, -0.4, 0.8, 0, 0,       -((0.55)/((0.55**2 + 0.23**2)**(1/2))), 0, ((0.23)/((0.55**2 + 0.23**2)**(1/2))),
        0.0,  0.4, 0.8, 1, 0,       -((0.55)/((0.55**2 + 0.23**2)**(1/2))), 0, ((0.23)/((0.55**2 + 0.23**2)**(1/2))),
        -0.55, -0.4, 0.47, 0, 1,    -((0.55)/((0.55**2 + 0.23**2)**(1/2))), 0, ((0.23)/((0.55**2 + 0.23**2)**(1/2))),
        -0.55, 0.4, 0.47, 1, 1,     -((0.55)/((0.55**2 + 0.23**2)**(1/2))), 0, ((0.23)/((0.55**2 + 0.23**2)**(1/2)))
    ]
    indices_techo_triangular=[
        0, 1, 2,
        2, 3, 1,
        4, 5, 6,
        6, 7, 5
    ]
    #techo tendra un grosor de
    vertices_techo_triangular_grosor= [
        0.55,-0.4, 0.52, 0, 0,  1, 0, 0,
        0.55, 0.4, 0.52, 1, 0,  1, 0, 0,
        0.55,-0.4, 0.47, 0, 1,  1, 0, 0,
        0.55, 0.4, 0.47, 1, 1,  1, 0, 0

    ]

    indices_techo_triangular_grosor=[
        0, 1, 2,
        2, 3, 1
    ]

    vertices_techo_triangular_frontal= [
        0.55,-0.4, 0.52, 0, 0,  ((0.55)/((0.55**2 + 0.23**2)**(1/2))), 0, ((0.23)/((0.55**2 + 0.23**2)**(1/2))),
        0.55,-0.4, 0.47, 1, 0,  ((0.55)/((0.55**2 + 0.23**2)**(1/2))), 0, ((0.23)/((0.55**2 + 0.23**2)**(1/2))),
        0.0 ,-0.4, 0.85, 0, 1,  ((0.55)/((0.55**2 + 0.23**2)**(1/2))), 0, ((0.23)/((0.55**2 + 0.23**2)**(1/2))),
        0.0 ,-0.4, 0.8, 1, 1,   ((0.55)/((0.55**2 + 0.23**2)**(1/2))), 0, ((0.23)/((0.55**2 + 0.23**2)**(1/2))),

        #lado negativo de x, 
        -0.55,-0.4, 0.52, 0, 0, -((0.55)/((0.55**2 + 0.23**2)**(1/2))), 0, ((0.23)/((0.55**2 + 0.23**2)**(1/2))),
        -0.55,-0.4, 0.47, 1, 0, -((0.55)/((0.55**2 + 0.23**2)**(1/2))), 0, ((0.23)/((0.55**2 + 0.23**2)**(1/2))),
        0.0  ,-0.4, 0.85, 0, 1, -((0.55)/((0.55**2 + 0.23**2)**(1/2))), 0, ((0.23)/((0.55**2 + 0.23**2)**(1/2))),
        0.0  ,-0.4, 0.8, 1, 1,  -((0.55)/((0.55**2 + 0.23**2)**(1/2))), 0, ((0.23)/((0.55**2 + 0.23**2)**(1/2)))
    ]

    indices_techo_triangular_frontal=[
        0, 1, 2,
        2, 3, 1,
        4, 5, 6,
        6, 7, 5
    ]

    vertices_entretecho=[
        -0.5, -0.4, 0.5, 0, 0,  0, -1, 0,
         0.0, -0.4, 0.8, 1, 0,  0, -1, 0,
         0.5, -0.4, 0.5, 0, 1,  0, -1, 0,

         0.5,  0.4, 0.5, 0, 0,  0, 1, 0,
         0.0,  0.4, 0.8, 1, 0,  0, 1, 0,
        -0.5,  0.4, 0.5, 0, 1,  0, 1, 0
    ]

    indices_entretecho=[
        0, 1, 2,
        3, 4, 5
    ]

    #------------------------------------------------------o--------------------------------------
    
    #creando los objetos:
    shape_paredes=Shape(vertices_pared, indices_pared)
    gpu_paredes=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_paredes)
    gpu_paredes.fillBuffers(shape_paredes.vertices,shape_paredes.indices)
    gpu_paredes.texture = textureSimpleSetup(
        getAssetPath(textura_paredes), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    shape_techo=Shape(vertices_techo_o_piso, indices_techo_o_piso)
    gpu_techo=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_techo)
    gpu_techo.fillBuffers(shape_techo.vertices,shape_techo.indices)
    gpu_techo.texture = textureSimpleSetup(
        getAssetPath(textura_paredes), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    shape_piso=Shape(vertices_techo_o_piso, indices_techo_o_piso)
    gpu_piso=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_piso)
    gpu_piso.fillBuffers(shape_piso.vertices,shape_piso.indices)
    gpu_piso.texture = textureSimpleSetup(
        getAssetPath("piso_tatami.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    #Uniendo todo para tener un techo 3D -------------------------o---------------------------

    shape_techo_triangular=Shape(vertices_techo_triangular, indices_techo_triangular)
    gpu_techo_triangular=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_techo_triangular)
    gpu_techo_triangular.fillBuffers(shape_techo_triangular.vertices,shape_techo_triangular.indices)
    gpu_techo_triangular.texture = textureSimpleSetup(
        getAssetPath(textura_techo), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    shape_techo_triangular_grosor=Shape(vertices_techo_triangular_grosor,indices_techo_triangular_grosor)
    gpu_techo_triangular_grosor=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_techo_triangular_grosor)
    gpu_techo_triangular_grosor.fillBuffers(shape_techo_triangular_grosor.vertices,shape_techo_triangular_grosor.indices)
    gpu_techo_triangular_grosor.texture = textureSimpleSetup(
        getAssetPath("techo_japones_antiguo.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    
    shape_techo_triangular_frontal=Shape(vertices_techo_triangular_frontal,indices_techo_triangular_frontal)
    gpu_techo_triangular_frontal=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_techo_triangular_frontal)
    gpu_techo_triangular_frontal.fillBuffers(shape_techo_triangular_frontal.vertices,shape_techo_triangular_frontal.indices)
    gpu_techo_triangular_frontal.texture = textureSimpleSetup(
        getAssetPath("techo_japones_antiguo.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    #-----------------------------------------------------------------------------------------------------
    shape_puerta=creandoParalelepipedo(0.15,0.03,0.5)
    gpu_puerta=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_puerta)
    gpu_puerta.fillBuffers(shape_puerta.vertices,shape_puerta.indices)
    gpu_puerta.texture = textureSimpleSetup(
        getAssetPath("nueva_puerta.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    shape_entretecho=Shape(vertices_entretecho,indices_entretecho)
    gpu_entretecho=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_entretecho)
    gpu_entretecho.fillBuffers(shape_entretecho.vertices,shape_entretecho.indices)
    gpu_entretecho.texture = textureSimpleSetup(
        getAssetPath(textura_paredes), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    shape_division_pisos=creandoParalelepipedo(0.5001,0.4001,0.007)
    gpu_division_pisos=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_division_pisos)
    gpu_division_pisos.fillBuffers(shape_division_pisos.vertices,shape_division_pisos.indices)
    gpu_division_pisos.texture = textureSimpleSetup(
        getAssetPath("division_pisos.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    shape_muralla_casa_10=creandoParalelepipedo(0.4,0.025,0.3)
    gpu_muralla_casa_10=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_muralla_casa_10)
    gpu_muralla_casa_10.fillBuffers(shape_muralla_casa_10.vertices,shape_muralla_casa_10.indices)
    gpu_muralla_casa_10.texture = textureSimpleSetup(
        getAssetPath("muralla_casa_10.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    shape_muralla_casa_11=creandoParalelepipedo(0.05,0.025,0.25)
    gpu_muralla_casa_11=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_muralla_casa_11)
    gpu_muralla_casa_11.fillBuffers(shape_muralla_casa_11.vertices,shape_muralla_casa_11.indices)
    gpu_muralla_casa_11.texture = textureSimpleSetup(
        getAssetPath("muralla_casa_11.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    shape_muralla_casa_12=creandoParalelepipedo(0.115,0.025,0.25)
    gpu_muralla_casa_12=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_muralla_casa_12)
    gpu_muralla_casa_12.fillBuffers(shape_muralla_casa_12.vertices,shape_muralla_casa_12.indices)
    gpu_muralla_casa_12.texture = textureSimpleSetup(
        getAssetPath("muralla_casa_12.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    shape_muralla_casa_13=creandoParalelepipedo(0.115,0.025,0.25)
    gpu_muralla_casa_13=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_muralla_casa_13)
    gpu_muralla_casa_13.fillBuffers(shape_muralla_casa_13.vertices,shape_muralla_casa_13.indices)
    gpu_muralla_casa_13.texture = textureSimpleSetup(
        getAssetPath("muralla_casa_13.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    shape_muralla_casa_14=creandoParalelepipedo(0.5,0.025,0.2)
    gpu_muralla_casa_14=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_muralla_casa_14)
    gpu_muralla_casa_14.fillBuffers(shape_muralla_casa_14.vertices,shape_muralla_casa_14.indices)
    gpu_muralla_casa_14.texture = textureSimpleSetup(
        getAssetPath("muralla_casa_14.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    #Nodo con la escena completa segun lo que pide la funcion
    escena_casa_completa=sg.SceneGraphNode("Casa")
    union=sg.SceneGraphNode("Union de todo")
    

    #Aca es donde se utilizan todos los parametros para crear las casas, poniendolo todo en el nodo "Union de todo"
    cuantos_pisos=nr_pisos
    if cuantos_pisos==1 and tipo_techo=="triangular" and opcion_de_casa==1:

        paredes=sg.SceneGraphNode("Paredes")
        piso=sg.SceneGraphNode("Piso")
        techo_plano=sg.SceneGraphNode("Techo Plano")
        techo_triangular=sg.SceneGraphNode("Techo Triangular")
        techo_triangular2=sg.SceneGraphNode("Techo Triangular 2")
        techo_triangular_grosor=sg.SceneGraphNode("Grosor Techo Triangular")
        techo_triangular_grosor2=sg.SceneGraphNode("Grosor Techo Triangular 2")
        techo_triangular_frontal=sg.SceneGraphNode("Frontal Techo Triangular")
        techo_triangular_frontal2=sg.SceneGraphNode("Frontal Techo Triangular 2")
        ventana=sg.SceneGraphNode("Ventana")
        ventana2=sg.SceneGraphNode("Ventana2")
        puerta=sg.SceneGraphNode("Puerta")
        entretecho=sg.SceneGraphNode("Entretecho")

        paredes.childs += [gpu_paredes]
        piso.transform=tr.matmul([tr.translate(
                0.0, 0.0, -0.4999), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
        piso.childs += [gpu_piso]
        techo_plano.childs +=[gpu_techo]
        techo_triangular.childs += [gpu_techo_triangular]
        techo_triangular2.transform = tr.matmul([tr.translate(
                0.0, 0.0, 0.05), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
        techo_triangular2.childs += [gpu_techo_triangular]
        techo_triangular_grosor.childs += [gpu_techo_triangular_grosor]
        techo_triangular_grosor2.transform = tr.matmul([tr.translate(
                -1.1, 0.0, 0.0), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
        techo_triangular_grosor2.childs += [gpu_techo_triangular_grosor]
        techo_triangular_frontal.childs += [gpu_techo_triangular_frontal]
        techo_triangular_frontal2.transform = tr.matmul([tr.translate(
                0.0, 0.8, 0.0), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
        techo_triangular_frontal2.childs += [gpu_techo_triangular_frontal]
        ventana.transform = tr.matmul([tr.translate(
                0.51, 0.0, 0.25), tr.uniformScale(0.3), tr.translate(0.0, 0.0, 0.0)])
        ventana.childs += [creandoVentana2(pipeline)]
        ventana2.transform=tr.matmul([tr.translate(
                -0.51, 0.0, 0.25), tr.uniformScale(0.3), tr.translate(0.0, 0.0, 0.0)])
        ventana2.childs += [creandoVentana2(pipeline)]
        puerta.transform=tr.matmul([tr.translate(
                0.0, 0.4, 0.0), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])
        puerta.childs += [gpu_puerta]
        entretecho.childs += [gpu_entretecho]       

        if especialidad_casa_nr==5:
            puerta.transform=tr.matmul([tr.translate(
                0.5, 0.0, 0.0), tr.uniformScale(0.5),tr.rotationZ((np.pi)/2) ,tr.translate(0.0, 0.0, 0.0)])
            ventana.transform = tr.matmul([tr.translate(
                0.0, 0.41, 0.25), tr.uniformScale(0.3),tr.rotationZ((np.pi)/2) ,tr.translate(0.0, 0.0, 0.0)])
            ventana2.transform = tr.matmul([tr.translate(
                0.0, -0.41, 0.25), tr.uniformScale(0.3),tr.rotationZ((np.pi)/2) ,tr.translate(0.0, 0.0, 0.0)])
    
        if especialidad_casa_nr==11:
            puerta.transform=tr.matmul([tr.translate(
                0.2, 0.4, 0.0), tr.uniformScale(0.7), tr.translate(0.0, 0.0, 0.0)])
        
        if especialidad_casa_nr==17:
            puerta.childs=[]



        union.childs +=[paredes]
        union.childs +=[piso]
        union.childs +=[techo_plano]
        union.childs +=[techo_triangular]
        union.childs +=[techo_triangular2]
        union.childs +=[techo_triangular_grosor]
        union.childs +=[techo_triangular_grosor2]
        union.childs +=[techo_triangular_frontal]
        union.childs +=[techo_triangular_frontal2]
        union.childs +=[ventana]
        union.childs +=[ventana2]
        union.childs +=[puerta]
        union.childs +=[entretecho]


    elif cuantos_pisos==1 and tipo_techo=="plano" and opcion_de_casa==1:

        paredes=sg.SceneGraphNode("Paredes")
        piso=sg.SceneGraphNode("Piso")
        techo_plano=sg.SceneGraphNode("Techo")
        ventana=sg.SceneGraphNode("Ventana")
        ventana2=sg.SceneGraphNode("Ventana2")
        puerta=sg.SceneGraphNode("Puerta")


        paredes.childs += [gpu_paredes]
        piso.transform=tr.matmul([tr.translate(
                0.0, 0.0, -0.4999), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
        piso.childs += [gpu_piso]
        techo_plano.childs += [gpu_techo]
        ventana.transform = tr.matmul([tr.translate(
                0.51, 0.0, 0.25), tr.uniformScale(0.3), tr.translate(0.0, 0.0, 0.0)])
        ventana.childs += [creandoVentana2(pipeline)]
        ventana2.transform=tr.matmul([tr.translate(
                -0.51, 0.0, 0.25), tr.uniformScale(0.3), tr.translate(0.0, 0.0, 0.0)])
        ventana2.childs += [creandoVentana2(pipeline)]
        puerta.transform=tr.matmul([tr.translate(
                0.0, 0.4, 0.0), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])
        puerta.childs += [gpu_puerta]          

        union.childs +=[paredes]
        union.childs +=[piso]
        union.childs +=[techo_plano]
        union.childs +=[ventana]
        union.childs +=[ventana2]
        union.childs +=[puerta] 
        


    elif cuantos_pisos==2 and opcion_de_casa==1:#Caja de fosforos de dos pisos
        while cuantos_pisos!=0:
            if cuantos_pisos==2:#Los pisos que no son el primero

                if tipo_techo=="triangular":
                    techo_triangular=sg.SceneGraphNode("Techo Triangular")
                    techo_triangular2=sg.SceneGraphNode("Techo Triangular 2")
                    techo_triangular_grosor=sg.SceneGraphNode("Grosor Techo Triangular")
                    techo_triangular_grosor2=sg.SceneGraphNode("Grosor Techo Triangular 2")
                    techo_triangular_frontal=sg.SceneGraphNode("Frontal Techo Triangular")
                    techo_triangular_frontal2=sg.SceneGraphNode("Frontal Techo Triangular 2")
                    entretecho=sg.SceneGraphNode("Entretecho")

                    techo_triangular.transform=tr.matmul([tr.translate(
                        0.0, 0.0, (cuantos_pisos-1)*0.5), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                    techo_triangular.childs += [gpu_techo_triangular]
                    techo_triangular2.transform = tr.matmul([tr.translate(
                        0.0, 0.0, 0.05+(cuantos_pisos-1)*0.5), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                    techo_triangular2.childs += [gpu_techo_triangular]
                    techo_triangular_grosor.transform=tr.matmul([tr.translate(
                        0.0, 0.0, (cuantos_pisos-1)*0.5), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                    techo_triangular_grosor.childs += [gpu_techo_triangular_grosor]
                    techo_triangular_grosor2.transform = tr.matmul([tr.translate(
                        -1.1, 0.0, 0.0+(cuantos_pisos-1)*0.5), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                    techo_triangular_grosor2.childs += [gpu_techo_triangular_grosor]
                    techo_triangular_frontal.transform=tr.matmul([tr.translate(
                        0.0, 0.0, (cuantos_pisos-1)*0.5), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                    techo_triangular_frontal.childs += [gpu_techo_triangular_frontal]
                    techo_triangular_frontal2.transform = tr.matmul([tr.translate(
                        0.0, 0.8, 0.0+(cuantos_pisos-1)*0.5), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                    techo_triangular_frontal2.childs += [gpu_techo_triangular_frontal]
                    entretecho.transform=tr.matmul([tr.translate(
                        0.0, 0.0, (cuantos_pisos-1)*0.5), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                    entretecho.childs += [gpu_entretecho] 

                    if especialidad_casa_nr==9:
                        techo_triangular.transform=tr.matmul([tr.translate(
                        0.0, -0.1, (cuantos_pisos-1)*0.5), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                        techo_triangular2.transform = tr.matmul([tr.translate(
                        0.0, -0.1, 0.05+(cuantos_pisos-1)*0.5), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                        techo_triangular_grosor.transform=tr.matmul([tr.translate(
                        0.0, -0.1, (cuantos_pisos-1)*0.5), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                        techo_triangular_grosor2.transform = tr.matmul([tr.translate(
                        -1.1, -0.1, 0.0+(cuantos_pisos-1)*0.5), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                        techo_triangular_frontal.transform=tr.matmul([tr.translate(
                        0.0, -0.1, (cuantos_pisos-1)*0.5), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                        techo_triangular_frontal2.transform = tr.matmul([tr.translate(
                        0.0, 0.7, 0.0+(cuantos_pisos-1)*0.5), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                        entretecho.transform=tr.matmul([tr.translate(
                        0.0, -0.1, (cuantos_pisos-1)*0.5), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])

                    union.childs +=[techo_triangular]
                    union.childs +=[techo_triangular2]
                    union.childs +=[techo_triangular_grosor]
                    union.childs +=[techo_triangular_grosor2]
                    union.childs +=[techo_triangular_frontal]
                    union.childs +=[techo_triangular_frontal2]
                    union.childs +=[entretecho]

                paredes=sg.SceneGraphNode("Paredes")
                piso=sg.SceneGraphNode("Piso")
                techo_plano=sg.SceneGraphNode("Techo Plano")
                division_pisos=sg.SceneGraphNode("Division Pisos")
                ventana=sg.SceneGraphNode("Ventana")
                ventana2=sg.SceneGraphNode("Ventana2")
                ventana3=sg.SceneGraphNode("Ventana3")
                ventana4=sg.SceneGraphNode("Ventana4")
                puerta=sg.SceneGraphNode("Puerta")

                paredes.transform=tr.matmul([tr.translate(
                        0.0, 0.0, (cuantos_pisos-1)*0.5), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                paredes.childs += [gpu_paredes]
                piso.transform=tr.matmul([tr.translate(
                        0.0, 0.0, -0.4999+(cuantos_pisos-1)*0.5), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                piso.childs += [gpu_piso]
                techo_plano.transform=tr.matmul([tr.translate(
                        0.0, 0.0, (cuantos_pisos-1)*0.5), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                techo_plano.childs +=[gpu_techo]
               
                ventana.transform = tr.matmul([tr.translate(
                        0.51, 0.0, 0.25+(cuantos_pisos-1)*0.5), tr.uniformScale(0.3), tr.translate(0.0, 0.0, 0.0)])
                ventana.childs += [creandoVentana2(pipeline)]
                ventana2.transform=tr.matmul([tr.translate(
                        -0.51, 0.0, 0.25+(cuantos_pisos-1)*0.5), tr.uniformScale(0.3), tr.translate(0.0, 0.0, 0.0)])
                ventana2.childs += [creandoVentana2(pipeline)]
                ventana3.transform=tr.matmul([tr.rotationZ((np.pi)/2),tr.translate(
                        0.41, 0.0, 0.25+(cuantos_pisos-1)*0.5), tr.uniformScale(0.3), tr.translate(0.0, 0.0, 0.0)])
                ventana3.childs += [creandoVentana2(pipeline)]
                ventana4.transform=tr.matmul([tr.rotationZ((np.pi)/2),tr.translate(
                        -0.41, 0.0, 0.25+(cuantos_pisos-1)*0.5), tr.uniformScale(0.3), tr.translate(0.0, 0.0, 0.0)])
                ventana4.childs += [creandoVentana2(pipeline)]
                division_pisos.transform=tr.matmul([tr.translate(
                        0.0, 0.0, 0.49), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                division_pisos.childs += [gpu_division_pisos]

                if especialidad_casa_nr==9:
                    gpu_piso.texture = textureSimpleSetup(
                    getAssetPath(textura_paredes), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
                    piso.childs = []
                    piso.childs =[gpu_piso]
                    paredes.transform=tr.matmul([tr.translate(
                        0.0, -0.1, (cuantos_pisos-1)*0.5), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                    techo_plano.transform=tr.matmul([tr.translate(
                        0.0, -0.1, (cuantos_pisos-1)*0.5), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                    ventana.transform = tr.matmul([tr.translate(
                        0.51, -0.1, 0.25+(cuantos_pisos-1)*0.5), tr.uniformScale(0.3), tr.translate(0.0, 0.0, 0.0)])
                    ventana2.transform=tr.matmul([tr.translate(
                        -0.51, -0.1, 0.25+(cuantos_pisos-1)*0.5), tr.uniformScale(0.3), tr.translate(0.0, 0.0, 0.0)])
                    ventana3.transform=tr.matmul([tr.rotationZ((np.pi)/2),tr.translate(
                        0.31, 0.0, 0.25+(cuantos_pisos-1)*0.5), tr.uniformScale(0.3), tr.translate(0.0, 0.0, 0.0)])
                    ventana4.transform=tr.matmul([tr.rotationZ((np.pi)/2),tr.translate(
                        -0.51, -0.1, 0.25+(cuantos_pisos-1)*0.5), tr.uniformScale(0.3), tr.translate(0.0, 0.0, 0.0)])
                    division_pisos.transform=tr.matmul([tr.translate(
                        0.0, -0.1, 0.49), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                    

                if especialidad_casa_nr==2:
                    gpu_piso.texture = textureSimpleSetup(
                    getAssetPath(textura_paredes), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

                    paredes.transform=tr.matmul([tr.translate(
                        0.0, 0.1, (cuantos_pisos-1)*0.5), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                    piso.transform=tr.matmul([tr.translate(
                        0.0, 0.1, -0.4999+(cuantos_pisos-1)*0.5), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                    piso.childs = []
                    piso.childs =[gpu_piso]
                    techo_plano.transform=tr.matmul([tr.translate(
                        0.0, 0.1, (cuantos_pisos-1)*0.5), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])



                union.childs +=[paredes]
                union.childs +=[piso]
                union.childs +=[techo_plano]
            
                union.childs +=[ventana]
                union.childs +=[ventana2]
                union.childs +=[ventana3]
                union.childs +=[ventana4]
                union.childs +=[puerta]
                union.childs +=[division_pisos]
 

                
            
                cuantos_pisos -=1
            else: #Primer piso
                paredes=sg.SceneGraphNode("Paredes")
                piso=sg.SceneGraphNode("Piso")
                techo_plano=sg.SceneGraphNode("Techo")
                ventana=sg.SceneGraphNode("Ventana")
                ventana2=sg.SceneGraphNode("Ventana2")
                puerta=sg.SceneGraphNode("Puerta")


                paredes.childs += [gpu_paredes]
                piso.transform=tr.matmul([tr.translate(
                        0.0, 0.0, -0.4999), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                piso.childs += [gpu_piso]
                techo_plano.childs += [gpu_techo]
                ventana.transform = tr.matmul([tr.translate(
                        0.51, 0.0, 0.25), tr.uniformScale(0.3), tr.translate(0.0, 0.0, 0.0)])
                ventana.childs += [creandoVentana2(pipeline)]
                ventana2.transform=tr.matmul([tr.translate(
                        -0.51, 0.0, 0.25), tr.uniformScale(0.3), tr.translate(0.0, 0.0, 0.0)])
                ventana2.childs += [creandoVentana2(pipeline)]
                puerta.transform=tr.matmul([tr.translate(
                        0.0, 0.4, 0.0), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])
                puerta.childs += [gpu_puerta]          

                if especialidad_casa_nr==10:
                    muralla_frontal=sg.SceneGraphNode("Muralla Frontal")
                    muralla_lateral=sg.SceneGraphNode("Muralla Lateral")

                    muralla_frontal.transform=tr.matmul([tr.translate(
                        0.1, 0.8, 0.0), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                    muralla_frontal.childs=[gpu_muralla_casa_10]
                    muralla_lateral.transform=tr.matmul([tr.translate(
                        -0.6, 0.415, 0.0), tr.uniformScale(1.0),tr.rotationZ((np.pi)/2), tr.translate(0.0, 0.0, 0.0)])
                    muralla_lateral.childs=[gpu_muralla_casa_10]

                    union.childs +=[muralla_frontal]
                    union.childs +=[muralla_lateral]

                if especialidad_casa_nr==11:
                    muralla_frontal=sg.SceneGraphNode("Muralla Frontal")
                    muralla_lateral=sg.SceneGraphNode("Muralla Lateral")
                    puerta.childs=[]

                    muralla_frontal.transform=tr.matmul([tr.translate(
                        0.5, 0.4, 0.0), tr.uniformScale(0.7), tr.translate(0.0, 0.0, 0.0)])
                    muralla_frontal.childs=[gpu_muralla_casa_11]
                    muralla_lateral.transform=tr.matmul([tr.translate(
                        0.7, 0.4, 0.0), tr.uniformScale(0.7), tr.translate(0.0, 0.0, 0.0)])
                    muralla_lateral.childs=[gpu_muralla_casa_11]

                    union.childs +=[muralla_frontal]
                    union.childs +=[muralla_lateral]

                if especialidad_casa_nr==12:
                    muralla_frontal=sg.SceneGraphNode("Muralla Frontal")
                    muralla_lateral=sg.SceneGraphNode("Muralla Lateral")
                    muralla_frontal_detras=sg.SceneGraphNode("Muralla Frontal Detras")
                    puerta.transform=tr.matmul([tr.translate(
                        -0.25, 0.4, 0.0), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])

                    muralla_frontal.transform=tr.matmul([tr.translate(
                        -0.05, 0.65, 0.0), tr.uniformScale(0.7), tr.translate(0.0, 0.0, 0.0)])
                    muralla_frontal.childs=[gpu_muralla_casa_12]
                    
                    muralla_lateral.childs=[gpu_muralla_casa_12]
                    muralla_frontal_detras.transform=tr.matmul([tr.translate(
                        -0.02, 0.54, 0.0), tr.uniformScale(0.7),tr.rotationZ((np.pi)/2), tr.translate(0.0, 0.0, 0.0)])
                    muralla_frontal_detras.childs=[gpu_muralla_casa_12]

                    union.childs +=[muralla_frontal]
                    union.childs +=[muralla_lateral]
                    union.childs +=[muralla_frontal_detras]
                
                if especialidad_casa_nr==13:
                    techito=sg.SceneGraphNode("Techo sobre puerta")
                    muralla_frontal=sg.SceneGraphNode("Muralla Frontal")
                    puerta.transform=tr.matmul([tr.translate(
                        -0.25, 0.4, 0.0), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])
                    
                    techito.transform=tr.matmul([tr.translate(
                        -0.25, 0.4, 0.0), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])
                    techito.childs += [creando_techo_triangular_chico(pipeline,"textura_metal.jpg")]

                    muralla_frontal.transform=tr.matmul([tr.translate(
                        -0.35, 0.65, 0.0), tr.uniformScale(0.7), tr.translate(0.0, 0.0, 0.0)])
                    muralla_frontal.childs += [gpu_muralla_casa_13]

                    union.childs +=[muralla_frontal]
                    union.childs +=[techito]
                
                if especialidad_casa_nr==14:
                    muralla_frontal=sg.SceneGraphNode("Muralla Frontal")
                    muralla_lateral=sg.SceneGraphNode("Muralla Lateral")
                    puerta.transform=tr.matmul([tr.rotationZ((np.pi)/2),tr.translate(
                        0.3, -0.50, 0.0), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])

                    muralla_frontal.transform=tr.matmul([tr.translate(
                        0.8, 0.15, 0.0), tr.uniformScale(1.0),tr.rotationZ((np.pi)/2), tr.translate(0.0, 0.0, 0.0)])
                    muralla_frontal.childs +=[gpu_muralla_casa_14]
                    muralla_lateral.transform=tr.matmul([tr.translate(
                        0.3, 0.65, 0.0), tr.uniformScale(1.0) , tr.translate(0.0, 0.0, 0.0)])
                    muralla_lateral.childs +=[gpu_muralla_casa_14]

                    union.childs +=[muralla_frontal]
                    union.childs +=[muralla_lateral]
                
                if especialidad_casa_nr==15:
                    shape_techo_madera=creandoParalelepipedo(0.5,0.4,0.01)
                    gpu_techo_madera=GPUShape().initBuffers()
                    pipeline.setupVAO(gpu_techo_madera)
                    gpu_techo_madera.fillBuffers(shape_techo_madera.vertices,shape_techo_madera.indices)
                    gpu_techo_madera.texture = textureSimpleSetup(
                        getAssetPath("pared_madera.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

                    Balcon=sg.SceneGraphNode("Balcon")
                    Techo_madera=sg.SceneGraphNode("Techo Madera")

                    Balcon.transform=tr.matmul([tr.translate(
                        -0.3, 0.45, 0.0), tr.uniformScale(1.0) ,tr.translate(0.0, 0.0, 0.0)])
                    Balcon.childs +=[creando_Balcon(pipeline,"pared_madera.jpg")]
                    Techo_madera.transform=tr.matmul([tr.translate(
                        0.0, 0.0, 1.0), tr.uniformScale(1.0) ,tr.translate(0.0, 0.0, 0.0)])
                    Techo_madera.childs += [gpu_techo_madera]

                    union.childs +=[Balcon]
                    union.childs +=[Techo_madera]

                if especialidad_casa_nr==18:
                    Balcon=sg.SceneGraphNode("Balcon")
                    

                    Balcon.transform=tr.matmul([tr.translate(
                    -0.3, 0.45, 0.0), tr.uniformScale(1.2) ,tr.translate(0.0, 0.0, 0.0)])
                    Balcon.childs +=[creando_Balcon(pipeline,"pared_madera.jpg")]
                    

                    union.childs +=[Balcon]
                
                if especialidad_casa_nr==19:
                    Balcon=sg.SceneGraphNode("Balcon")
                    

                    Balcon.transform=tr.matmul([tr.translate(
                    -0.3, 0.45, 0.0), tr.uniformScale(1.0) ,tr.translate(0.0, 0.0, 0.0)])
                    Balcon.childs +=[creando_Balcon(pipeline,"division_pisos.jpg")]
                    

                    union.childs +=[Balcon]
                    



                union.childs +=[paredes]
                union.childs +=[piso]
                union.childs +=[techo_plano]
                union.childs +=[ventana]
                union.childs +=[ventana2]
                union.childs +=[puerta] 
                cuantos_pisos -=1

    elif cuantos_pisos==2 and opcion_de_casa==2:#Opcion de casa en L
        while cuantos_pisos!=0:
            if cuantos_pisos==2:
                if tipo_techo=="triangular":
                    techo_triangular=sg.SceneGraphNode("Techo Triangular")
                    techo_triangular2=sg.SceneGraphNode("Techo Triangular 2")
                    techo_triangular_grosor=sg.SceneGraphNode("Grosor Techo Triangular")
                    techo_triangular_grosor2=sg.SceneGraphNode("Grosor Techo Triangular 2")
                    techo_triangular_frontal=sg.SceneGraphNode("Frontal Techo Triangular")
                    techo_triangular_frontal2=sg.SceneGraphNode("Frontal Techo Triangular 2")
                    entretecho=sg.SceneGraphNode("Entretecho")

                    segundo_techo=sg.SceneGraphNode("Segundo techo")

                    techo_triangular.transform=tr.matmul([tr.translate(
                        0.4, -0.6, (cuantos_pisos-1)*0.5), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                    techo_triangular.childs += [gpu_techo_triangular]
                    techo_triangular2.transform = tr.matmul([tr.translate(
                        0.4, -0.6, 0.05+(cuantos_pisos-1)*0.5), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                    techo_triangular2.childs += [gpu_techo_triangular]
                    techo_triangular_grosor.transform=tr.matmul([tr.translate(
                        0.4, -0.6, (cuantos_pisos-1)*0.5), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                    techo_triangular_grosor.childs += [gpu_techo_triangular_grosor]
                    techo_triangular_grosor2.transform = tr.matmul([tr.translate(
                        -0.7, -0.6, 0.0+(cuantos_pisos-1)*0.5), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                    techo_triangular_grosor2.childs += [gpu_techo_triangular_grosor]
                    techo_triangular_frontal.transform=tr.matmul([tr.translate(
                        0.4, -0.6, (cuantos_pisos-1)*0.5), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                    techo_triangular_frontal.childs += [gpu_techo_triangular_frontal]
                    techo_triangular_frontal2.transform = tr.matmul([tr.translate(
                        0.4, 0.2, 0.0+(cuantos_pisos-1)*0.5), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                    techo_triangular_frontal2.childs += [gpu_techo_triangular_frontal]
                    entretecho.transform=tr.matmul([tr.translate(
                        0.4, -0.6, (cuantos_pisos-1)*0.5), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                    entretecho.childs += [gpu_entretecho] 

                    union.childs +=[techo_triangular]
                    union.childs +=[techo_triangular2]
                    union.childs +=[techo_triangular_grosor]
                    union.childs +=[techo_triangular_grosor2]
                    union.childs +=[techo_triangular_frontal]
                    union.childs +=[techo_triangular_frontal2]
                    union.childs +=[entretecho]

                    segundo_techo.childs +=[techo_triangular]
                    segundo_techo.childs +=[techo_triangular2]
                    segundo_techo.childs +=[techo_triangular_grosor]
                    segundo_techo.childs +=[techo_triangular_grosor2]
                    segundo_techo.childs +=[techo_triangular_frontal]
                    segundo_techo.childs +=[techo_triangular_frontal2]
                    segundo_techo.childs +=[entretecho]

                    segundo_techo.transform=tr.matmul([tr.rotationZ((np.pi)/2),tr.translate(
                        0.0, 1.4, 0.0), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                    union.childs += [segundo_techo]

                paredes=sg.SceneGraphNode("Paredes")
                paredes2=sg.SceneGraphNode("Paredes 2")

                piso=sg.SceneGraphNode("Piso")
                piso2=sg.SceneGraphNode("Piso 2")
                techo_plano=sg.SceneGraphNode("Techo Plano")
                techo_plano2=sg.SceneGraphNode("Techo Plano 2")

                ventana=sg.SceneGraphNode("Ventana")
                ventana2=sg.SceneGraphNode("Ventana2")
                ventana3=sg.SceneGraphNode("Ventana3")
                ventana4=sg.SceneGraphNode("Ventana4")
                ventana5=sg.SceneGraphNode("Ventana5")
                ventana6=sg.SceneGraphNode("Ventana6")

                
                paredes.transform=tr.matmul([tr.translate(
                            0.4, -0.5, (cuantos_pisos-1)*0.5), tr.uniformScale(1.0),tr.rotationZ((np.pi)/2),tr.translate(0.0, 0.0, 0.0)])
                paredes.childs += [gpu_paredes]
                paredes2.transform=tr.matmul([tr.translate(
                            -0.7, 0.4, (cuantos_pisos-1)*0.5), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                paredes2.childs += [gpu_paredes]

                piso.transform=tr.matmul([tr.translate(
                            0.4, -0.5, -0.4999+(cuantos_pisos-1)*0.5), tr.uniformScale(1.0),tr.rotationZ((np.pi)/2),tr.translate(0.0, 0.0, 0.0)])
                piso.childs += [gpu_piso]
                piso2.transform=tr.matmul([tr.translate(
                            -0.5, 0.4, 0.0), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                piso2.childs += [gpu_piso]
                techo_plano.transform=tr.matmul([tr.translate(
                            0.4, -0.5, (cuantos_pisos-1)*0.5), tr.uniformScale(1.0),tr.rotationZ((np.pi)/2),tr.translate(0.0, 0.0, 0.0)])
                techo_plano.childs += [gpu_techo]
                techo_plano2.transform=tr.matmul([tr.translate(
                            -0.7, 0.4, (cuantos_pisos-1)*0.5), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
                techo_plano2.childs += [gpu_techo]

                ventana.transform=tr.matmul([tr.translate(
                            0.8099, -0.5, 0.25+ (cuantos_pisos-1)*0.5), tr.uniformScale(0.4),tr.translate(0.0, 0.0, 0.0)])
                ventana.childs += [creandoVentana2(pipeline)]
                ventana2.transform=tr.matmul([tr.translate(
                            -0.0099, -0.5, 0.25+ (cuantos_pisos-1)*0.5), tr.uniformScale(0.4),tr.translate(0.0, 0.0, 0.0)])
                ventana2.childs += [creandoVentana2(pipeline)]
                ventana3.transform=tr.matmul([tr.translate(
                            -0.7, 0.8099, 0.25+ (cuantos_pisos-1)*0.5), tr.uniformScale(0.4),tr.rotationZ((np.pi)/2),tr.translate(0.0, 0.0, 0.0)])
                ventana3.childs +=[creandoVentana2(pipeline)]
                ventana4.transform=tr.matmul([tr.translate(
                            -0.7, -0.0099, 0.25+ (cuantos_pisos-1)*0.5), tr.uniformScale(0.4),tr.rotationZ((np.pi)/2),tr.translate(0.0, 0.0, 0.0)])
                ventana4.childs +=[creandoVentana2(pipeline)]
                ventana5.transform=tr.matmul([tr.translate(
                            -1.225, 0.4, 0.25+ (cuantos_pisos-1)*0.5), tr.uniformScale(0.4),tr.translate(0.0, 0.0, 0.0)])
                ventana5.childs += [creandoVentana2(pipeline)]
                ventana6.transform=tr.matmul([tr.rotationZ((np.pi)/2),tr.translate(
                        -1.01, -0.4, 0.25+(cuantos_pisos-1)*0.5), tr.uniformScale(0.4), tr.translate(0.0, 0.0, 0.0)])
                ventana6.childs += [creandoVentana2(pipeline)]

                union.childs +=[paredes]
                union.childs +=[paredes2]
                union.childs +=[piso]
                union.childs +=[piso2]
                union.childs +=[techo_plano]
                union.childs +=[techo_plano2]
                union.childs +=[ventana]
                union.childs +=[ventana2]
                union.childs +=[ventana3]
                union.childs +=[ventana4]
                union.childs +=[ventana5]
                union.childs +=[ventana6]

                cuantos_pisos -=1
            
            else:
                shape_relleno=creandoParalelepipedo(0.5,0.4,0.99999)
                gpu_relleno=GPUShape().initBuffers()
                pipeline.setupVAO(gpu_relleno)
                gpu_relleno.fillBuffers(shape_relleno.vertices,shape_relleno.indices)
                gpu_relleno.texture = textureSimpleSetup(
                getAssetPath(textura_paredes), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

                if especialidad_casa_nr==17:
                    a=a

                paredes=sg.SceneGraphNode("Paredes")
                paredes2=sg.SceneGraphNode("Paredes 2")
                pared_para_rellenar_casa_en_L=sg.SceneGraphNode("Relleno paredes")
                division_pisos=sg.SceneGraphNode("Division Pisos")
                division_pisos2=sg.SceneGraphNode("Division Pisos 2")
                division_pisos3=sg.SceneGraphNode("Division Pisos 3")


                piso=sg.SceneGraphNode("Piso")
                piso2=sg.SceneGraphNode("Piso 2")
                techo_plano=sg.SceneGraphNode("Techo Plano")

                ventana=sg.SceneGraphNode("Ventana")
                ventana2=sg.SceneGraphNode("Ventana2")
                ventana3=sg.SceneGraphNode("Ventana3")
                ventana4=sg.SceneGraphNode("Ventana4")

                puerta=sg.SceneGraphNode("Puerta")

                
                paredes.transform=tr.matmul([tr.translate(
                            0.4, -0.5, (cuantos_pisos-1)*0.5), tr.uniformScale(1.0),tr.rotationZ((np.pi)/2),tr.translate(0.0, 0.0, 0.0)])
                paredes.childs += [gpu_paredes]
                paredes2.transform=tr.matmul([tr.translate(
                            -0.7, 0.4, (cuantos_pisos-1)*0.5), tr.uniformScale(1.0),tr.translate(0.0, 0.0, 0.0)])
                paredes2.childs += [gpu_paredes]

                piso.transform=tr.matmul([tr.translate(
                            0.4, -0.5, -0.4999+(cuantos_pisos-1)*0.5), tr.uniformScale(1.0),tr.rotationZ((np.pi)/2),tr.translate(0.0, 0.0, 0.0)])
                piso.childs += [gpu_piso]
                piso2.transform=tr.matmul([tr.translate(
                            -0.7, 0.4, -0.4999+(cuantos_pisos-1)*0.5), tr.uniformScale(1.0),tr.translate(0.0, 0.0, 0.0)])
                piso2.childs += [gpu_piso]
                techo_plano.transform=tr.matmul([tr.translate(
                            0.4, -0.5, (cuantos_pisos-1)*0.5), tr.uniformScale(1.0),tr.rotationZ((np.pi)/2),tr.translate(0.0, 0.0, 0.0)])
                techo_plano.childs +=[gpu_techo]
                pared_para_rellenar_casa_en_L.transform=tr.matmul([tr.translate(
                            0.3, 0.4, 0.0), tr.uniformScale(1.0),tr.translate(0.0, 0.0, 0.0)])
                pared_para_rellenar_casa_en_L.childs += [gpu_relleno]
                division_pisos.transform=tr.matmul([tr.translate(
                        0.4, -0.5, 0.49), tr.uniformScale(1.0),tr.rotationZ((np.pi)/2) ,tr.translate(0.0, 0.0, 0.0)])
                division_pisos.childs += [gpu_division_pisos]
                division_pisos2.transform=tr.matmul([tr.translate(
                        -0.7, 0.4, 0.49), tr.uniformScale(1.0) ,tr.translate(0.0, 0.0, 0.0)])
                division_pisos2.childs += [gpu_division_pisos]
                division_pisos3.transform=tr.matmul([tr.translate(
                        0.3, 0.4, 0.49), tr.uniformScale(1.0) ,tr.translate(0.0, 0.0, 0.0)])
                division_pisos3.childs += [gpu_division_pisos]

                puerta.transform=tr.matmul([tr.translate(
                        0.4 ,-0.999, 0.0), tr.uniformScale(0.5), tr.translate(0.0, 0.0, 0.0)])
                puerta.childs +=[gpu_puerta]

                ventana.transform=tr.matmul([tr.translate(
                            0.8099, -0.5, 0.25+ (cuantos_pisos-1)*0.5), tr.uniformScale(0.4),tr.translate(0.0, 0.0, 0.0)])
                ventana.childs += [creandoVentana2(pipeline)]
                ventana2.transform=tr.matmul([tr.translate(
                            -0.0099, -0.5, 0.25+ (cuantos_pisos-1)*0.5), tr.uniformScale(0.4),tr.translate(0.0, 0.0, 0.0)])
                ventana2.childs += [creandoVentana2(pipeline)]
                ventana3.transform=tr.matmul([tr.translate(
                            -0.7, 0.8099, 0.25+ (cuantos_pisos-1)*0.5), tr.uniformScale(0.4),tr.rotationZ((np.pi)/2),tr.translate(0.0, 0.0, 0.0)])
                ventana3.childs +=[creandoVentana2(pipeline)]
                ventana4.transform=tr.matmul([tr.translate(
                            -0.7, -0.0099, 0.25+ (cuantos_pisos-1)*0.5), tr.uniformScale(0.4),tr.rotationZ((np.pi)/2),tr.translate(0.0, 0.0, 0.0)])
                ventana4.childs +=[creandoVentana2(pipeline)]

                



                union.childs +=[paredes]
                union.childs +=[paredes2]
                union.childs +=[piso]
                union.childs +=[piso2]
                union.childs +=[techo_plano]
                union.childs +=[pared_para_rellenar_casa_en_L]
                union.childs +=[puerta]
                union.childs +=[ventana]
                union.childs +=[ventana2]
                union.childs +=[ventana3]
                union.childs +=[ventana4]
                union.childs +=[division_pisos]
                union.childs +=[division_pisos2]
                union.childs +=[division_pisos3]

                cuantos_pisos -=1


    escena_casa_completa.childs += [union]



    return escena_casa_completa




 
#Crea un arbol con raices en sus esquinas, un tronco, y esferas como "ramas"
def creandoArbol(pipeline,textura_arbol):
    
    vertices_base_laterales = [
        #   positions         texture coordinates

        # Cara pegada al piso del arbol
         0.1,  -0.1, 0.0,  0, 0,    0, 0, -1,
        -0.1,  -0.1, 0.0,  0, 1,    0, 0, -1,
         0.1,   0.1, 0.0,  1, 0,    0, 0, -1,
        -0.1,   0.1, 0.0,  1, 1,    0, 0, -1,

        # X-: pared perpendicular al eje x negativo
         0.1,  -0.1, 0.5,  0, 1,    0, 0, 1,
        -0.1,  -0.1, 0.5,  0, 0,    0, 0, 1,
         0.1,   0.1, 0.5,  1, 1,    0, 0, 1,
        -0.1,   0.1, 0.5,  1, 0,    0, 0, 1

    ]

    indices_base_laterales = [
        0, 1, 2, 2, 3, 1, 
        4, 5, 6, 6, 7, 5,  
        0, 2, 4, 4, 6, 2,  
        5, 7, 3, 5, 1, 3] 

    
    vertices_laterales_faltante = [
        #   positions         texture coordinates

        
         -0.1,  -0.1, 0.0,  0, 0,   0, -1, 0,
          0.1,  -0.1, 0.0,  0, 1,   0, -1, 0,
         -0.1,  -0.1, 0.5,  1, 0,   0, -1, 0,
          0.1,  -0.1, 0.5,  1, 1,   0, -1, 0,

        
         -0.1,  0.1, 0.0,  0, 0,    0, 1, 0,
          0.1,  0.1, 0.0,  0, 1,    0, 1, 0,
         -0.1,  0.1, 0.5,  1, 0,    0, 1, 0,
          0.1,  0.1, 0.5,  1, 1,    0, 1, 0

    ]

    indices_laterales_faltante = [
        0, 1, 2, 2, 3, 1, 
        4, 5, 6, 6, 7, 5  
    ]  

    vertices_raices=[
        0.1, -0.1, 0.1, 0, 0,   -1, 0, 0,
        0.1, -0.1, 0.0, 0, 1,   -1, 0, 0,
        0.15, -0.15, 0.0, 1, 1, -1, 0, 0,

        0.1, -0.1, 0.1, 0, 0,   -1, 0, 0,
        0.075,-0.1, 0.0, 0, 1,  -1, 0, 0,     
        0.15, -0.15, 0.0, 1, 1, -1, 0, 0,

        0.1, -0.1, 0.1, 0, 0,   -1, 0, 0,
        0.1,-0.075, 0.0, 0, 1,  -1, 0, 0,     
        0.15, -0.15, 0.0, 1, 1, -1, 0, 0
    ]
    indices_raices=[
        0, 1, 2,
        3, 4, 5,
        6, 7, 8
    ]


    shapeArbol=Shape(vertices_base_laterales, indices_base_laterales)
    gpu_Arbol=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_Arbol)
    gpu_Arbol.fillBuffers(shapeArbol.vertices, shapeArbol.indices)
    gpu_Arbol.texture=textureSimpleSetup(
    getAssetPath("corteza_pino.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    shapeArbol_restante=Shape(vertices_laterales_faltante, indices_laterales_faltante)
    gpu_Arbol_restante=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_Arbol_restante)
    gpu_Arbol_restante.fillBuffers(shapeArbol_restante.vertices, shapeArbol_restante.indices)
    gpu_Arbol_restante.texture=textureSimpleSetup(
    getAssetPath("corteza_pino.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    shape_raices=Shape(vertices_raices, indices_raices)
    gpu_raices=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_raices)
    gpu_raices.fillBuffers(shape_raices.vertices, shape_raices.indices)
    gpu_raices.texture=textureSimpleSetup(
    getAssetPath("corteza_pino.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    shapeEsfera=createSphere(0.15,20,0,0,0,0.0,0.0,0.5)
    gpu_Esfera=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_Esfera)
    gpu_Esfera.fillBuffers(shapeEsfera.vertices, shapeEsfera.indices)
    gpu_Esfera.texture=textureSimpleSetup(
    getAssetPath(textura_arbol), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    
    # Definimos el nodo escena
    scene = sg.SceneGraphNode('system')

    Arbolito = sg.SceneGraphNode('Arbolito1')


    
    Arbol_1 = sg.SceneGraphNode('Arbol_1')
    Arbol_2 = sg.SceneGraphNode('Arbol_2')
    Raiz= sg.SceneGraphNode("Raiz")
    Raiz2= sg.SceneGraphNode("Raiz2")
    Raiz3= sg.SceneGraphNode("Raiz3")
    Raiz4= sg.SceneGraphNode("Raiz4")
    Rama=sg.SceneGraphNode("Rama")
    Rama2=sg.SceneGraphNode("Rama2")
    Rama3=sg.SceneGraphNode("Rama3")
    Rama4=sg.SceneGraphNode("Rama4")
    Rama5=sg.SceneGraphNode("Rama5")
    Rama6=sg.SceneGraphNode("Rama6")


    Arbol_1.transform = tr.matmul([tr.translate(
                    0.0,0.0,0.0), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])

    Arbol_2.transform = tr.matmul([tr.translate(
                    0.0,0.0,0.0), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
    
    Raiz.transform = tr.matmul([tr.translate(
                    0.0,0.0,0.0), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
    
    Raiz2.transform = tr.matmul([tr.translate(
                    0.0,0.0,0.0), tr.uniformScale(1.0),tr.rotationZ((np.pi)/2) , tr.translate(0.0, 0.0, 0.0)])
    
    Raiz3.transform = tr.matmul([tr.translate(
                    0.0,0.0,0.0), tr.uniformScale(1.0),tr.rotationZ((np.pi)) , tr.translate(0.0, 0.0, 0.0)])

    Raiz4.transform = tr.matmul([tr.translate(
                    0.0,0.0,0.0), tr.uniformScale(1.0),tr.rotationZ(3*(np.pi)/2) , tr.translate(0.0, 0.0, 0.0)])

    Rama.transform = tr.matmul([tr.translate(
                    0.0,0.0,0.0), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
    Rama2.transform = tr.matmul([tr.translate(
                    0.0,0.15,0.0), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
    Rama3.transform = tr.matmul([tr.translate(
                    0.0,-0.15,0.0), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
    Rama4.transform = tr.matmul([tr.translate(
                    0.15,0.0,0.0), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
    Rama5.transform = tr.matmul([tr.translate(
                    -0.15,0.0,0.0), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
    Rama6.transform = tr.matmul([tr.translate(
                    0.0,0.0,0.225), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])

    Arbol_1.childs += [gpu_Arbol]
    Arbol_2.childs += [gpu_Arbol_restante]
    Raiz.childs += [gpu_raices]
    Raiz2.childs += [gpu_raices]
    Raiz3.childs += [gpu_raices]
    Raiz4.childs += [gpu_raices]
    Rama.childs += [gpu_Esfera]
    Rama2.childs += [gpu_Esfera]
    Rama3.childs += [gpu_Esfera]
    Rama4.childs += [gpu_Esfera]
    Rama5.childs += [gpu_Esfera]
    Rama6.childs += [gpu_Esfera]

    Arbolito.childs += [Arbol_1]
    Arbolito.childs += [Arbol_2]
    Arbolito.childs += [Raiz]
    Arbolito.childs += [Raiz2]
    Arbolito.childs += [Raiz3]
    Arbolito.childs += [Raiz4]
    Arbolito.childs += [Rama]
    Arbolito.childs += [Rama2]
    Arbolito.childs += [Rama3]
    Arbolito.childs += [Rama4]
    Arbolito.childs += [Rama5]
    Arbolito.childs += [Rama6]

    scene.childs += [Arbolito]





    

    return scene


def creandoFarol(pipeline):

    #poste sera el palo vertical del farol, que tendra altura 1.2(esta se toma desde z=0 hasata z=1.2), casi mas grande que las casas
    shape_poste=creandoParalelepipedo(0.01,0.01,1.2)
    gpu_poste=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_poste)
    gpu_poste.fillBuffers(shape_poste.vertices,shape_poste.indices)
    gpu_poste.texture=textureSimpleSetup(
    getAssetPath("metal_farol.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    shape_palo_horizontal=creandoParalelepipedo(0.01,0.15,0.01)
    gpu_palo_horizontal=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_palo_horizontal)
    gpu_palo_horizontal.fillBuffers(shape_palo_horizontal.vertices,shape_palo_horizontal.indices)
    gpu_palo_horizontal.texture=textureSimpleSetup(
    getAssetPath("metal_farol.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    #Cajita donde estara la luz que alumbrara el farol

    shape_tapa_cajita_luz=creandoParalelepipedo(0.025,0.05,0.01)
    gpu_tapa_cajita_luz=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_tapa_cajita_luz)
    gpu_tapa_cajita_luz.fillBuffers(shape_tapa_cajita_luz.vertices,shape_tapa_cajita_luz.indices)
    gpu_tapa_cajita_luz.texture=textureSimpleSetup(
    getAssetPath("metal_farol.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    shape_tapa_x=creandoParalelepipedo(0.001,0.05,0.02)
    gpu_tapa_x=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_tapa_x)
    gpu_tapa_x.fillBuffers(shape_tapa_x.vertices,shape_tapa_x.indices)
    gpu_tapa_x.texture=textureSimpleSetup(
    getAssetPath("metal_farol.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    shape_tapa_y=creandoParalelepipedo(0.025,0.001,0.02)
    gpu_tapa_y=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_tapa_y)
    gpu_tapa_y.fillBuffers(shape_tapa_y.vertices,shape_tapa_y.indices)
    gpu_tapa_y.texture=textureSimpleSetup(
    getAssetPath("metal_farol.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    shape_foco=creandoParalelepipedo(0.0249,0.049,0.0005)
    gpu_foco=GPUShape().initBuffers()
    pipeline.setupVAO(gpu_foco)
    gpu_foco.fillBuffers(shape_foco.vertices,shape_foco.indices)
    gpu_foco.texture=textureSimpleSetup(
    getAssetPath("blanco.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    

    #-----------------------------------------------o-------------------------------------------------
    #Aca se van a crear los nodos donde estara las diferentes componentes de un farol


    escena_farol=sg.SceneGraphNode("Casa")
    union=sg.SceneGraphNode("Union de todo")

    cajita_luz = sg.SceneGraphNode('Caja luz')
    union_caja=sg.SceneGraphNode('Union caja')

    tapa_caja=sg.SceneGraphNode('Tapa caja')
    tapa_caja.transform = tr.matmul([tr.translate(
                    0.0,0.0,0.0), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
    tapa_caja.childs += [gpu_tapa_cajita_luz]

    tapa_x=sg.SceneGraphNode('Tapa X')
    tapa_x.transform = tr.matmul([tr.translate(
                    -0.024, 0.0, -0.02), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
    tapa_x.childs += [gpu_tapa_x]
    tapa_x2=sg.SceneGraphNode('Tapa X')
    tapa_x2.transform = tr.matmul([tr.translate(
                    0.024, 0.0, -0.02), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
    tapa_x2.childs += [gpu_tapa_x]

    tapa_y=sg.SceneGraphNode('Tapa Y')
    tapa_y.transform = tr.matmul([tr.translate(
                    0.0,-0.049, -0.02), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
    tapa_y.childs += [gpu_tapa_y]
    tapa_y2=sg.SceneGraphNode('Tapa Y')
    tapa_y2.transform = tr.matmul([tr.translate(
                    0.0,0.049, -0.02), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
    tapa_y2.childs += [gpu_tapa_y]
    foco=sg.SceneGraphNode("Foco")
    foco.transform = tr.matmul([tr.translate(
                    0.0,0.0, -0.01), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
    foco.childs += [gpu_foco]


    union_caja.transform= tr.matmul([tr.translate(
                    0.0,0.32, 1.18), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
    union_caja.childs += [tapa_caja]
    union_caja.childs += [tapa_x]
    union_caja.childs += [tapa_x2]
    union_caja.childs += [tapa_y]
    union_caja.childs += [tapa_y2]
    union_caja.childs += [foco]

    cajita_luz.childs+=[union_caja]
    
    
    poste= sg.SceneGraphNode('Poste')
    poste.transform = tr.matmul([tr.translate(
                    0.0,0.0, 0.0), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
    poste.childs += [gpu_poste]

    palo_horizontal = sg.SceneGraphNode('Palo Horizontal')
    palo_horizontal.transform= tr.matmul([tr.translate(
                    0.0,0.16, 1.19), tr.uniformScale(1.0), tr.translate(0.0, 0.0, 0.0)])
    palo_horizontal.childs += [gpu_palo_horizontal]
    
    
    union.childs += [poste]
    union.childs += [cajita_luz]
    union.childs += [palo_horizontal]

    escena_farol.childs += [union]

    return escena_farol


#Es parte necesaria para obtener el modelo completo de un archivo obj
def readFaceVertex(faceDescription):

    aux = faceDescription.split('/')

    assert len(aux[0]), "Vertex index has not been defined."

    faceVertex = [int(aux[0]), None, None]

    assert len(aux) == 3, "Only faces where its vertices require 3 indices are defined."

    if len(aux[1]) != 0:
        faceVertex[1] = int(aux[1])

    if len(aux[2]) != 0:
        faceVertex[2] = int(aux[2])

    return faceVertex

#Lee archivos obj. que es de donde se sacara el auto
def readOBJ(filename, color):

    vertices = []
    normals = []
    textCoords= []
    faces = []

    with open(filename, 'r') as file:
        for line in file.readlines():
            aux = line.strip().split(' ')
            
            if aux[0] == 'v':
                vertices += [[float(coord) for coord in aux[1:]]]

            elif aux[0] == 'vn':
                normals += [[float(coord) for coord in aux[1:]]]

            elif aux[0] == 'vt':
                assert len(aux[1:]) == 2, "Texture coordinates with different than 2 dimensions are not supported"
                textCoords += [[float(coord) for coord in aux[1:]]]

            elif aux[0] == 'f':
                N = len(aux)                
                faces += [[readFaceVertex(faceVertex) for faceVertex in aux[1:4]]]
                for i in range(3, N-1):
                    faces += [[readFaceVertex(faceVertex) for faceVertex in [aux[i], aux[i+1], aux[1]]]]

        vertexData = []
        indices = []
        index = 0

        # Per previous construction, each face is a triangle
        for face in faces:

            # Checking each of the triangle vertices
            for i in range(0,3):
                vertex = vertices[face[i][0]-1]
                normal = normals[face[i][2]-1]

                vertexData += [
                    vertex[0], vertex[1], vertex[2],
                    color[0], color[1], color[2],
                    normal[0], normal[1], normal[2]
                ]

            # Connecting the 3 vertices to create a triangle
            indices += [index, index + 1, index + 2]
            index += 3        

        return Shape(vertexData, indices)














