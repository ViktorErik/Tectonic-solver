import pygame as pg
from node import Node
import random
from random import randint
pg.font.init()

class Draw:
    def __init__(self, window, X_TILES, Y_TILES, WIDTH, HEIGHT, DRAW_SCREEN_HEIGHT):
        self.window = window
        self.X_TILES = X_TILES
        self.Y_TILES = Y_TILES
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        """
        self.COLORS = {"red": (255, 0, 0), "green": (0, 255, 0), "blue": (0, 0, 255),
                       "orange": (230, 130, 0), "white": (255, 255, 255), "lightblue": (70, 150, 255), 
                       "yellow": (255, 200, 50), "purple": (70, 20, 200)}
        """
        self.COLORS = [(randint(0, 255), randint(0, 255), randint(0, 255)) for _ in range(100)]


        self.node_color = {clr: [] for clr in self.COLORS}
        self.nodes = []

        self.TEXT_COLOR = (0, 0, 0)

        self.BTN_SCREEN_CLR = (50, 50, 50)
        self.BTN_CLR = (255, 255, 255)
        self.BTN_WIDTH = 150
        self.BTN_HEIGHT = 30
        self.DRAW_SCREEN_HEIGHT = DRAW_SCREEN_HEIGHT

        self.DRAW_BTN_X = (self.WIDTH // 2 - self.BTN_WIDTH - 10)
        self.DRAW_BTN_Y = (self.HEIGHT - self.DRAW_SCREEN_HEIGHT // 2 - self.BTN_HEIGHT // 2)

        self.WRITE_BTN_X = (self.WIDTH // 2 + 10)
        self.WRITE_BTN_Y = (self.HEIGHT - self.DRAW_SCREEN_HEIGHT // 2 - self.BTN_HEIGHT // 2)

        self.SQUARE_SIZE = self.WIDTH / self.X_TILES

        self.font = pg.font.Font("freesansbold.ttf", 16)
        self.new_shape_text = self.font.render("Ny färg", True, (self.TEXT_COLOR))
        self.write_text = self.font.render("Skriv tal", True, (self.TEXT_COLOR))
        self.square_text = self.font.render("", True, (self.TEXT_COLOR))

        self.write_mode = False
        
        self.cur_color = self.COLORS[0]

        self.drawn_squares = []
        self.used_colors = set()

        self.selected = None
    
    def delete_square(self):
        x, y = self.drawn_squares[-1]
        for clr in self.node_color:
            if self.node_color[clr]:

                if (x, y) == (self.node_color[clr][-1].x, self.node_color[clr][-1].y):
                    self.node_color[clr].pop()

        self.nodes.pop()
        self.drawn_squares.pop()

    
    def call_all(self):
        self.window.fill((0, 0, 0))
        self.draw_square()
        self.write()
        self.change_btn_mode()
        self.draw_button_screen()
        self.get_color()

    def get_color(self):
        
        cursor_x = pg.mouse.get_pos()[0]
        cursor_y = pg.mouse.get_pos()[1]

        square_pos_x = int(cursor_x // self.SQUARE_SIZE * self.SQUARE_SIZE) 
        square_pos_y = int(cursor_y // self.SQUARE_SIZE * self.SQUARE_SIZE) 

        if (square_pos_x, square_pos_y) in self.drawn_squares and pg.mouse.get_pressed()[0]:
            self.cur_color = self.window.get_at((square_pos_x, square_pos_y))[:-1]

    def draw_square(self):

        if pg.mouse.get_pressed()[0] and not self.write_mode:
            cursor_x = pg.mouse.get_pos()[0]
            cursor_y = pg.mouse.get_pos()[1]

            

            if (0 < cursor_x < self.WIDTH) and (0 < cursor_y < self.HEIGHT - self.DRAW_SCREEN_HEIGHT): 

                square_pos_x = int(cursor_x // self.SQUARE_SIZE * self.SQUARE_SIZE) 
                square_pos_y = int(cursor_y // self.SQUARE_SIZE * self.SQUARE_SIZE)

                if (square_pos_x, square_pos_y) not in self.drawn_squares:
                    new_node = Node(square_pos_x, square_pos_y)
                    self.drawn_squares.append((square_pos_x, square_pos_y))
                    self.node_color[self.cur_color].append(new_node)
                    self.used_colors.add(self.cur_color)
                    self.nodes.append(new_node)



        for clr in self.node_color.keys():
            for n in self.node_color[clr]:
                pg.draw.rect(self.window, clr, (n.x, n.y, self.SQUARE_SIZE, self.SQUARE_SIZE))
    
    def draw_button_screen(self):
        # Rita skärm bakom knappar
        pg.draw.rect(self.window, self.BTN_SCREEN_CLR, (0, self.HEIGHT - self.DRAW_SCREEN_HEIGHT, self.WIDTH, self.DRAW_SCREEN_HEIGHT))

        # Rita draw-knappen och write-knappen
        pg.draw.rect(self.window, self.BTN_CLR, (self.DRAW_BTN_X, self.DRAW_BTN_Y, self.BTN_WIDTH, self.BTN_HEIGHT))
        pg.draw.rect(self.window, self.BTN_CLR, (self.WRITE_BTN_X, self.WRITE_BTN_Y, self.BTN_WIDTH, self.BTN_HEIGHT))

        # Text till draw-knappen
        self.window.blit(self.new_shape_text, (
            self.DRAW_BTN_X + self.BTN_WIDTH // 2 - self.new_shape_text.get_width() // 2, 
            self.DRAW_BTN_Y + self.BTN_HEIGHT // 2 - self.new_shape_text.get_height() // 2))

        # Text till write-knappen
        self.window.blit(self.write_text, (
            self.WRITE_BTN_X + self.BTN_WIDTH // 2 - self.write_text.get_width() // 2,
            self.WRITE_BTN_Y + self.BTN_HEIGHT // 2 - self.write_text.get_height() // 2
        ))
    
    def change_btn_mode(self):
        cursor_x = pg.mouse.get_pos()[0]
        cursor_y = pg.mouse.get_pos()[1]
        
        if pg.mouse.get_pressed()[0]: 
            # Ändra till draw-mode/ändra färg
            if (self.DRAW_BTN_X < cursor_x < self.DRAW_BTN_X + self.BTN_WIDTH and
                self.DRAW_BTN_Y < cursor_y < self.DRAW_BTN_Y + self.BTN_HEIGHT):
                
                self.write_mode = False

                if len(self.used_colors) >= len(self.COLORS):
                    pg.quit()
                    return

                while self.cur_color in self.used_colors:
                    self.cur_color = random.choice(self.COLORS)
            
            # Ändra till write-mode
            elif (self.WRITE_BTN_X < cursor_x < self.WRITE_BTN_X + self.BTN_WIDTH and
                  self.WRITE_BTN_Y < cursor_y < self.WRITE_BTN_Y + self.BTN_HEIGHT):
                self.write_mode = True
        
    def write(self):

        cursor_x = pg.mouse.get_pos()[0]
        cursor_y = pg.mouse.get_pos()[1]
        if self.write_mode:
            if 0 < cursor_x < self.WIDTH and 0 < cursor_y < self.HEIGHT - self.DRAW_SCREEN_HEIGHT and pg.mouse.get_pressed()[0]:

                square_pos_x = int(cursor_x // self.SQUARE_SIZE * self.SQUARE_SIZE)
                square_pos_y = int(cursor_y // self.SQUARE_SIZE * self.SQUARE_SIZE)

                for n in self.nodes:
                    if square_pos_x == n.x and square_pos_y == n.y:
                        self.selected = n


        keys_pressed = list(pg.key.get_pressed())
        for i in range(30, 40):
            if keys_pressed[i]:
                self.selected.val = i - 29
        
        for n in self.nodes:
            if n.val == 10: 
                n.val = None
            str_val = str(n.val) if n.val != None else ""
            self.square_text = self.font.render(str_val, True, self.TEXT_COLOR)
            self.window.blit(self.square_text, (n.x - self.square_text.get_width() // 2 + self.SQUARE_SIZE // 2, 
                                                n.y - self.square_text.get_height() // 2 + self.SQUARE_SIZE // 2))

