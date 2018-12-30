'''
Created on 24/04/2013

@author: Tom Besford
'''
import tkinter
import tkinter.messagebox
import math
import threading
import presets
import ai
import cellular_automaton

NAME = 'LifeGenesis Legacy'

class Main():
    '''
    Main class
    '''
    def __init__(self):
        #Attributes
        self.options = {'Size':30, 'Lines':True, 'Speed':70, 'Difficulty':tkinter.IntVar()}
        self.options['Difficulty'].set(2)
        self.size = self.options['Size']
        self.stop_repeat_flag = threading.Event()
        self.sim_id_list = []
        self.state = 'Idle'
        self.game_state = 'Create'
        self.sim = cellular_automaton.CellularAutomaton(self.size)

        self.build_menu()
        self.draw_sim()

    def build_menu(self):
        '''
        Create menu_bar
        '''
        menu_bar = tkinter.Menu(ROOT)

        self.patterns_menu = tkinter.Menu(menu_bar, tearoff=0)
        self.patterns_menu.add_command(
            label='Traffic Lights',
            command=lambda: self.preset('Traffic Lights')
            )
        self.patterns_menu.add_command(
            label='Honey Farm',
            command=lambda: self.preset('Honey Farm')
            )
        self.patterns_menu.add_command(
            label='Oscillators',
            command=lambda: self.preset('Oscillators')
            )
        self.patterns_menu.add_command(
            label='Pulsar',
            command=lambda: self.preset('Pulsar')
            )
        self.patterns_menu.add_command(
            label='Gliders',
            command=lambda: self.preset('Gliders')
            )
        self.patterns_menu.add_command(
            label='Spaceships',
            command=lambda: self.preset('Spaceships')
            )
        self.patterns_menu.add_command(
            label='Eater',
            command=lambda: self.preset('Eater')
            )
        self.patterns_menu.add_command(
            label='Virus',
            command=lambda: self.preset('Virus')
            )
        self.patterns_menu.add_separator()
        self.patterns_menu.add_command(
            label='Glider Gun',
            command=lambda: self.preset('Glider Gun')
            )

        self.life_menu = tkinter.Menu(menu_bar, tearoff=0)
        self.life_menu.add_command(
            label='Next',
            accelerator='F3',
            command=self.next_iteration
            )
        self.life_menu.add_command(
            label='Go',
            accelerator='F5',
            command=lambda: self.change_state('Running')
            )
        self.life_menu.add_command(
            label='Stop',
            accelerator='F6',
            command=lambda: self.change_state('Idle'),
            state='disabled'
            )
        self.life_menu.add_separator()
        self.life_menu.add_command(
            label='Clear',
            accelerator='F7',
            command=self.clear_grid
            )
        self.life_menu.add_command(
            label='Random',
            accelerator='F8',
            command=self.randomise_grid
            )
        self.life_menu.add_cascade(
            label='Patterns',
            menu=self.patterns_menu
            )
        self.life_menu.add_separator()
        self.life_menu.add_command(
            label='Options...',
            accelerator='F9',
            command=self.options_window
            )
        self.life_menu.add_separator()
        self.life_menu.add_command(
            label='Exit',
            command=ROOT.destroy
            )
        menu_bar.add_cascade(
            label='Life',
            menu=self.life_menu
            )

        self.game_menu = tkinter.Menu(menu_bar, tearoff=0)
        self.game_menu.add_command(
            label='New game',
            accelerator='F2',
            command=lambda: self.change_state('Game')
            )
        self.game_menu.add_command(
            label='Quit this game',
            command=lambda: self.change_state('Idle'),
            state='disabled'
            )
        self.game_menu.add_separator()
        self.game_menu.add_radiobutton(
            label='Easy',
            variable=self.options['Difficulty'],
            value=0
            )
        self.game_menu.add_radiobutton(
            label='Hard',
            variable=self.options['Difficulty'],
            value=1
            )
        self.game_menu.add_radiobutton(
            label='Very Hard',
            variable=self.options['Difficulty'],
            value=2
            )
        self.game_menu.add_separator()
        self.game_menu.add_command(
            label='Hint',
            state='disabled'
            )
        menu_bar.add_cascade(label='Game', menu = self.game_menu)

        self.help_menu = tkinter.Menu(menu_bar, tearoff=0)
        self.help_menu.add_command(
            label='Index',
            accelerator='F1',
            command=self.index_help
            )
        self.help_menu.add_command(
            label='How to Play',
            command=self.how_to_play_help
            )
        self.help_menu.add_command(
            label='Commands',
            command=self.commands_help
            )
        self.help_menu.add_command(
            label='Using Help',
            command=self.using_help
            )
        self.help_menu.add_separator()
        self.help_menu.add_command(
            label='About %s...' % (NAME),
            command=self.about_window
            )
        menu_bar.add_cascade(label='Help', menu=self.help_menu)
        ROOT.config(menu=menu_bar)

        menu_bar.bind_all('<F3>', self.next_iteration)
        menu_bar.bind_all('<F5>', lambda _: self.change_state('Running'))
        menu_bar.bind_all('<F6>', lambda _: self.change_state('Idle'))
        menu_bar.bind_all('<F7>', self.clear_grid)
        menu_bar.bind_all('<F8>', self.randomise_grid)
        menu_bar.bind_all('<F9>', self.options_window)
        menu_bar.bind_all('<F2>', lambda _: self.change_state('Game'))
        menu_bar.bind_all('<F1>', self.index_help)
        menu_bar.bind_all('<Control-q>', lambda _: self.change_state('Idle'))

    def draw_sim(self):
        '''
        Create a grid of labels
        '''
        ROOT.geometry('360x360')
        self.sim_id_list = [[0 for x in range(self.size)]for y in range(self.size)]

        if self.options['Lines']:
            rel = 'raised'
        else:
            rel = 'flat'

        for y in range(self.size):
            for x in range(self.size):
                cell = tkinter.Label(ROOT, bg='#808080', relief=rel, borderwidth=1, padx=0, pady=0)
                cell.grid(row=y, column=x, sticky='n'+'s'+'e'+'w')
                cell.bind('<ButtonPress-1>', self.click_left)
                cell.bind('<ButtonPress-3>', self.click_right)
                cell.bind('<B1-Motion>', self.click_drag_left)
                cell.bind('<B3-Motion>', self.click_drag_right)
                cell.bind('<Double-Button-1>', self.double_click)
                cell.bind('<Double-Button-3>', self.double_click)
                self.sim_id_list[y][x] = cell

        self.update_sim()
        self.root_grid_weight(1)

    def destroy_sim(self):
        '''
        Destroy all the label widgets of the grid
        '''
        for y in range(len(self.sim_id_list)):
            for x in range(len(self.sim_id_list[0])):
                cell = self.sim_id_list[y][x]
                cell.destroy()

        self.root_grid_weight(0)

    def root_grid_weight(self, new_weight):
        '''
        Changes row and column weights in tkinter window ROOT
        '''
        for i in range(self.size):
            tkinter.Misc.columnconfigure(ROOT,i,weight=new_weight)
        for i in range(self.size):
            tkinter.Misc.rowconfigure(ROOT,i,weight=new_weight)

    def update_sim(self):
        '''
        Update the colours of the grid of labels
        '''
        for y in range(len(self.sim_id_list)):
            for x in range(len(self.sim_id_list)):
                if self.sim.data[y][x] == 0:
                    col = '#808080'
                elif self.sim.data[y][x] == 1:
                    col = '#0000FF'
                elif self.sim.data[y][x] == 2:
                    col = '#7F0000'
                cell = self.sim_id_list[y][x]
                cell.configure(bg=col)

    def click_left(self, _=None):
        '''
        Place blue cell or make move if in a game
        '''
        if all([
            ROOT.winfo_pointerx() > ROOT.winfo_rootx(),
            ROOT.winfo_pointerx() < ROOT.winfo_rootx() + ROOT.winfo_width(),
            ROOT.winfo_pointery() > ROOT.winfo_rooty(),
            ROOT.winfo_pointery() < ROOT.winfo_rooty() + ROOT.winfo_height()
            ]):
            x, y = self.get_coordinates()

            if self.state == 'Game':
                self.game_move(x, y)
            else:
                self.change_cell(1, (x, y))

    def click_right(self, _=None):
        '''
        Place red cell
        '''
        if all([
            ROOT.winfo_pointerx() > ROOT.winfo_rootx(),
            ROOT.winfo_pointerx() < ROOT.winfo_rootx() + ROOT.winfo_width(),
            ROOT.winfo_pointery() > ROOT.winfo_rooty(),
            ROOT.winfo_pointery() < ROOT.winfo_rooty() + ROOT.winfo_height(),
            self.state != 'Game'
            ]):
            x, y = self.get_coordinates()
            self.change_cell(2, (x, y))

    def click_drag_left(self, _=None):
        '''
        Place blue cells
        '''
        if self.state != 'Game':
            self.click_left()

    def click_drag_right(self, _=None):
        '''
        Place red cells
        '''
        if self.state != 'Game':
            self.click_right()

    def double_click(self, _=None):
        '''
        If there is no current game, change cell to dead
        '''
        if self.state != 'Game':
            x, y = self.get_coordinates()
            self.change_cell(0, (x, y))

    def change_cell(self, cell_type, coordinates):
        '''
        Change the state of one cell
        '''
        x = coordinates[0]
        y = coordinates[1]

        self.sim.data[y][x] = cell_type

        if cell_type == 0:
            col = '#808080'
        elif cell_type == 1:
            col = '#0000FF'
        elif cell_type == 2:
            col = '#7F0000'
        cell = self.sim_id_list[y][x]
        cell.configure(bg=col)

    def get_coordinates(self):
        '''
        Returns 2 integers
        '''
        mouse_x = ROOT.winfo_pointerx() - ROOT.winfo_rootx()
        mouse_y = ROOT.winfo_pointery() - ROOT.winfo_rooty()
        cell_width = ROOT.winfo_width()/self.size
        cell_height = ROOT.winfo_height()/self.size
        x = math.floor(mouse_x/cell_width)
        y = math.floor(mouse_y/cell_height)

        return x, y

    def next_iteration(self, _=None):
        '''
        Next grid iteration
        '''
        previous_data = self.sim.copy_data()
        self.sim.iterate()
        self.update_sim()
        if self.state == 'Running' and self.sim.data == previous_data:
            self.change_state('Idle')

    def clear_grid(self, _=None):
        '''
        Kill all cells in the grid
        '''
        self.sim.reset_data()
        self.update_sim()

    def randomise_grid(self, _=None):
        '''
        Populate the grid with cells at random
        '''
        self.sim.randomise_data(100)
        self.update_sim()

    def resize_sim(self, size):
        '''
        Change the size of the grid
        '''
        self.size = size
        self.sim.size = self.size
        self.sim.reset_data()

    def generate_hint(self, _=None):
        '''
        AI suggest a move in game
        '''
        pass

    def game_move(self, x, y):
        '''
        A move is made in game
        '''
        if self.game_state == 'Create':
            if self.sim.data[y][x] == 0:
                self.change_cell(1, (x, y))
                self.game_state = 'Destroy'
                ROOT.title('Choose cell to delete')

        elif self.game_state == 'Destroy':
            if self.sim.data[y][x] == 2:
                self.change_cell(0, (x, y))
                self.game_state = 'Iterate'
                ROOT.title('Click to generate')
                self.game_over()

        elif self.game_state == 'Iterate':
            self.next_iteration()
            self.game_state = 'Computer'
            ROOT.title('Click for computer to take turn')
            self.game_over()

        elif self.game_state == 'Computer':
            ai_create, ai_destroy = ai.get_end_node(self)

            self.change_cell(2, ai_create)
            self.change_cell(0, ai_destroy)

            ROOT.title('Choose cell to add')
            if not self.game_over():
                self.next_iteration()
                self.game_state = 'Create'
                self.game_over()

    def game_over(self):
        '''
        Check if game is over and end it if so. Returns True/False
        '''
        blue = 0
        red = 0
        for row in self.sim.data:
            blue += row.count(1)
            red += row.count(2)

        if blue and red:
            return False
        if not blue and red:
            string = 'You Lose.'
        elif blue and not red:
            string = 'Congratulations, you Win!'
        elif not blue and not red:
            string = 'The Game is a Draw..'

        tkinter.messagebox.showinfo('%s -- Game Over' % (NAME), string)
        self.change_state('Idle')
        return True

    def change_state(self, new_state):
        '''
        Change between Idle Simulation, Running Simulation and In Game states
        '''
        if new_state == 'Idle':
            if self.state == 'Game':
                self.destroy_sim()
                self.resize_sim(self.options['Size'])
                self.draw_sim()
                for i in [0, 1, 2, 3, 4, 5, 6, 7, 9]:
                    self.patterns_menu.entryconfig(i, state='normal')
                self.game_menu.entryconfig(1, state='disabled')
                self.game_menu.entryconfig(7, state='disabled')
            elif self.state == 'Running':
                self.life_menu.entryconfig(2, state='disabled')
                self.stop_repeat_flag.set()
            for i in [0, 1, 4, 5, 8]:
                self.life_menu.entryconfig(i, state='normal')
            ROOT.title(NAME)
            self.state = 'Idle'
        elif new_state == 'Running' and self.state != 'Game':
            self.stop_repeat_flag.clear()
            repeat_thread = RepeatIterateThread(self, self.stop_repeat_flag)
            repeat_thread.start()
            ROOT.title('%s -- running' % (NAME))
            self.life_menu.entryconfig(0, state='disabled')
            self.life_menu.entryconfig(1, state='disabled')
            self.life_menu.entryconfig(2, state='normal')
            self.state = 'Running'
        elif new_state == 'Game':
            if self.state == 'Running':
                self.stop_repeat_flag.set()
            self.destroy_sim()
            self.resize_sim(15)
            self.sim.randomise_data(18)
            self.draw_sim()
            self.game_state = 'Create'
            for i in [0, 1, 2, 4, 5, 8]:
                self.life_menu.entryconfig(i, state='disabled')
            for i in [0, 1, 2, 3, 4, 5, 6, 7, 9]:
                self.patterns_menu.entryconfig(i, state='disabled')
            self.game_menu.entryconfig(1, state='normal')
            self.game_menu.entryconfig(7, state='normal')
            ROOT.title('Choose cell to add')
            self.state = 'Game'

    def options_window(self, _=None):
        '''
        Open options window
        '''
        options = tkinter.Toplevel(padx=20, pady=20)
        options.title('%s Options' % (NAME))
        options.grab_set()

        size_frame = tkinter.LabelFrame(options, text='Grid', padx=10, pady=10)
        size_frame.pack(fill='x')
        size_label = tkinter.Label(size_frame, text='Size')
        size_label.pack(side='left')
        size_entry=tkinter.Entry(size_frame, width=7)
        size_entry.insert(0, str(self.size))
        size_entry.pack(side='left')
        show_lines = tkinter.BooleanVar()
        show_lines.set(self.options['Lines'])
        lines_check = tkinter.Checkbutton(size_frame, text='Show Lines', variable=show_lines)
        lines_check.pack(side='right')

        pad_frame = tkinter.Frame(options, pady=20)
        pad_frame.pack()

        speed_frame = tkinter.LabelFrame(pad_frame, text='Speed', padx=10, pady=10)
        speed_frame.pack(fill='x')
        speed_label1 = tkinter.Label(speed_frame, text='Slow')
        speed_label1.pack(side='left')
        speed_scale = tkinter.Scale(speed_frame, orient='horizontal', showvalue=0, length=150)
        speed_scale.set(self.options['Speed'])
        speed_scale.pack(side='left')
        speed_label2 = tkinter.Label(speed_frame, text='Fast')
        speed_label2.pack(side='left')

        button_frame = tkinter.Frame(options, padx=20)
        button_frame.pack(fill='x')

        ok_button = tkinter.Button(
            button_frame,
            text='OK',
            command=lambda: self.save_settings(
                options,
                int(size_entry.get()),
                show_lines.get(),
                speed_scale.get()
                ),
            width=10
            )
        ok_button.pack(side='left')

        cancel_button = tkinter.Button(
            button_frame,
            text='Cancel',
            command=options.destroy,
            width=10
            )
        cancel_button.pack(side='right')

        options.mainloop()

    def save_settings(self, window, size, lines, speed):
        '''
        Apply users changes to options
        '''
        if all([size >= 5, size <= 99]):
            self.destroy_sim()
            window.destroy()
            if size is not self.size:
                self.resize_sim(size)
            self.options['Size'] = size
            self.options['Lines'] = lines
            self.options['Speed'] = speed
            self.draw_sim()
        else:
            tkinter.messagebox.showerror(
                'Grid size out of range',
                'Grid size must be from 5 to 99.'
                )

    def about_window(self, _=None):
        '''
        Open about window
        '''
        about = tkinter.Toplevel(bg='#C0C0C0', padx=10, pady=10)
        about.title('About %s' % (NAME))
        about.grab_set()
        logo = tkinter.PhotoImage(file='../img/logo.png')

        logo_label = tkinter.Label(about, image=logo, relief='sunken')
        logo_label.pack()

        about_label = tkinter.Label(
            about,
            text='This is Jim Horne\'s Life.\n\n A bowl of cherries!',
            bg='#C0C0C0',
            padx=10,
            pady=10
            )
        about_label.pack()

        license_label = tkinter.Label(
            about,
            text='A clone written by Tom Besford under the Apache 2.0 license.',
            bg='#C0C0C0',
            wraplength=256,
            padx=10,
            pady=15
            )
        license_label.pack()

        ok_button=tkinter.Button(about, text='OK', command=about.destroy, width=8)
        ok_button.pack()

        about.mainloop()

    def preset(self, name):
        '''
        Load a pattern preset
        '''
        self.destroy_sim()
        pattern = presets.PRESETS[name]
        self.options['Size'] = len(pattern)
        self.resize_sim(len(pattern))
        self.sim.data = pattern
        self.draw_sim()

    def index_help(self, _=None):
        '''
        Open winhelp file to index
        '''
        pass

    def how_to_play_help(self):
        '''
        Open winhelp file to how to play
        '''
        pass

    def commands_help(self):
        '''
        Open winhelp file to commands
        '''
        pass

    def using_help(self):
        '''
        Open winhelp file to using help
        '''
        pass

class RepeatIterateThread(threading.Thread):
    '''
    Separate thread to repeatedly iterate the grid
    '''
    def __init__(self, master, event):
        threading.Thread.__init__(self)
        self.stopped = event
        self.master = master

    def run(self):
        while not self.stopped.wait((100 - self.master.options['Speed'])/50):
            self.master.next_iteration()

if __name__ == '__main__':
    ROOT = tkinter.Tk()
    ROOT.title(NAME)
    Main()
    ROOT.mainloop()
