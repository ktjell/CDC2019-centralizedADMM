# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 14:46:01 2019

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
from scipy.optimize import minimize
import matplotlib.pyplot as plt

class party(Thread):
    
    def __init__(self, F, P, t, i, q, com, f, ite, retur, const):
        Thread.__init__(self)
        self.c = 0
        self.comr = 0
        self.F = F
        self.P = P
        self.t = t
        self.i = i
        self.q = q
        self.f = f
        self.ite = ite
        self.com = com
        self.comtime = 0
        self.recv = {}
        self.retur = retur
        self.const = const
        
    def readQueue(self):
        while not self.q.empty():
            b = self.q.get()
            self.recv[b[0]] = b[1]
#            self.q2.put([b[0][-1], b[1]])
        
    def get_val(self, name):
        while name not in self.recv:
            self.readQueue()
        res = self.recv[name]
        del self.recv[name]
        return res        
            
    def broadcast(self, name, val):
        for i in range(self.P):
            self.com.comParty(ips.party_addr[i], [name + str(self.i), val])
    
    def get_broadcast(self, name):
        res = []
        for i in range(self.P):
            res.append(self.get_val(name+str(i)))
        return res
                    
    def reconstruct_secret(self, name):
        res = self.get_broadcast(name)
        return ss.rec(self.F, res)
    
    def distribute_shares(self, name, val):
        shares = ss.share(self.F, val, self.t, self.P)
        for i in range(self.P):
            self.com.comParty(ips.party_addr[i], [name + str(self.i), shares[i]])

    def run(self):
        x_ar = []
        for ii in range(self.ite):
            
            #RECIEVING FROM Parties:
            rec = self.get_val('out'+str(ii))
            beta1 = rec[0]
            beta2= rec[1]

            g = lambda x: self.f(x) +  beta1 * x**2 + beta2 * x
            res = minimize(g, x0=0)
            x = res['x'][0]
            print('Party', self.i, 'x: ', x)
            x_ar.append(x)
            self.retur.put(x)
            self.distribute_shares('in'+str(ii+1), int(self.const*x))

        
#        plt.plot(x_ar)
        