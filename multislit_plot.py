# coding: utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import random


def start_point(opening,blocking,distance):
    x = distance[0] - 1500
    y = (random.random() - 0.5)*(0.5*blocking[0] + 4*(blocking[0] + opening[0]))*2
    return x,y    

def line(x_0,y_0):
    y_max = 20  #mm
    x_max = 12750  #mm
    #k = (random.random()-0.5)*2*y_max/x_max
    k = (random.random()-0.5)*np.tan(1.2*np.pi/180)
    b = y_0 - k*x_0
    return k,b

def end_point(opening,blocking,distance,k,b):
    detector_pos = 34750
    y_1 = None
    for slit_i in range(len(distance)):
        cycle = blocking[slit_i]+opening[slit_i]
        x_1 = distance[slit_i]
        y_test = k*x_1+b
        y_test_2 = abs(y_test)%cycle        
        if (y_test_2 >= 0 and y_test_2 <= 0.5*blocking[slit_i]) or (y_test_2 >= 0.5*blocking[slit_i]+opening[slit_i] and y_test_2 <= cycle) or abs(y_test) >= 4*cycle:
            y_1 = y_test
            break
        elif y_test_2 > 0.5*blocking[slit_i] and y_test_2 < 0.5*blocking[slit_i]+opening[slit_i]:
            continue
    if y_1 == None:
        x_1 = detector_pos
        y_1 = k*x_1+b
    return x_1,y_1

def multislit_coord(opening,blocking,distance):
    multislit = []
    multislit_x = []
    for slit_index in range(len(distance)):
        slit = np.linspace(-0.5*blocking[slit_index],0.5*blocking[slit_index],5)
        block = []
        for block_i in range(-4,5):
            block.append(slit + (blocking[slit_index] + opening[slit_index])*block_i)
        multislit.append(block)
        multislit_x.append([distance[slit_index]]*5)  
    return multislit_x,multislit

def plot_slits_and_rays():
    absorb_num = {}
    for i in distance:
        absorb_num[i] = 0
    for i in range(30000):
        x_0,y_0 = start_point(opening,blocking,distance)
        k,b = line(x_0,y_0)
        x_1,y_1 = end_point(opening,blocking,distance,k,b)
        if x_1 in distance:
            absorb_num[x_1]+=1
        plt.plot([x_0,x_1],[y_0,y_1],color = 'red',ls = '-',linewidth = 0.1)
    for slit_i in range(len(distance)):
        for block_i in range(len(multislit[slit_i])):
            plt.plot(multislit_x[slit_i],multislit[slit_i][block_i],color = 'k')
            #plt.xlim((9000,34750))
    plt.rc('font',family = 'Times New Roman')
    plt.tick_params(axis = 'both',direction = 'in')
    plt.xlabel('Distance from moderator')
    plt.ylabel('Horizontal distance')
    plt.savefig('multislit_plot.png',format = 'png',dpi = 300, bbox_pixel = 'tight', transparent = True)
    return absorb_num

def plot_absorb_num(absorb_num):
    count = list(absorb_num.values())
    ratio = []
    for i in count:
        ratio.append(i/sum(count))
    fig = plt.figure()
    plt.rc('font',family = 'Times New Roman')
    ax = fig.add_subplot(111)
    ax.plot(distance,ratio,marker = 'o') 
    ax.set_xlabel('Distance from moderator')
    ax.set_ylabel('Absorbed ratio')
    plt.tick_params(axis = 'both',direction = 'in')
    plt.savefig('absorb_num.png',format = 'png',dpi = 300, bbox_pixel = 'tight', transparent = True)

    
    
    #ax.set_yscale('log')    

data = pd.read_csv('multi-slit_data.txt',sep= '\s+',index_col = None)

distance = list(data['distance'])
opening = list(data['opening'])
blocking = list(data['blocking'])
multislit_x,multislit =  multislit_coord(opening,blocking,distance)    
absorb_num = plot_slits_and_rays()
plot_absorb_num(absorb_num)

















