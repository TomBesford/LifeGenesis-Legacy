'''
Created on Jun 14, 2017

@author: Tom Besford

- Only supports 1 - 2 live states
- Write resize_lattice()
- Supports Moore and Von Neumann neighbourhoods with radius
- Does not support infinite grid
'''
from random import randrange

class CellularAutomaton():
    def __init__(self, width=30, height=30, edge='border', live_states=[1, 2], nhood_type='moore', nhood_radius=1, born=[3], survive=[2,3]):
        self.width = width
        self.height = height
        self.edge = edge
        self.live_states = live_states
        self.nhood_type = nhood_type
        self.nhood_radius = nhood_radius
        self.born = born
        self.survive = survive
        
        self.reset_data()
    
    def reset_data(self):
        self.data = null_lattice_data(self.width, self.height)
    
    def iterate(self, n=1):#Do 'n' iterations
        for i in range(n):
            next_iteration = null_lattice_data(self.width, self.height)
            
            for y in range(self.height):
                for x in range(self.width):
                    nhood = []#Create list of adjacent cells
                    
                    for ny in range(2*self.nhood_radius+1):
                        if self.nhood_type is 'moore':
                            nhood_xlength = ny*2+1
                        elif self.nhood_type is 'von-neumann':
                            nhood_xlength = 2*self.nhood_radius+1
                        for nx in range(nhood_xlength):
                            if self.nhood_type is 'moore':
                                xx = x-self.nhood_radius+nx
                            elif self.nhood_type is 'von-neumann':
                                xx = x-ny+nx
                            yy = y-self.nhood_radius+ny
                    
                            if xx is not x or yy is not y:
                                if self.edge is 'border':
                                    if xx >= 0 and xx < self.width and yy >= 0 and yy < self.height:
                                        nhood.append(self.data[yy][xx])
                    
                                elif self.edge is 'wrapped':
                                    if xx < 0:
                                        xx += self.width
                                    elif xx > self.width-1:
                                        xx -= self.width
                                    if yy < 0:
                                        yy += self.height
                                    elif yy > self.height-1:
                                        yy -= self.height
                                    nhood.append(self.data[yy][xx])
                    
                                elif self.edge is 'infinite':
                                    nhood.append(self.data[yy][xx])

                    nhood.sort()#Remove dead cells from list
                    if nhood.count(0) == len(nhood):
                        nhood = []
                    else:
                        nhood = nhood[nhood.count(0):]
                    
                    if self.data[y][x] is 0:#If cell is dead
                        if self.born.count(len(nhood)) > 0:#Only supports 2 live states
                            unique_states = []
                            for cell in nhood:
                                if unique_states.count(cell) is 0:
                                    unique_states.append(cell)
                            
                            if len(unique_states) is 1:
                                next_iteration[y][x] = unique_states[0]
                            
                            elif len(unique_states) is len(nhood):
                                #next_iteration[y][x] = a new state
                                pass
                            
                            elif nhood.count(unique_states[0]) > nhood.count(unique_states[1]):
                                next_iteration[y][x] = unique_states[0]
                            elif nhood.count(unique_states[0]) < nhood.count(unique_states[1]): 
                                next_iteration[y][x] = unique_states[1]
                        else:
                            next_iteration[y][x] = 0
                    
                    else:#If cell is live
                        if self.survive.count(len(nhood)) > 0:
                            next_iteration[y][x] = self.data[y][x]
                        else:
                            next_iteration[y][x] = 0                    
            
            self.data = next_iteration
    
    def randomise_data(self, states, num):#live_states = List of live states, num = number of each live state to create
        self.reset_data()
        
        if num * len(states) < self.width * self.height:#If there's enough space for the cells you're trying to create
            for state in states:
                if self.live_states.count(state) > 0:#If the cell you're trying to create is allowed
                    for i in range(num):
                        placed = False
                        
                        while placed is False:
                            x = randrange(0, self.width)
                            y = randrange(0, self.height)
                            if self.data[y][x] is 0:
                                self.data[y][x] = state
                                placed = True
    
    def resize_lattice(self, perspective, width, height):
        #change lattice dimensions without wiping data
        pass
    
    def print_to_console(self):
        for line in self.data: print ' '.join(str(cell) for cell in line)

def null_lattice_data(w, h):#Returns an empty grid 
    return [[0 for y in range(h)]for x in range(w)]