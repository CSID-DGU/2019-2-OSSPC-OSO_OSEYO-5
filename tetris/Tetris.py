import pygame, sys, time
from pygame.locals import *
from Board import *
import threading
from operator import itemgetter
import pickle

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
        self.start_time=60 # origin 90
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
           
    def HighScore(self,input_id):
        high_scores = []
        with open('assets/highscores.txt', 'rb') as f:
            high_scores = pickle.load(f)
        
        high_scores.append((str(input_id), self.board.score))
        high_scores = sorted(high_scores, key=itemgetter(1), reverse=True)[:10]
        with open('assets/highscores.txt', 'wb') as f:
            pickle.dump(high_scores, f)

        self.board.HS(high_scores)

    def run(self, input_id):
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
                pygame.mixer.music.set_volume(0.50)
                pygame.mixer.music.play(-1, 0.0)
            if self.board.game_over():
                self.screen.fill(BLACK)
                pygame.mixer.music.stop()
                self.board.GameOver()
                self.HighScore(input_id)
                self.check_reset = True
                self.board.init_board()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYUP and event.key == K_ESCAPE:
                    main()
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

            self.board.draw(input_id)

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
                if self.board.round!=10:
                    self.board.next_round()
                    self.init()
                else:
                    self.screen.fill(BLACK)
                    pygame.mixer.music.stop()                    
                    self.board.all_clear()
                    self.HighScore(input_id)
                    self.check_reset = True
                    self.board.init_board()
            
            pygame.display.update() 
            self.clock.tick(30)

############# menu #############
import sys
import os
import pygame
import pygameMenu

sys.path.insert(0, '../../')
FPS = 60.0

ABOUT = ['pygameMenu {0}'.format(pygameMenu.__version__),
         'Author: @{0}'.format(pygameMenu.__author__),
         pygameMenu.locals.TEXT_NEWLINE,
         'Email: {0}'.format(pygameMenu.__email__)]

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
MENU_BACKGROUND_COLOR = (169, 169, 169)
MENU_TITLE_BG_COLOR = (169,169,169)
WINDOW_SIZE = (350, 450)

surface = None
main_menu = None

home_bg = pygame.transform.scale(pygame.image.load("assets/images/home_bg.png"),(350,450))
help_bg = pygame.transform.scale(pygame.image.load("assets/images/squid.png"),(300,300))
def main_background(): #surface를 선언하고 fill
    #global surface
    surface.fill((0, 0, 0)) ##게임창 외 부분 검은색
    surface.blit(home_bg, (0,0))

'''def main_background():
    global surface
    surface.fill((0, 0, 0))'''

