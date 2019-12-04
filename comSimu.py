# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 14:45:09 2019

@author: kst
"""
from ipcon1 import ipconfigs as ips

class communicationSimulation:
    def __init__(self,qP, qA):
        self.qP = qP
        self.qA = qA
        
    def comParty(self,add, val):
        index = ips.party_addr.index(add)
        if not self.qP[index].full():
            self.qP[index].put(val)
        else:
            print('KØ ER FULD!')
    
    def comAgent(self,add, val):
        index = ips.agent_addr.index(add)
        if not self.qA[index].full():
            self.qA[index].put(val)
        else:
            print('KØ ER FULD!')