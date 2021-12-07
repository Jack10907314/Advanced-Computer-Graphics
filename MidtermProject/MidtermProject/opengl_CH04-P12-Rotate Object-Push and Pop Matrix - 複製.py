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

def vector2DRotate(vector, angle):
    theta = np.radians(angle)
    cos, sin = np.cos(theta), np.sin(theta)
    rotate_matrix = np.array(((cos,-sin), (sin, cos))) #旋轉矩陣
    
    rotate_vector = np.dot(rotate_matrix, vector)
    
    return rotate_vector

def vector2DUnit(vector):
    vector = vector / np.sqrt(np.dot(vector,vector))
    return vector

def vector2DAngle(vector1, vector2):
    x1 = vector1[0]
    y1 = vector1[1]
    x2 = vector2[0]
    y2 = vector2[1]
    angle = 0
    
    angle1 = atan2(y1, x1)
    angle1 = int(angle1 * 180 / pi)

    angle2 = atan2(y2, x2)
    angle2 = int(angle2 * 180 / pi)

    angle = angle2 - angle1
    
    #print(angle)
    return angle
    
def axisRotate(vector1, vector2):
    x_rotate = 0
    y_rotate = 0
    z_rotate = 0
    
    yz_vector1 = np.array([vector1[1], vector1[2]])
    yz_vector2 = np.array([vector2[1], vector2[2]])
    zx_vector1 = np.array([vector1[2], vector1[0]])
    zx_vector2 = np.array([vector2[2], vector2[0]])
    xy_vector1 = np.array([vector1[0], vector1[1]])
    xy_vector2 = np.array([vector2[0], vector2[1]])
    
    x_rotate = vector2DAngle(yz_vector1, yz_vector2)
    y_rotate = vector2DAngle(zx_vector1, zx_vector2)
    z_rotate = vector2DAngle(xy_vector1, xy_vector2)
    
    global index_position
    print("index : " + str(index_position))
    print("x_rotate : " + str(x_rotate))
    print("y_rotate : " + str(y_rotate))
    print("z_rotate : " + str(z_rotate))
    return x_rotate, y_rotate, z_rotate

def carRotateAndTranslate():
    global slow
    global index_position, last_position, now_position
    slow += 1
    if(slow > 3):
        slow = 0
        last_position = path[index_position]
        index_position = index_position + 1
    if(index_position >= len(path)):
        index_position = 0
    now_position = path[index_position]
    
    car_head = now_position - last_position
    
    xy_car_head = np.array([car_head[0], car_head[1]])
    right_side = vector2DRotate(xy_car_head, -90)
    right_side = vector2DUnit(right_side)
    right_side = right_side * 5

    x_rotate, y_rotate, z_rotate = axisRotate(np.array([0,1,0]), car_head)
    
    car_translate = np.array([now_position[0] + right_side[0], now_position[1] + right_side[1], now_position[2] + 2])
    
    if(x_rotate > 90):
        x_rotate = 0
    elif(x_rotate < -90):
        x_rotate = 0
        
    return right_side, car_head, car_translate, x_rotate, y_rotate, z_rotate

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
    right_side, car_head, car_translate, x_rotate, y_rotate, z_rotate =carRotateAndTranslate()
    glViewport(0, 0, windowWidth, windowHeight)
    # glOrtho(-5,5,-5,5,-windowHeight*10.0,windowHeight*10.0)
    # glOrtho(-float(windowWidth)/10.0,float(windowWidth)/10.0,-float(windowHeight)/10.0,float(windowHeight)/10.0,-windowHeight*10.0,windowHeight*10.0)
    # glOrtho(-float(windowWidth)/2.0,float(windowWidth)/2.0,-float(windowHeight)/2.0,float(windowHeight)/2.0,-windowHeight*10.0,windowHeight*10.0)
    # gluLookAt(1,0,0,0,0,0,0,1,0)
    # glOrtho(-50,50,-50,50,-50,100)
    # gluLookAt(car_translate[0], car_translate[1], car_translate[2],car_translate[0] + right_side[0], car_translate[1] + right_side[1], car_translate[2],0,0,1)
    glFrustum(-windowWidth/400,windowWidth/400,-windowHeight/400,windowHeight/400,5,4000)
    gluLookAt(car_translate[0], car_translate[1], car_translate[2],car_translate[0] + car_head[0], car_translate[1] + car_head[1], car_translate[2] + car_head[2],0,0,1)
    # gluLookAt(0,0,1000,0,0,0,0,1,0)
    glEnable(GL_LIGHTING)
    
    glPushMatrix()
    visualization.draw(meshes_map)
    glPopMatrix()
    
    glPushMatrix()
    glTranslate(car_translate[0], car_translate[1], car_translate[2])
    glRotate(x_rotate,1,0,0)
    glRotate(z_rotate,0,0,1)
    glRotate(180,0,1,0)
    glRotate(-90,1,0,0)
    # glRotate(z_rotate,0,0,1)
    # glRotate(90,0,1,0)
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
