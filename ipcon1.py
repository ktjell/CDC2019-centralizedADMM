# -*- coding: utf-8 -*-
"""
Created on Thu May  9 14:14:40 2019

@author: kst
"""

class ipconfigs:
    port = 62
    
    party_addr =  ['192.168.100.1', #P0
                   '192.168.100.2', #P1
                   '192.168.100.3', #P2
                  ]
    agent_addr = [
                  '192.168.100.4',
                  '192.168.100.5',
                  '192.168.100.6',
                 ]
    
    
    
    ccu_adr = '192.168.100.246'
    
    server_addr = [[ccu_adr, 4002], #P0
                   [ccu_adr, 4003], #P1
                   [ccu_adr, 4007], #P2
                   [ccu_adr, 4008], #P3
                   [ccu_adr, 4010], #Reciever 4
                   [ccu_adr, 4011]  #Reciever 5
                  ]
    
class network:
    
    N = [[0,1,2],
         [0,1,2],
         [0,1,2,5],
         [3,4,5],
         [3,4,5],
         [2,3,4,5]            
        ]
    
    C = [[[1,0,1,2]],
         [[1,0,1,2]],
         [[1,0,1,2]],
         [[2,3,4,5]],
         [[2,3,4,5]],
         [[2,3,4,5]]
        ]
    
    VC =[[],
         [[2,1,5]],
         [[2,1,5],[5,2,3]],
         [[5,2,3]],
         [],
         [[2,1,5],[5,2,3]]
        ]
    
    W = [[[1,1,1]],
         [[1,1,2]],
         [[1,1,1]],
         [[1,1,2]],
         [[1,1,1]],
         [[1,1,1]]
        ]
    
    VW =[[],
         [2],
         [1,1],
         [2],
         [],
         [1,1]
        ]
    



#    
#    
#    
#    
    