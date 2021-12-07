import sys
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

from pywavefront import visualization
import pywavefront

meshes_map = pywavefront.Wavefront('FullTrack.obj')
meshes_car= pywavefront.Wavefront('Chevrolet_Camaro_SS_Low.obj')
path = []

theda = 0
angle = 0

lightAmbient = [ 0.5,0.5,0.5,1.0 ]
lightDiffuse = [ 0.9,0.9,0.9,1.0 ]
lightSpecular = [ 1.0,1.0,1.0, 1.0 ]
lightPosition = [ 0,1000,1000,1.0 ]

windowWidth = 800
windowHeight = 600

index_position = 0
car_head = np.array([0,0,0])
last_position = np.array([0,0,0])
now_position = np.array([0,0,0])

slow = 0

def readPath():
    xyz = open("Path.xyz", 'r')
    coordinates = []
    for line in xyz:
        x, y, z = line.split()
        coordinates.append([float(x), float(y), float(z)])
    coordinates = np.array(coordinates)
    xyz.close()
    return coordinates

def car_Matrix():
    global slow
    global index_position, last_position, now_position
    slow += 1
    if(slow > 2):
        slow = 0
        last_position = path[index_position]
        index_position = index_position + 1
    if(index_position >= len(path)):
        index_position = 0
    now_position = path[index_position]
    
    car_head = now_position - last_position
    
    w = car_head
    w = w / np.linalg.norm(w)
    U = np.array([0,0,1])
    u = np.cross(U,w)
    u = u / np.linalg.norm(u)
    v = np.cross(w,u)
    M = [ [u[0], v[0], w[0], now_position[0] + 5*u[0] + 2*v[0]],
          [u[1], v[1], w[1], now_position[1] + 5*u[1] + 2*v[1]], 
          [u[2], v[2], w[2], now_position[2] + 5*u[2] + 2*v[2]], 
          [0., 0., 0., 1.] ]
    MinvT = np.transpose(M)
    matmatList = [MinvT[i][j] for i in range(4) for j in range(4)]

    car_translate = now_position + 5*u + 2*v
    car_roof = v
    
    return matmatList, car_translate, car_head, car_roof

def drawCoordinate():
    glLineWidth(3)
    glBegin(GL_LINES)
    glColor3f(1,0,0)
    glVertex3f(0,0,0)
    glVertex3f(100,0,0)
    glColor3f(0,1,0)
    glVertex3f(0,0,0)
    glVertex3f(0,100,0)
    glColor3f(0,0,1)
    glVertex3f(0,0,0)
    glVertex3f(0,0,100)
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glLightfv(GL_LIGHT0, GL_POSITION, lightPosition)
    matmatList, car_translate, car_head, car_roof = car_Matrix()
    glViewport(0, 0, windowWidth, windowHeight)
    glFrustum(-windowWidth/400,windowWidth/400,-windowHeight/400,windowHeight/400,5,4000)
    gluLookAt(car_translate[0], car_translate[1], car_translate[2],car_translate[0] + car_head[0], car_translate[1] + car_head[1], car_translate[2] + car_head[2], car_roof[0], car_roof[1], car_roof[2])

    glEnable(GL_LIGHTING)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    visualization.draw(meshes_map)
    glPopMatrix()
    
    glPushMatrix()
    glLoadMatrixf(matmatList)
    visualization.draw(meshes_car)
    glPopMatrix()

    glDisable(GL_LIGHTING)
    drawCoordinate()
    glutSwapBuffers()
    glutPostRedisplay()

def reshape(width,height):
    glViewport(0, 0, width, height)

def keyboard( key, x, y ):
    if key == esc:
        sys.exit()

path = readPath()
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
glutCreateWindow(b'CH04-Example')
glutReshapeWindow(windowWidth,windowHeight)
glutReshapeFunc(reshape)
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glLightfv(GL_LIGHT0, GL_AMBIENT, lightAmbient)
glLightfv(GL_LIGHT0, GL_DIFFUSE, lightAmbient)
glLightfv(GL_LIGHT0, GL_SPECULAR, lightSpecular)
glLightfv(GL_LIGHT0, GL_POSITION, lightPosition)
glutMainLoop()
