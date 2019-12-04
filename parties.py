# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 14:44:47 2019

@author: kst
"""

import numpy as np
from threading import Thread
import FFArithmetic as field
import shamir_scheme as ss
import proc
import time
from ipcon1 import ipconfigs as ips
import queue as que
  
        
class party(Thread):
    
    def __init__(self, F, x, A, P, t, i, q, com, B, c, ite, const, prime, qRetur):
        Thread.__init__(self)
        self.c = 0
        self.comr = 0
        self.F = F
        self.x = x
        self.A = A
        self.P = P
        self.t = t
        self.i = i
        self.q = q
        self.com = com
        self.B = B
        self.c = c
        self.ite = ite
        self.comtime = 0
        self.recv = {}
        self.const = const
        self.prime = prime
        self.qRetur = qRetur
        self.counter = 0
        
    def readQueue(self):
        while not self.q.empty():
            b = self.q.get()
            self.recv[b[0]] = b[1]
            if int(b[0][-1]) < 5:
                self.qRetur.put([b[0][-1], [self.counter, float(str(b[1]))/7979490791]])
                self.counter +=1

#            self.q2.put([b[0][-1], b[1]])
        
    def get_val(self, name):
        while name not in self.recv:
            self.readQueue()
        res = self.recv[name]
        del self.recv[name]
        return res        
            
    def broadcast(self, name, val):
        for i in range(self.P):
            self.com.comParty(ips.party_addr[i], [name + str(self.i+5), val])
    
    def get_broadcast(self, name):
        res = []
        for i in range(self.P):
            res.append(self.get_val(name+str(i+5)))
        return res
                    
    def reconstruct_secret(self, name):
        res = self.get_broadcast(name)
        return ss.rec(self.F, res)
    
    def distribute_shares(self, name, val):
        shares = ss.share(self.F, val, self.t, self.P)
        for i in range(self.P):
            self.com.comParty(ips.party_addr[i], [name + str(self.i), shares[i]])

    def run(self):

## GET INPUT SHARINGS FROM ALL PARTIES
        m = self.B.shape[0]
        m1= self.B.shape[1]
        lam = np.zeros(m, dtype = np.int)
        rho = 2
        x = np.zeros(m1, dtype = np.int)
        
    
        #START CALCULATIONS:
                
        for ii in range(self.ite):
            #RECIEVING FROM AGENTS:
            if ii != 0:
                input_shares = []
                for i in range(self.A):
                    input_shares.append(self.get_val('in'+str(ii) + str(i)))
            else:
                input_shares = self.x
            x_bar = np.array(input_shares) 
#            print(np.dot(self.B,x_bar), self.i, 'in parties')
            #START CALCULATIONS:
#            x_temp1 = []
#            for j,item in enumerate(x_bar):
#                self.broadcast('xbar'+str(j+5), item)
#                x_temp1.append(self.reconstruct_secret('xbar'+str(j+5)))
#            
#            if self.i == 0:
#                print(x_temp1)
            
            x_temp = (self.const*x).astype(int)-x_bar
            x_temp1 = []
            for j,item in enumerate(x_temp):
                self.broadcast('xtemp'+str(j), item)
                x_temp1.append(self.reconstruct_secret('xtemp'+str(j)))
            xtemp1 = [float(str(j))-self.prime if float(str(j)) > self.prime/2 else float(str(j)) for j in x_temp1]
            x_temp2 = [j * 1/(self.const*(self.A+1)) for j in xtemp1]
            x = x -  x_temp2
#            if self.i==0:
#                print(x)
            
            #            self.distribute_shares('xtemp1', x_temp1/self.A)
#            x_s = self.get_val('xtemp1')
            
            lam_bar =(lam*self.const).astype(int) + rho * (np.dot(self.B, x_bar)-self.c*self.const)
#            lam_temp1 = []
#            for j,item in enumerate(lam_bar):
#                self.broadcast('lamtemp1'+str(j), item)
#                lam_temp1.append(self.reconstruct_secret('lamtemp1'+str(j)))
#            if self.i == 0:
#                print('this', lam_temp1)
            lam_temp = ((lam*self.const).astype(int) - lam_bar)
            lam_temp1 = []
            for j,item in enumerate(lam_temp):
                self.broadcast('lamtemp'+str(j), item)
                lam_temp1.append(self.reconstruct_secret('lamtemp'+str(j)))
            lamtemp1 = [float(str(j))-self.prime if float(str(j)) > self.prime/2 else float(str(j)) for j in lam_temp1]
            lam_temp2 = [float(str(j))* 1/(self.const*(self.A+1)) for j in lamtemp1]
            lam = lam - lam_temp2
#            if self.i == 0:
#                print(lam)
#                print('lam', lam)
#                print(self.B)
#                print(self.c)
#                print(x)

            beta1 = []
            beta2 = []
            for i in range(m1):
                beta1.append((rho/2) * np.sum(self.B[:,i]**2))
                temp = []
                for j in range(m):
                    temp2 = [] 
                    for kk in range(m1):
                        if i != kk:
                            temp2.append(self.B[j,kk]*x[kk])
                            
#                    if self.i==0:
#                        print(self.B[j,i]* 
#                    (lam[j] - rho*self.c[j] + rho*sum(temp2)))
                    temp.append(self.B[j,i]* 
                    (lam[j] - rho*self.c[j] + rho*sum(temp2))
                            )
                beta2.append(sum(temp))
            
#            if self.i == 0:
#                print(beta1, beta2)
#            
            #TRANSMISSION TO AGENTS:
            if self.i == 0:
                for jj in range(self.A):
                     self.com.comAgent(ips.agent_addr[jj], ['out' + str(ii), [beta1[jj], beta2[jj]]])

                
            
#            for jj in range(self.A):
#                self.com.comAgent(ips.agent_addr[jj], ['out' + str(ii) + str(self.i), [beta1[jj], beta2[jj]]])
            
            