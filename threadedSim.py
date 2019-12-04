# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 14:47:14 2018

@author: kst
"""
import numpy as np
#import matplotlib.pyplot as plt
from threading import Thread
import FFArithmetic as field
import shamir_scheme as ss
import proc
from ipcon1 import ipconfigs as ips
import queue as que
import agents as ag
import parties as pa
import comSimu
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from multiprocessing import Process, Manager, Queue
import sched, time
import threading
# This function is responsible for displaying the data
# it is run in its own process to liberate main process
def display(name,q,xpos,ypos):
    app2 = QtGui.QApplication([])

    win2 = pg.GraphicsWindow(title="Basic plotting examples")
    win2.resize(680,550)
    win2.setWindowTitle('pyqtgraph example: Plotting')
    win2.move(xpos,ypos)
    p2 = win2.addPlot()
    curve0 = p2.plot(pen='y',symbol='o', symbolPen=None, symbolSize=10, symbolBrush=('b'))
    curve1 = p2.plot(pen='y',symbol='o', symbolPen=None, symbolSize=10, symbolBrush=('r'))
    curve2 = p2.plot(pen='y',symbol='o', symbolPen=None, symbolSize=10, symbolBrush=('g'))
    
    x0 = []
    y0 = []
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    c0=[-1]
    c1=[-1]
    c2=[-1]
    
    def updateInProc(curve0,curve1,curve2,q,x0,y0,x1,y1,x2,y2,c0,c1,c2):
        item = q.get()
        s = item[0]
        if s == '0':
            c0[0]+=1
            x0.append(c0[0])
            y0.append(item[1][1])
            curve0.setData(x0,y0)
        elif s=='1':
            c1[0]+=1
            x1.append(c1[0])
            y1.append(item[1][1])
            curve1.setData(x1,y1)
        elif s=='2':
            c2[0]+=1
            x2.append(c2[0])
            y2.append(item[1][1])
            curve2.setData(x2,y2)
            

    timer = QtCore.QTimer()
    timer.timeout.connect(lambda: updateInProc(curve0,curve1,curve2,q,x0,y0,x1,y1,x2,y2,c0,c1,c2))
    timer.start(50)

    QtGui.QApplication.instance().exec_()

def displayAgent(name,q,xpos,ypos):
    app2 = QtGui.QApplication([])

    win2 = pg.GraphicsWindow(title="Basic plotting examples")
    win2.resize(680,550)
    win2.setWindowTitle('pyqtgraph example: Plotting')
    win2.move(xpos,ypos)
    p2 = win2.addPlot()
    curve = p2.plot(pen='y',symbol='o', symbolPen=None, symbolSize=10, symbolBrush=('b'))

    x = []
    y = []
    c=[-1]
    
    def updateInProc(curve,q,x,y,c):
        item = q.get()
        c[0]+=1
        x.append(c[0])
        y.append(item)
        curve.setData(x,y)


    timer = QtCore.QTimer()
    timer.timeout.connect(lambda: updateInProc(curve,q,x,y,c))
    timer.start(50)

    QtGui.QApplication.instance().exec_()


def io(running,q):
    t = 0
    while running.is_set():
        s = np.sin(2 * np.pi * t)
        t += 0.01
        q.put([t,s])
        time.sleep(0.01)
    print("Done")

class test(Thread):
    party_addr = ips.party_addr
    def __init__(self, q1, q2):
        Thread.__init__(self)
        self.q1 = q1
        self.q2 = q2
        self.on = True
    def run(self):
        while self.on ==True:
            if not self.q1.empty():
                item = self.q1.get()
                self.q2.put(item)

if __name__ == '__main__':

    prime =7979490791 
    F = field.GF(prime)            
    A = 3       #number agents
    t = 1
    m = 2       #Number constraints
    ite = 100
    P = 3   #number computing parties
    const= 1000
    
    x = np.array([ss.share(F, 0, t, P) for i in range(A)])
    np.random.seed(1)
    f = []
    for k in range(A):
        f.append(lambda x: ((x-k)**2))
    
    
    E = np.random.randint(10, size = (m,A))
    #    
    #Q = np.random.randint(10,size=(m,1))
    #E = np.array([[-5,2],[5,1]]).transpose()
    #B = np.array([5,1])
    Q = np.array([2,5])
    
#    
    qP = [que.Queue() for i in range(P)]
    qA = [que.Queue() for i in range(A)]
    
    qAretur = [que.Queue() for i in range(A)]
    qPretur = [que.Queue() for i in range(P)]
    Que0 = Queue()
    Que1 = Queue()
    Que2 = Queue()
    QueA0 = Queue()
    QueA1 = Queue()
    QueA2 = Queue()
    retur = que.Queue()
     
    com = comSimu.communicationSimulation(qP, qA)


    tes0 = test(qPretur[0], Que0)
    tes0.start()
    tes1 = test(qPretur[1], Que1)
    tes1.start()
    tes2 = test(qPretur[2], Que2)
    tes2.start()
    tesA0 = test(qAretur[0], QueA0)
    tesA0.start()
    tesA1 = test(qAretur[1], QueA1)
    tesA1.start()
    tesA2 = test(qAretur[2], QueA2)
    tesA2.start()
    # Start display process
    pos1 = 580
    pos2 = 685
    ppp0 = Process(target=display, args=('bob',Que0, 0,pos1))
    ppp0.start()
    ppp1 = Process(target=display, args=('bob',Que1, pos2,pos1))
    ppp1.start()
    ppp2 = Process(target=display, args=('bob',Que1,2*pos2,pos1))
    ppp2.start()

    pppA0 = Process(target=displayAgent, args=('bob',QueA0,0,0))
    pppA0.start()
    pppA1 = Process(target=displayAgent, args=('bob',QueA1,pos2,0))
    pppA1.start()
    pppA2 = Process(target=displayAgent, args=('bob',QueA2,2*pos2,0))
    pppA2.start()
    parties = []
    for k in range(P):
        parties.append(pa.party(F, x[:,k], A, P, t, k, qP[k], com, E, Q, ite, const,prime, qPretur[k]))
    
    for p in parties:
        p.start()
    
    agents = []
    for k in range(A):   
        agents.append(ag.party(F, P, t, k, qA[k], com, f[k], ite, qAretur[k],const))
    
    for a in agents:
        a.start()
    
    for a in agents:
        a.join()   
#    #
##    plt.figure()
##    for a in range(A):    
##        l = []
##        for j in range(ite):
##            l.append(qAretur[a].get())
##        plt.plot(l)
#        
#        
#    for p in parties:
#        p.join()   
    input("Type any key to quit.")
    tes0.on =False
    tes1.on =False
    tes2.on =False
    tesA0.on=False
    tesA1.on=False
    tesA2.on=False
    
    ppp0.terminate()
    ppp0.join()
    ppp1.terminate()
    ppp1.join()
    ppp2.terminate()
    ppp2.join()
    
    pppA0.terminate()
    pppA0.join()
    pppA1.terminate()
    pppA1.join()
    pppA2.terminate()
    pppA2.join()