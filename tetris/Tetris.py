import pygame, sys, time
from pygame.locals import *
from Board import *
import threading
#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((350, 450))
        self.clock = pygame.time.Clock()
        self.board = Board(self.screen)
        self.music_on_off = True
        self.check_reset = True

    def init(self):
        self.frame_count=0
        self.start_time=90 # origin 90
        self.board.piece_x=3
        self.board.piece_y=0
        
    def handle_key(self, event_key):
        if event_key == K_DOWN or event_key == K_s:
            self.board.drop_piece()
        elif event_key == K_LEFT or event_key == K_a:
            self.board.move_piece(dx=-1, dy=0)
        elif event_key == K_RIGHT or event_key == K_d:
            self.board.move_piece(dx=1, dy=0)
        elif event_key == K_UP or event_key == K_w:
            self.board.rotate_piece()
        elif event_key == K_SPACE:
            self.board.full_drop_piece()
        elif event_key == K_q:
            self.board.ultimate()
        elif event_key == K_m:
            self.music_on_off = not self.music_on_off
            if self.music_on_off:
                pygame.mixer.music.play(-1, 0.0)
            else:
                pygame.mixer.music.stop()
        elif event_key == K_z:
            self.board.use_item()
            
    def HighScore(self):
        try:
            f = open('assets/save.txt', 'r')
            l = f.read()
            f.close()
            if int(l) < self.board.score:
                h_s = self.board.score
                f = open('assets/save.txt', 'w')
                f.write(str(self.board.score))
                f.close()
            else:
                h_s = l
            self.board.HS(str(h_s))
        except:
            f = open('assets/save.txt', 'w')
            f.write(str(self.board.score))
            f.close()
            self.board.HS(str(self.board.score))

    def run(self):
        self.init()
        pygame.init()
        icon = pygame.image.load('assets/images/icon.PNG')
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Tetris')
        pygame.time.set_timer(pygame.USEREVENT, 500)
        start_sound = pygame.mixer.Sound('assets/sounds/Start.wav')
        start_sound.play()
        bgm = pygame.mixer.music.load('assets/sounds/bgm.wav')
        while True:
            if self.check_reset:
                self.board.newGame()
                self.check_reset = False
                pygame.mixer.music.set_volume(0.60) # 볼륩
                pygame.mixer.music.play(-1, 0.0)
            if self.board.game_over():
                self.screen.fill(BLACK)
                pygame.mixer.music.stop()
                self.board.GameOver()
                self.HighScore()
                self.check_reset = True
                self.board.init_board()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYUP and event.key == K_p:
                    self.screen.fill(BLACK)
                    pygame.mixer.music.stop()
                    self.board.pause()
                    pygame.mixer.music.play(-1, 0.0)
                elif event.type == KEYDOWN:
                    self.handle_key(event.key)
                elif event.type == pygame.USEREVENT:
                    self.board.drop_piece()
                elif event.type== K_z:
                    self.board.use_item()
            # self.screen.fill(BLACK)
            self.board.draw()

            # Timer
            total_seconds=self.start_time-(self.frame_count//30)
            if total_seconds<0:
                total_seconds=0

            minutes=total_seconds//60
            seconds=total_seconds%60

            output='{0:02}:{1:02}'.format(minutes,seconds)
            time_value=pygame.font.Font('assets/Roboto-Bold.ttf', 16).render(output, True, BLACK)
            self.screen.blit(time_value,(275,430))
            self.frame_count+=1
            
            if minutes==0 and seconds==0:
                self.board.next_round()
                self.init()

            pygame.display.flip() 
            self.clock.tick(30)

if __name__ == "__main__":
    Tetris().run()