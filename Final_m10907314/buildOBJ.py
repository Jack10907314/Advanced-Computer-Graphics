import numpy as np
import math
import cv2

np.set_printoptions(suppress=False)
circle_count_K = 100 #phi解析度K
line_count_N =  100 #theta解析度N
sphere_radius = 100 #球體半徑
image_ratio = 0.8 #取相片的百分比圓

K = circle_count_K
N = line_count_N

#section = np.zeros((K,N), dtype=float)
point = np.zeros((K+1,N+1,3), dtype=float) #所有的空間座標點
index = np.zeros((K+1,N+1,), dtype=int) #紀錄obj內的v/vt/vn的index位置
half_total_point_count = (K+1) * (N+1) #紀錄另一半的點index起始位置

#讀入兩張圖片並合併成一張圖片輸出
img_FRONT = cv2.imread("FRONT.JPG")
img_REAR = cv2.imread("REAR.JPG")
img_combine = np.hstack((img_FRONT, img_REAR))
cv2.imwrite("COMBINE.JPG", img_combine)

def normal(start, end): #輸出為兩點的單位向量
    vector = np.zeros((3,), dtype=float)
    vector = end - start
    norm = np.linalg.norm(vector)
    if norm == 0: 
       return vector
    return vector / norm

#建立出半圓的所有空間座標點
for k in range(K+1):
    for n in range(N+1):
        
        r = sphere_radius
        phi = math.pi/2 - math.pi*k/(2*K)
        theta = 2*math.pi*n/N
        
        x = r * math.cos(phi) * math.cos(theta)
        y = r * math.cos(phi) * math.sin(theta)
        z = r * math.sin(phi)

        point[k][n] = np.array([x,y,z])
        

#寫mtl檔
f = open("COMBINE.mtl",'w')
f.write("newmtl COMBINE\n")
f.write("Kd 1 1 1\n")
f.write("Ka 1 1 1\n")
f.write("Ks 1 1 1\n")
f.write("map_Kd COMBINE.JPG\n")
f.close()

#寫obj檔
f = open("COMBINE.obj",'w')
f.write("mtllib COMBINE.mtl\n")

# #-------------------front part-------------------
#寫obj內前半圓的v空間座標
for k in range(K+1):
    for n in range(N+1):
        f.write('v {x} {y} {z}\n'.format(x=format(point[k][n][0], '.30f'), 
                                          y=format(point[k][n][1], '.30f'), 
                                          z=format(point[k][n][2], '.30f')))
        index[k][n] = k*(N+1) + n + 1
f.write("\n")

#寫obj內前半圓的vt紋理座標
for k in range(K+1):
    for n in range(N+1):
        #標準化
        standard_x = (point[k][n][0] * image_ratio + sphere_radius) / (2 * sphere_radius)
        standard_y = (point[k][n][1] * image_ratio + sphere_radius) / (2 * sphere_radius)  #picture y正往下
        standard_x = standard_x / 2
        standard_y = standard_y
        f.write('vt {x} {y} 0\n'.format(x=format(standard_x, '.30f'), 
                                      y=format(standard_y, '.30f')))
f.write("\n")

#寫obj內前半圓的vn法向量
for k in range(K+1):
    for n in range(N+1):
        normal_vector = normal(point[k][n], np.array([0,0,0]))
        f.write('vn {x} {y} {z}\n'.format(x=format(normal_vector[0], '.30f'), 
                                          y=format(normal_vector[1], '.30f'), 
                                          z=format(normal_vector[2], '.30f')))
f.write("\n")

#寫obj內前半圓的f 四點成一個面
f.write("usemtl COMBINE\n")
for k in range(K):
    for n in range(N):
        f.write('f')
        f.write(' {index_v}/{index_vt}/{index_vn}'.format(index_v=index[k][n], index_vt=index[k][n], index_vn=index[k][n]))
        f.write(' {index_v}/{index_vt}/{index_vn}'.format(index_v=index[k][n+1], index_vt=index[k][n+1], index_vn=index[k][n+1]))
        f.write(' {index_v}/{index_vt}/{index_vn}'.format(index_v=index[k+1][n+1], index_vt=index[k+1][n+1], index_vn=index[k+1][n+1]))
        f.write(' {index_v}/{index_vt}/{index_vn}'.format(index_v=index[k+1][n], index_vt=index[k+1][n], index_vn=index[k+1][n]))
        f.write('\n')
        
        
# #-------------------rear part-------------------
#寫obj內後半圓的v空間座標
for k in range(K+1):
    for n in range(N+1):
        f.write('v {x} {y} {z}\n'.format(x=format(point[k][n][0] * -1, '.30f'), 
                                          y=format(point[k][n][1] * -1, '.30f'), 
                                          z=format(point[k][n][2] * -1, '.30f')))
        index[k][n] = k*(N+1) + n + 1 + half_total_point_count
f.write("\n")

#寫obj內後半圓的vt紋理座標
for k in range(K+1):
    for n in range(N+1):
        #標準化
        standard_x = (point[k][n][0] * image_ratio + sphere_radius) / (2 * sphere_radius)
        standard_y = (-1 * point[k][n][1] * image_ratio + sphere_radius) / (2 * sphere_radius)  #picture y正往下
        standard_x = standard_x / 2 + 0.5
        standard_y = standard_y
        f.write('vt {x} {y} 0\n'.format(x=format(standard_x, '.30f'), 
                                      y=format(standard_y, '.30f')))
f.write("\n")

#寫obj內後半圓的vn法向量
for k in range(K+1):
    for n in range(N+1):
        normal_vector = normal(point[k][n]*-1, np.array([0,0,0]))
        f.write('vn {x} {y} {z}\n'.format(x=format(normal_vector[0], '.30f'), 
                                          y=format(normal_vector[1], '.30f'), 
                                          z=format(normal_vector[2], '.30f')))
f.write("\n")

#寫obj內後半圓的f 四點成一個面
f.write("usemtl COMBINE\n")
for k in range(K):
    for n in range(N):
        f.write('f')
        f.write(' {index_v}/{index_vt}/{index_vn}'.format(index_v=index[k][n], index_vt=index[k][n], index_vn=index[k][n]))
        f.write(' {index_v}/{index_vt}/{index_vn}'.format(index_v=index[k+1][n], index_vt=index[k+1][n], index_vn=index[k+1][n]))
        f.write(' {index_v}/{index_vt}/{index_vn}'.format(index_v=index[k+1][n+1], index_vt=index[k+1][n+1], index_vn=index[k+1][n+1]))
        f.write(' {index_v}/{index_vt}/{index_vn}'.format(index_v=index[k][n+1], index_vt=index[k][n+1], index_vn=index[k][n+1]))
        f.write('\n')

f.close()