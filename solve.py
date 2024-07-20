import pygame as pg

class Solve:

    def __init__(self, window, X_TILES, Y_TILES, WIDTH, node_color, nodes, draw, clock, FPS):
        self.window = window
        self.X_TILES = X_TILES
        self.Y_TILES = Y_TILES
        self.WIDTH = WIDTH
        self.SQUARE_SIZE = WIDTH // self.X_TILES
        self.node_color = node_color
        self.draw = draw
        self.clock = clock
        self.FPS = FPS

        self.nodes = nodes

        self.neighbors = {}
        self.init_neighbors()

        self.in_shape = {}
        self.init_in_shape()

        self.solve()
    
    def init_in_shape(self):
        for clr in self.node_color:
            for n in self.node_color[clr]:
                cur_neighbors = []
                for n2 in self.node_color[clr]:
                    if n is not n2:
                        cur_neighbors.append(n2)
                self.in_shape[n] = cur_neighbors.copy()
        

    def init_neighbors(self):
        for n in self.nodes:
            cur_neighbors = []
            for n2 in self.nodes:
                if n is not n2 and abs(n.x - n2.x) <= self.SQUARE_SIZE + 1 and abs(n.y - n2.y) <= self.SQUARE_SIZE + 1:
                    cur_neighbors.append(n2)
            self.neighbors[n] = cur_neighbors.copy()
    
    def is_valid(self, n, num):
        for neighbor in self.neighbors[n]:
            if neighbor.val == num:
                return False
        
        for inside in self.in_shape[n]:
            if inside.val == num:
                return False
        
        return True

    def solve(self):

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
        
        self.draw.call_all()
        self.clock.tick(self.FPS)
        pg.display.update()

        for n in self.nodes:
            if not n.val:
                for num in range(1, len(self.in_shape[n]) + 2):
                    if self.is_valid(n, num):
                        n.val = num
                        self.solve()
                        n.val = None
                return None
        
        self.show()

       
    
    def show(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
            
            self.draw.call_all()

            self.clock.tick(self.FPS)
            pg.display.update()


