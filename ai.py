'''
AI for playing against computer
'''
import random
import cellular_automaton

def get_end_node(master):
    '''
    Returns 2 tuples.
    '''
    nodes = get_nodes(master.sim)
    end_node = nodes[0]

    for node in nodes:
        if master.options['Difficulty'].get() == 2 and node.red > end_node.red:
            end_node = node
        elif master.options['Difficulty'].get() == 0 and node.red < end_node.red:
            end_node = node

    if master.options['Difficulty'].get() == 1:
        end_node = nodes[random.randrange(len(nodes))]

    return end_node.create, end_node.destroy

def get_nodes(sim):
    '''
    Returns list of objects.
    '''
    nodes = []
    empty_cells = []
    blue_cells = []
    for y, row in enumerate(sim.data):
        for x, cell in enumerate(row):
            if cell == 0:
                isolated = True
                for dy in range(-2, 3):
                    for dx in range(-2, 3):
                        try:
                            if sim.data[y+dy][x+dx] != 0:
                                isolated = False
                        except IndexError:
                            pass
                if not isolated:
                    empty_cells.append((x, y))
            elif cell == 1:
                isolated = True
                for dy in range(-2, 3):
                    for dx in range(-2, 3):
                        try:
                            if (dx != 0 or dy != 0) and sim.data[y+dy][x+dx] != 0:
                                isolated = False
                        except IndexError:
                            pass
                if not isolated:
                    blue_cells.append((x, y))

    for empty_cell in empty_cells:
        for blue_cell in blue_cells:
            nodes.append(Node(sim.copy_data(), empty_cell, blue_cell))

    return nodes

class Node():
    '''
    Object representing a possible move

    Attributes:
    create - A tuple containing x/y coordinates for creating the red cell
    destroy - A tuple containing x/y coordinates for killing the blue cell
    data - The grid that would result from this move
    red - Number of red cells resulting from this move
    blue - Number of blue cells resulting from this move
    '''
    def __init__(self, data, create, destroy):
        self.create = create
        self.destroy = destroy
        self.data = data
        self.update_data()
        self.red, self.blue = self.count_cells()

    def update_data(self):
        '''
        Applies changes to this nodes copy of the grid data and does one iteration
        '''
        sim = cellular_automaton.CellularAutomaton(len(self.data))
        sim.data = self.data
        sim.data[self.create[1]][self.create[0]] = 2
        sim.data[self.destroy[1]][self.destroy[0]] = 0
        sim.iterate()

    def count_cells(self):
        '''
        Returns 2 integers
        '''
        red = 0
        blue = 0
        for row in self.data:
            blue += row.count(1)
            red += row.count(2)
        return red, blue
