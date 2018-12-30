'''
Conways Game of Life simulator
'''
import random

class CellularAutomaton():
    '''
    Simulates a cellular automaton
    '''
    def __init__(self, size=0):
        self.size = size
        self.data = self.null_lattice_data()

    def reset_data(self):
        '''
        Set every value in data to 0
        '''
        self.data = self.null_lattice_data()

    def iterate(self):
        '''
        Advance simulation by 1 generation
        '''
        next_iteration = self.null_lattice_data()

        for y in range(self.size):
            for x in range(self.size):

                #Create list of adjacent live cells
                nhood = []

                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if dx != 0 or dy != 0:
                            if all([
                                x + dx >= 0,
                                x + dx < self.size,
                                y + dy >= 0,
                                y + dy < self.size,
                                ]):
                                if self.data[y + dy][x + dx] != 0:
                                    nhood.append(self.data[y + dy][x + dx])

                #If cell is dead
                if self.data[y][x] == 0 and len(nhood) == 3:
                    if nhood.count(1) > nhood.count(2):
                        next_iteration[y][x] = 1
                    else:
                        next_iteration[y][x] = 2

                #If cell is live
                elif self.data[y][x] != 0 and (len(nhood) == 2 or len(nhood) == 3):
                    next_iteration[y][x] = self.data[y][x]

        self.data = next_iteration

    def randomise_data(self, num):
        '''
        Add random data
        '''
        self.reset_data()

        if num < self.size * self.size:
            for state in range(1, 3):
                for i in range(num):
                    placed = False

                    while not placed:
                        x = random.randrange(0, self.size)
                        y = random.randrange(0, self.size)
                        if self.data[y][x] == 0:
                            self.data[y][x] = state
                            placed = True

    def null_lattice_data(self):
        '''
        Returns list of lists with every value set to 0
        '''
        return [[0 for y in range(self.size)]for x in range(self.size)]

    def copy_data(self):
        '''
        Returns a copy of data
        '''
        data_copy = []
        for row in self.data:
            data_copy.append(list(row))
        return data_copy
