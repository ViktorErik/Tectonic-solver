from draw import Draw
import pygame as pg
from solve import Solve


class Main:
    
    def __init__(self):

        self.WIDTH, self.HEIGHT = 420, 420
        self.BG_COLOR = (0, 0, 0)
        self.X_TILES = 5
        self.Y_TILES = 5
        self.DRAW_SCREEN_HEIGHT = 80
        
        self.HEIGHT *= (self.Y_TILES / self.X_TILES)
        self.HEIGHT += self.DRAW_SCREEN_HEIGHT
        self.window = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.display.set_caption("Tectonic fusk")

        self.draw = Draw(self.window, self.X_TILES, self.Y_TILES, self.WIDTH, self.HEIGHT, self.DRAW_SCREEN_HEIGHT)

        self.FPS = 200
        self.clock = pg.time.Clock()
        self.main()

    def main(self):


        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        self.draw.delete_square()

            self.window.fill((self.BG_COLOR))

            self.draw.call_all()

            if (len(self.draw.drawn_squares) >= self.X_TILES * self.Y_TILES and 
                pg.key.get_pressed()[pg.K_SPACE]):
                self.solve()
                return


                

            self.clock.tick(self.FPS)
            pg.display.update()
    
    def solve(self): 
        Solve(self.window, self.X_TILES, self.Y_TILES, self.WIDTH, self.draw.node_color, self.draw.nodes, self.draw, self.clock, self.FPS)
        
if __name__ == "__main__":
    Main()
