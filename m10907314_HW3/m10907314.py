import sys
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
from cv2 import *
import cv2

from pywavefront import visualization
import pywavefront

meshes = pywavefront.Wavefront('Dog.obj')
np_meshes = np.array(meshes.vertices)

#找meshes的最大最小x、y、z 
meshes_left = np.min(np_meshes[:,0])
meshes_right = np.max(np_meshes[:,0])
meshes_near = np.min(np_meshes[:,1])
meshes_far = np.max(np_meshes[:,1])
meshes_bottom = np.min(np_meshes[:,2])
meshes_top = np.max(np_meshes[:,2])

#計算長寬高的一半
meshes_width = (meshes_right - meshes_left) / 2
meshes_height = (meshes_top - meshes_bottom) / 2
meshes_depth = (meshes_far - meshes_near) / 2

#計算中心點的xyz點
meshes_center_x = meshes_left + meshes_width
meshes_center_y = meshes_near + meshes_depth
meshes_center_z = meshes_bottom + meshes_height

theda = 0
angle = 0

lightAmbient = [ 0.5,0.5,0.5,1.0 ]
lightDiffuse = [ 0.9,0.9,0.9,1.0 ]
lightSpecular = [ 1.0,1.0,1.0, 1.0 ]
lightPosition = [ 0,1000,1000,1.0 ]

#可自訂產生的圖片大小
bigWidth = 8000
bigHeight = 8000

windowWidth = int(bigWidth / 10)
windowHeight = int(bigHeight / 10)

BIGimg = np.zeros( [bigHeight,bigWidth,3] , dtype = np.uint8)
def display():
    global BIGimg
    #glFrustum看整張圖的left、right、bottom、top
    left = -meshes_width
    right = meshes_width
    bottom = -meshes_height
    top = meshes_height
    #將長寬各切十等分 並將圖片最後合併成高解析圖片
    for i in range(10):
        for j in range(10):
            #計算切割後的left、right、bottom、top的範圍
            small_width = (right - left) / 10
            small_height = (top - bottom) / 10
            small_left = left + small_width * i
            small_right = small_left + small_width
            small_bottom = bottom + small_height * j
            small_top = small_bottom + small_height

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glLightfv(GL_LIGHT0, GL_POSITION, lightPosition)
            glViewport(0, 0, windowWidth, windowHeight)
            #glFrustum最後的meshes_depth*2相機離meshes的距離，meshes_depth*4則是原本的meshes_depth*2 + meshes_depth*2涵蓋整個meshes範圍
            glFrustum(small_left, small_right, small_bottom, small_top, meshes_depth*2, meshes_depth*4)
            #相機是從meshes的中心點沿著y軸離meshes_depth*3放置，離meshes的最短距離為meshes_depth*2
            gluLookAt(meshes_center_x, meshes_center_y + meshes_depth*3, meshes_center_z,
                      meshes_center_x, meshes_center_y                 , meshes_center_z,
                      0,0,1)
            glEnable(GL_LIGHTING)
            visualization.draw(meshes)
            glDisable(GL_LIGHTING)
            
            #將opengl的畫面儲存下來，並放置BIGimg的指定的對應位置上
            colorBuffer = (GLubyte * int(windowWidth * windowHeight * 3))(0) # 1440000 == 800*600*3
            glReadPixels(0, 0, windowWidth, windowHeight, GL_BGR, GL_UNSIGNED_BYTE, colorBuffer)
            imgColorflip = np.fromstring(colorBuffer, np.uint8).reshape( windowHeight, windowWidth, 3 )
            imgColor = cv2.flip(imgColorflip, 0) 
            BIGimg[j*windowHeight:(j+1)*windowHeight,i*windowWidth:(i+1)*windowWidth] = imgColorflip 
            waitKey(10)

            glutSwapBuffers()
            
    #將BIGimg轉正後儲存
    BIGimg = cv2.flip(BIGimg, 0)
    cv2.imwrite("BIGimg.jpg",BIGimg)
    
    #將結果的BIGimg縮小顯示
    cv2.namedWindow("BIGimg", 0);
    cv2.resizeWindow("BIGimg", windowWidth, windowHeight);
    cv2.imshow("BIGimg", BIGimg)
    cv2.waitKey(10)

def reshape(width,height):
    glViewport(0, 0, width, height)

def keyboard( key, x, y ):
    if key == esc:
        sys.exit()


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
glutCreateWindow(b'CH05-Example')
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
