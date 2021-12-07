import sys
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

windowWidth = 800
windowHeight = 600

angle_minute = 0
angle_hour = 0

allVertex=[[-25.0000,15.0000,1.0000],
[-15.0000,15.0000,1.0000],
[70.0000,110.0000,1.0000],
[-25.0000,25.0000,1.0000],
[-28.0610,20.0000,0.5000],
[-20.0000,11.9390,0.5000],
[84.7932,20.0000,0.5000],
[-20.0000,28.0610,0.5000],
[60.2126,-86.5632,0.0000],
[90.0000,-90.0000,0.0000],
[119.7874,-86.5632,0.0000],
[147.1424,-76.7753,0.0000],
[32.8576,-76.7753,0.0000],
[171.2812,-61.4200,0.0000],
[8.7188,-61.4201,0.0000],
[-11.4200,-41.2812,0.0000],
[191.4200,-41.2812,0.0000],
[206.7753,-17.1424,0.0000],
[216.5632,10.2126,0.0000],
[220.0000,40.0000,0.0000],
[216.5632,69.7874,0.0000],
[206.7753,97.1424,0.0000],
[191.4200,121.2812,0.0000],
[171.2812,141.4200,0.0000],
[147.1423,156.7753,0.0000],
[119.7874,166.5632,0.0000],
[90.0000,170.0000,0.0000],
[60.2126,166.5632,0.0000],
[32.8576,156.7753,0.0000],
[8.7188,141.4200,0.0000],
[-11.4201,121.2812,0.0000],
[-26.7753,97.1423,0.0000],
[-36.5632,69.7874,0.0000],
[-40.0000,40.0000,0.0000],
[-36.5632,10.2126,0.0000],
[-26.7753,-17.1424,0.0000]]

# 2 triangles
hourHand=[[0,1,2],[3,0,2]]

# 2 triangles
minuteHand=[[4,5,6],[7,4,6]]

# 26 triangles
clockBody=[[8,9,10],
[8,10,11],
[12,8,11],
[12,11,13],
[14,12,13],
[15,14,13],
[15,13,16],
[15,16,17],
[15,17,18],
[15,18,19],
[15,19,20],
[15,20,21],
[15,21,22],
[15,22,23],
[15,23,24],
[15,24,25],
[15,25,26],
[15,26,27],
[15,27,28],
[15,28,29],
[15,29,30],
[15,30,31],
[15,31,32],
[15,32,33],
[15,33,34],
[15,34,35]]

def drawClock():
    glColor3f(1,1,1)
    glBegin(GL_TRIANGLES) 
    for fID in clockBody:
        glVertex3fv(allVertex[fID[0]])
        glVertex3fv(allVertex[fID[1]])
        glVertex3fv(allVertex[fID[2]])
    glEnd()


def drawhourHand():
    glColor3f(1,0,0)
    
    #要倒過來看 會先乘以glTranslatef(20,-20,0)平移矩陣
    glTranslatef(90,40,0)           #第四步:將時針平移至時鐘上
    glRotatef(-1*angle_hour,0,0,1)  #第三步:乘以-1是為了轉順時鐘方向，旋轉angle_hour角度
    glRotatef(45,0,0,1)             #第二步:將時針旋轉45度從原本一點半鐘方向移到12點鐘方向
    glTranslatef(20,-20,0)          #第一步:移到原點(0,0,0)
    glBegin(GL_TRIANGLES) 
    for fID in hourHand:
        glVertex3fv(allVertex[fID[0]])
        glVertex3fv(allVertex[fID[1]])
        glVertex3fv(allVertex[fID[2]])
    glEnd()

def drawminuteHand():
    glColor3f(0,2,0)
    
    #要倒過來看 會先乘以glTranslatef(20,-20,0)平移矩陣
    glTranslatef(90,40,0)            #第四步:將分針平移至時鐘上
    glRotatef(-1*angle_minute,0,0,1) #第三步:乘以-1是為了轉順時鐘方向，旋轉angle_minute角度
    glRotatef(90,0,0,1)              #第二步:將分針旋轉90度從原本三點鐘方向移到12點鐘方向
    glTranslatef(20,-20,0)           #第一步:移到原點(0,0,0)
    glBegin(GL_TRIANGLES) 
    for fID in minuteHand:
        glVertex3fv(allVertex[fID[0]])
        glVertex3fv(allVertex[fID[1]])
        glVertex3fv(allVertex[fID[2]])
    glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glViewport(0, 0, windowWidth, windowHeight)
    glOrtho(-float(windowWidth)/2.0,float(windowWidth)/2.0,-float(windowHeight)/2.0,float(windowHeight)/2.0,-windowHeight*10.0,windowHeight*10.0)
    

    global angle_minute,angle_hour #function內使用全域變數
    angle_minute += 6 #每過一次分針就多6度
    
    #分針轉360度時，時針轉6度並把分針數值歸0
    if angle_minute == 360:
        angle_hour += 6
        angle_minute = 0
        
    #時針轉360度時，把時針數值歸0
    if angle_hour == 360:
        angle_hour = 0
        
    #分三個glPushMatrix和glPopMatrix 這樣就不會互相影響旋轉和平移矩陣
    glPushMatrix()
    drawClock()
    glPopMatrix()
    
    glPushMatrix()
    drawhourHand()
    glPopMatrix()
    
    glPushMatrix()
    drawminuteHand()
    glPopMatrix()
    
    glutSwapBuffers()
    glutPostRedisplay()

def reshape(width,height):
    glViewport(0, 0, width, height)

def keyboard( key, x, y ):
    if key == esc:
        sys.exit()

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
glutCreateWindow(b'Homework2')
glutReshapeWindow(800,600)
glutReshapeFunc(reshape)
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMainLoop()
