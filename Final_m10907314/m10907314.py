import sys
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
from cv2 import *

from pywavefront import visualization
import pywavefront

meshes = pywavefront.Wavefront('COMBINE.obj')

mouseLeftPressed = 0
mouseRightPressed = 0
clickPt = np.array([0,0])
transfMatrix = np.eye(4,dtype=float)

lightAmbient = [ 0.4,0.4,0.4,1.0 ]
lightDiffuse = [ 0.9,0.9,0.9,1.0 ]
lightSpecular = [ 1.0,1.0,1.0, 1.0 ]
lightPosition = [ 0,0,0,1.0 ]

windowWidth = 800
windowHeight = 600

def drawGrid():
    glLineWidth(1)
    glBegin(GL_LINES)
    for y in range(0, 20):
        glColor3f(1-y/19,0,0)
        glVertex3f(0,10*y,0)
        glVertex3f(200,10*y,0)
    glEnd()
    glBegin(GL_LINES)
    for x in range(0, 20):
        glColor3f(0,1-x/19,0)
        glVertex3f(10*x,0,0)
        glVertex3f(10*x,200,0)
    glEnd()
    
def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glLightfv(GL_LIGHT0, GL_POSITION, lightPosition)
    glViewport(0, 0, int(windowWidth/2.0), windowHeight)
    glFrustum(-400/1000, 400/10000,-600/1000, 600/1000, 1.0, 5000) #修改視野大小
    gluLookAt(0,-10,0,0,0,100,0,1,0) #修改相機位置至原點
    glEnable(GL_LIGHTING)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    global transfMatrix
    transfMatrixT = np.transpose(transfMatrix)
    matmatList = [transfMatrixT[i][j] for i in range(4) for j in range(4)]
    glLoadMatrixf(matmatList)
    visualization.draw(meshes)
    glPopMatrix()
    glDisable(GL_LIGHTING)
    drawGrid()
    
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glLightfv(GL_LIGHT0, GL_POSITION, lightPosition)
    glViewport(int(windowWidth/2.0), 0, int(windowWidth/2.0), windowHeight)
    glFrustum(-400/1000, 400/10000,-600/1000, 600/1000, 1.0, 5000) #修改視野大小
    gluLookAt(0,10,0,0,0,100,0,1,0) #修改相機位置至原點
    glEnable(GL_LIGHTING)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    
    transfMatrixT = np.transpose(transfMatrix)
    matmatList = [transfMatrixT[i][j] for i in range(4) for j in range(4)]
    glLoadMatrixf(matmatList)
    visualization.draw(meshes)
    glPopMatrix()
    glDisable(GL_LIGHTING)
    drawGrid()
    
    glutSwapBuffers()


def reshape(width,height):
    glViewport(0, 0, width, height)

def keyboard( key, x, y ):
    if key == b'\x1b': #ESC
        print('terminate program')
        sys.exit()

def keyboardSpecial(key,x,y):
    global xv
    global yv
    if key==100:
        print('Left')
    elif key == 102:
        print('Right')
    elif key == 101:
        print('Up')
    elif key == 103:
        print('Down')
    else:
        print('No definition')
    #display()    
        
def MouseFunc(button, state, x, y):
    global mouseLeftPressed, mouseRightPressed, clickPt
    if state == 1:
        if button == 0:
            mouseLeftPressed = 0
        if button == 2:
            mouseRightPressed = 0
    else:
        if button == 0:
            mouseLeftPressed = 1
        if button == 2:
            mouseRightPressed = 1
        clickPt = np.array([x,y])
        
	
def MouseMotion(x, y):
    global mouseLeftPressed, mouseRightPressed, clickPt, transfMatrix
    if mouseLeftPressed==1:
        dR = np.array( [ x-clickPt[0] , -1*(y-clickPt[1]) ] )
        dxyz = np.array( [ transfMatrix[0][3] , transfMatrix[1][3], transfMatrix[2][3]] )
        rRatio = 100.0
        Tinv= np.array([ [ 1.0, 0.0, 0.0, -dxyz[0] ],\
                         [ 0.0, 1.0, 0.0, -dxyz[1] ],\
                         [ 0.0, 0.0, 1.0, -dxyz[2] ],\
                         [ 0.0, 0.0, 0.0,     1.0  ] ])
        T= np.array([ [ 1.0, 0.0, 0.0, dxyz[0] ],\
                      [ 0.0, 1.0, 0.0, dxyz[1] ],\
                      [ 0.0, 0.0, 1.0, dxyz[2] ],\
                      [ 0.0, 0.0, 0.0,    1.0  ] ])
        Rx = np.array([ [ 1.0, 0.0, 0.0, 0.0 ],\
                        [ 0.0, cos(dR[1]/rRatio), -sin(dR[1]/rRatio), 0.0 ],\
                        [ 0.0, sin(dR[1]/rRatio), cos(dR[1]/rRatio), 0.0 ],\
                        [ 0.0, 0.0, 0.0, 1.0 ] ])
        Ry = np.array([ [ cos(dR[0]/rRatio), 0.0, sin(dR[0]/rRatio), 0.0 ],\
                        [ 0.0, 1.0, 0.0, 0.0 ],\
                        [ -sin(dR[0]/rRatio), 0.0, cos(dR[0]/rRatio), 0.0 ],\
                        [ 0.0, 0.0, 0.0, 1.0 ] ])
        transfMatrix = Tinv.dot(transfMatrix)
        transfMatrix = Rx.dot(transfMatrix)
        transfMatrix = Ry.dot(transfMatrix)
        transfMatrix = T.dot(transfMatrix)
        display()
    if mouseRightPressed==1:
        dT = np.array( [ x-clickPt[0] , y-clickPt[1] ] )
        Tmatrix = np.array([ [ 1.0, 0.0, 0.0,  dT[0]],\
                             [ 0.0, 1.0, 0.0, -dT[1]],\
                             [ 0.0, 0.0, 1.0,   0.0 ],\
                             [ 0.0, 0.0, 0.0,   1.0 ] ])
        transfMatrix = Tmatrix.dot(transfMatrix)
        display()
    clickPt = np.array([x,y])


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
glutCreateWindow(b'CH10-Example')
glutReshapeWindow(windowWidth,windowHeight)
glutReshapeFunc(reshape)
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutSpecialFunc(keyboardSpecial)
glutMouseFunc(MouseFunc)
glutMotionFunc(MouseMotion)
glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glLightfv(GL_LIGHT0, GL_AMBIENT, lightAmbient)
glLightfv(GL_LIGHT0, GL_DIFFUSE, lightAmbient)
glLightfv(GL_LIGHT0, GL_SPECULAR, lightSpecular)
glLightfv(GL_LIGHT0, GL_POSITION, lightPosition)
glutMainLoop()