def main(test=False):
    pygame.init()
    pygame.mixer.music.stop()

    global main_menu
    global surface

    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Create pygame screen and objects
    surface = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('TETRIS')
    clock = pygame.time.Clock()

    # signup_menu
    signup_menu = pygameMenu.Menu(surface,
                                    bgfun=main_background,
                                    color_selected=COLOR_WHITE,
                                    font='assets/Roboto-Bold.ttf',
                                    font_color=COLOR_BLACK,
                                    font_size=20,
                                    font_size_title=50,
                                    menu_alpha=50,
                                    menu_color=MENU_BACKGROUND_COLOR,
                                    menu_color_title=MENU_TITLE_BG_COLOR,
                                    menu_height=int(WINDOW_SIZE[1] * 0.85),
                                    menu_width=int(WINDOW_SIZE[0] * 0.9),
                                    onclose=pygameMenu.events.DISABLE_CLOSE,
                                    title='SIGN_UP',
                                    widget_alignment=pygameMenu.locals.ALIGN_LEFT,
                                    window_height=WINDOW_SIZE[1],
                                    window_width=WINDOW_SIZE[0]
                                    )

    # Add text inputs with different configurations
    wid1 = signup_menu.add_text_input('ID: ',
                                        default=' ',
                                        maxchar=8,
                                        textinput_id='ID')
    signup_menu.add_text_input('PASSWORD: ',
                                        password=True,
                                        maxchar=8,
                                        textinput_id='PASSWORD')

    def data_func():
        print('signup data:')
        f=open("assets/account.txt","a")
        data = signup_menu.get_input_data()
        if (data['ID'].strip()).upper() in open("assets/account.txt").read():
            print("중복되는 아이디가 있습니다.")
        elif (len(data['ID'].strip().split())>1):
            print("띄어쓰기는 허용되지 않습니다.")
        else:
            new_user_id = (data['ID'].strip()).upper()
            new_user_pw = (data['PASSWORD'].strip()).upper()
            new_user_sc = "0" #score 점수 0으로 초기화
            f.write(new_user_id + " " + new_user_pw + " " + new_user_sc + "\n")
        f.close()

    signup_menu.add_option('Store data', data_func)  # Call function
    signup_menu.add_option('Return to main menu', pygameMenu.events.BACK,align=pygameMenu.locals.ALIGN_CENTER)

    #signin_menu
    signin_menu = pygameMenu.Menu(surface,
                                bgfun=main_background,
                                color_selected=COLOR_WHITE,
                                font='assets/Roboto-Bold.ttf',                                  
                                font_color=COLOR_BLACK,
                                menu_color_title=MENU_TITLE_BG_COLOR,
                                font_size=20,
                                font_size_title=40,
                                menu_alpha=50,
                                menu_color=MENU_BACKGROUND_COLOR,
                                menu_height=int(WINDOW_SIZE[1] * 0.85),
                                menu_width=int(WINDOW_SIZE[0] * 0.9),
                                onclose=pygameMenu.events.DISABLE_CLOSE,
                                title='SIGN_IN',
                                widget_alignment=pygameMenu.locals.ALIGN_LEFT,
                                window_height=WINDOW_SIZE[1],
                                window_width=WINDOW_SIZE[0]
                                  )

    # Add text inputs with different configurations
    signin_menu.add_text_input('ID: ',
                                      default=' ',
                                      textinput_id='ID')
    signin_menu.add_text_input('PASSWORD: ',
                               password=True,
                               maxchar=8,
                               textinput_id='PASSWORD',
                               input_underline='_')

    def data2_func():
        data = signin_menu.get_input_data()  # UI상에 입력된 정보 받아서 data에 저장
        input_id = (data['ID'].strip()).upper()
        input_pw = (data['PASSWORD'].strip()).upper()
        f = open("assets/account.txt", "r")  # 가입한 계정이 저장되는 위치
        r = f.read()
        l = r.split()
        f.close()
        id_idx=0; login_con=0
        for id_idx in range(len(l)):  # 아이디 인덱스가 리스트 길이보다 짧으면
            if input_id != l[id_idx]:  # 리스트 아이디와 아이디인덱스 value 비교
                id_idx += 3
            elif input_id == l[id_idx]:  # 아이디 있으면 비밀번호 입력
               if login_con == 0:
                    if input_pw == l[id_idx+1]:
                       login_con = 1
                       print("signed in")
                       Tetris().run(input_id)
                       break
                    else:
                        print("비밀번호가 틀렸습니다")
                        signin_menu.full_reset() ## 아직 안돼서 그냥 이전 메뉴로 돌아가게
                        break

    signin_menu.add_option('Login', data2_func)  # Call function
    signin_menu.add_option('Return to main menu', pygameMenu.events.BACK, align=pygameMenu.locals.ALIGN_CENTER)

    ##j 로그인 에러 메시지
    # sound = pygameMenu.sound.Sound()
    # wrongpw_menu = pygameMenu.Menu(surface,
    #                               bgfun=main_background,
    #                               title="wrong ID or PASSWORD",
    #                               fps=FPS,
    #                               color_selected=COLOR_WHITE,
    #                               font=pygameMenu.font.FONT_BEBAS,
    #                               font_color=COLOR_BLACK,
    #                               menu_color_title=MENU_TITLE_BG_COLOR,
    #                               font_size=20,
    #                               font_size_title=40,
    #                               menu_alpha=100,
    #                               menu_color=MENU_BACKGROUND_COLOR,
    #                               menu_height=int(WINDOW_SIZE[1] * 0.85),
    #                               menu_width=int(WINDOW_SIZE[0] * 0.9),
    #                               onclose=pygameMenu.events.DISABLE_CLOSE,
    #                               window_height=WINDOW_SIZE[1],
    #                               window_width=WINDOW_SIZE[0]
    #                              )
    # wrongpw_menu.set_sound(sound, True)

    # rank_menu
    ranks  = []
    with open('assets/highscores.txt', 'rb') as f:
        r = pickle.load(f)
        r.sort(key=itemgetter(1, 0), reverse=True)
        for i in range(0,len(r)):
            ranks.append(str(r[i]))

    rank_menu = pygameMenu.TextMenu(surface,
                                    bgfun=main_background,
                                    color_selected=COLOR_WHITE,
                                    menu_color_title=MENU_TITLE_BG_COLOR,
                                    font='assets/Roboto-Bold.ttf',
                                    font_color=COLOR_BLACK,
                                    font_size=20,
                                    font_size_title=40,
                                    menu_alpha=50,
                                    menu_color=MENU_BACKGROUND_COLOR,
                                    menu_height=int(WINDOW_SIZE[1] * 0.9),
                                    menu_width=int(WINDOW_SIZE[0] * 0.9),
                                    option_shadow=False,
                                    title='RANK', # top10
                                    text_color=COLOR_BLACK,
                                    text_align=pygameMenu.locals.ALIGN_CENTER,
                                    text_fontsize=14,
                                    window_height=WINDOW_SIZE[1],
                                    window_width=WINDOW_SIZE[0]
                                    )
    for line in ranks:
        rank_menu.add_line(line)  # Add line
    rank_menu.add_option('Return to Menu', pygameMenu.events.BACK, align=pygameMenu.locals.ALIGN_CENTER)
    f.close()

    # help_menu ##j
    helps = ['HELP :',
             '\n',
            'Press ESC to enable/disable Menu',
            'Press ENTER to access a Sub-Menu or use an option',
            'Press UP/DOWN to move through Menu',
            'Press LEFT/RIGHT to move through Selectors']

    help_menu = pygameMenu.TextMenu(surface,
                                    bgfun=main_background,
                                    color_selected=COLOR_WHITE,
                                    menu_color_title=MENU_TITLE_BG_COLOR,
                                    font='assets/Roboto-Bold.ttf',
                                    font_color=COLOR_BLACK,
                                    font_size=20,
                                    font_size_title=40,
                                    menu_alpha=50,
                                    menu_color=MENU_BACKGROUND_COLOR,
                                    menu_height=int(WINDOW_SIZE[1] * 0.9),
                                    menu_width=int(WINDOW_SIZE[0] * 0.9),
                                    option_shadow=False,
                                    title='HELP',
                                    text_color=COLOR_BLACK,
                                    text_align=pygameMenu.locals.ALIGN_CENTER,
                                    text_fontsize=14,
                                    window_height=WINDOW_SIZE[1],
                                    window_width=WINDOW_SIZE[0]
                                    )
    for line in helps:
        help_menu.add_line(line)  # Add line
    help_menu.add_option('Return to Menu', pygameMenu.events.BACK, align=pygameMenu.locals.ALIGN_CENTER)

    # Main menu
    main_menu = pygameMenu.Menu(surface,
                                bgfun=main_background,
                                color_selected=COLOR_WHITE,
                                font='assets/Roboto-Bold.ttf',
                                font_color=COLOR_BLACK,
                                font_size=20,
                                font_size_title=40,
                                menu_alpha=0,
                                menu_color=MENU_BACKGROUND_COLOR,
                                menu_height=int(WINDOW_SIZE[1] * 0.7),
                                menu_width=int(WINDOW_SIZE[0] * 0.8),
                                option_shadow=False,
                                title='TETRIS', #'Main menu',
                                window_height=WINDOW_SIZE[1],
                                window_width=WINDOW_SIZE[0]
                                )
    main_menu.set_fps(FPS)

    main_menu.add_option('SIGN_UP', signup_menu)
    main_menu.add_option('SIGN_IN', signin_menu)
    main_menu.add_option('RANK', rank_menu)
    main_menu.add_option('HELP', help_menu)
    main_menu.add_option('Quit', pygameMenu.events.EXIT)

    assert main_menu.get_widget('ID', recursive=True) is wid1

    # Main loop
    while True:
        # Tick
        clock.tick(FPS)

        # Paint background
        main_background()

        # Main menu
        main_menu.mainloop(disable_loop=test)

        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test:
            break

if __name__ == '__main__':
    main()