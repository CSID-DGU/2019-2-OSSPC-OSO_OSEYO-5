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
        '''try:
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
            self.board.HS(str(self.board.score))'''
        # pickle
        # unpickle
        high_scores = []
        with open('highscores.txt', 'rb') as f:
            high_scores = pickle.load(f)
        
        high_scores.append((str(input_id), self.board.score))
        high_scores = sorted(high_scores, key=itemgetter(1), reverse=True)[:10]
        with open('highscores.txt', 'wb') as f:
            pickle.dump(high_scores, f)

        self.board.HS(high_scores)

    def run(self, input_id):
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
                pygame.mixer.music.set_volume(0.70)
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
            self.board.draw(input_id)
            pygame.display.update()
            self.clock.tick(30)
#여기부터 홈 메뉴 부분 가져온거
import sys

sys.path.insert(0, '../../')

import os
import pygame
FPS = 60.0
import pygameMenu

# -----------------------------------------------------------------------------
# Constants and global variables
# -----------------------------------------------------------------------------
ABOUT = ['pygameMenu {0}'.format(pygameMenu.__version__),
         'Author: @{0}'.format(pygameMenu.__author__),
         pygameMenu.locals.TEXT_NEWLINE,
         'Email: {0}'.format(pygameMenu.__email__)]

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
MENU_BACKGROUND_COLOR = (169, 169, 169) #메뉴 배경 색상 #회색 ##j
MENU_TITLE_BG_COLOR = (169,169,169) #제목 배경 색상 ##j
WINDOW_SIZE = (350, 400) ##초기 메뉴 사이즈

sound = None
surface = None
main_menu = None


# -----------------------------------------------------------------------------
# Methods
# -----------------------------------------------------------------------------
def main_background(): #surface를 선언하고 fill

    global surface
    surface.fill((0, 0, 0)) ##게임창 외 부분 검은색


def check_name_test(value):

    print('User name: {0}'.format(value))# 프린트 {0}{2}{1}.format(a,b,c) 하면 a,c,b순으로 출력됨


# noinspection PyUnusedLocal
def update_menu_sound(value, enabled):

    global main_menu
    global sound
    if enabled:
        main_menu.set_sound(sound, recursive=True)
        print('Menu sound were enabled')
    else:
        main_menu.set_sound(None, recursive=True)
        print('Menu sound were disabled')


def main(test=False):
    """
    Main program.

    :param test: Indicate function is being tested
    :type test: bool
    :return: None
    """

    # -------------------------------------------------------------------------
    # Globals
    # -------------------------------------------------------------------------
    global main_menu
    global sound
    global surface

    # -------------------------------------------------------------------------
    # Init pygame
    # -------------------------------------------------------------------------
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Create pygame screen and objects
    surface = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Multi Input')
    clock = pygame.time.Clock()

    # -------------------------------------------------------------------------
    # Set sounds
    # -------------------------------------------------------------------------
    sound = pygameMenu.sound.Sound()

    # Load example sounds
    sound.load_example_sounds()

    # Disable a sound
    sound.set_sound(pygameMenu.sound.SOUND_TYPE_ERROR, None)

    # -------------------------------------------------------------------------
    # Create menus
    # -------------------------------------------------------------------------

    # signup_menu
    signup_menu = pygameMenu.Menu(surface,
                                    bgfun=main_background,
                                    color_selected=COLOR_WHITE,
                                    font=pygameMenu.font.FONT_BEBAS,
                                    font_color=COLOR_BLACK,
                                    font_size=25,
                                    font_size_title=50,
                                    menu_alpha=100,
                                    menu_color=MENU_BACKGROUND_COLOR,
                                    ##j
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
                                        onreturn=check_name_test,
                                        textinput_id='ID')
    signup_menu.add_text_input('PASSWORD: ',
                                        password=True,
                                        maxchar=8,
                                        textinput_id='PASSWORD')

    def data_func():
        """
        Print data of the menu.

        :return: None
        """
        print('signup data:')
        f=open("account.txt","a")
        data = signup_menu.get_input_data()
        if (data['ID'].strip()).upper() in open("account.txt").read():
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
                                  font=pygameMenu.font.FONT_BEBAS,
                                  font_color=COLOR_BLACK,
                                  menu_color_title=MENU_TITLE_BG_COLOR,
                                  font_size=20,
                                  font_size_title=40,
                                  menu_alpha=100,
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
                                      onreturn=check_name_test,
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
        f = open("account.txt", "r")  # 가입한 계정이 저장되는 위치
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


    # rank_menu ##j
    ranks  = []
    with open('highscores.txt', 'rb') as f:
        r = pickle.load(f)
        r.sort(key=itemgetter(1, 0), reverse=True)
        for i in range(0,len(r)):
            ranks.append(str(r[i]))



    rank_menu = pygameMenu.TextMenu(surface,
                                    bgfun=main_background,
                                    color_selected=COLOR_WHITE,
                                    menu_color_title=MENU_TITLE_BG_COLOR,
                                    font=pygameMenu.font.FONT_BEBAS,
                                    font_color=COLOR_BLACK,
                                    font_size_title=40,
                                    menu_alpha=100,
                                    menu_color=MENU_BACKGROUND_COLOR,
                                    menu_height=int(WINDOW_SIZE[1] * 0.85),
                                    menu_width=int(WINDOW_SIZE[0] * 0.9),
                                    onclose=pygameMenu.events.EXIT,  # User press ESC button
                                    option_shadow=False,
                                    title='RANK',
                                    text_color=COLOR_BLACK,
                                    text_align=pygameMenu.locals.ALIGN_CENTER,
                                    text_fontsize=10,
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
                                font=pygameMenu.font.FONT_BEBAS,
                                font_color=COLOR_BLACK,
                                font_size_title=40,
                                menu_alpha=100,
                                menu_color=MENU_BACKGROUND_COLOR,
                                menu_height=int(WINDOW_SIZE[1] * 0.85),
                                menu_width=int(WINDOW_SIZE[0] * 0.9),
                                onclose=pygameMenu.events.EXIT, # User press ESC button
                                option_shadow=False,
                                title='HELP',
                                text_color=COLOR_BLACK,
                                text_align=pygameMenu.locals.ALIGN_CENTER,
                                text_fontsize=10,
                                window_height=WINDOW_SIZE[1],
                                window_width=WINDOW_SIZE[0]
                                   )
    for line in helps:
                  help_menu.add_line(line)  # Add line
    help_menu.add_option('Return to Menu', pygameMenu.events.BACK,align=pygameMenu.locals.ALIGN_CENTER)


    # Main menu
    main_menu = pygameMenu.Menu(surface,
                                bgfun=main_background,
                                color_selected=COLOR_WHITE,
                                font=pygameMenu.font.FONT_COMIC_NEUE,
                                font_color=COLOR_BLACK,
                                font_size=20,
                                font_size_title=40,
                                menu_alpha=100,
                                menu_color=MENU_BACKGROUND_COLOR,
                                menu_height=int(WINDOW_SIZE[1] * 0.7),
                                menu_width=int(WINDOW_SIZE[0] * 0.8),
                                # User press ESC button
                                onclose=pygameMenu.events.EXIT,
                                option_shadow=False,
                                title='Main menu',
                                window_height=WINDOW_SIZE[1],
                                window_width=WINDOW_SIZE[0]
                                )
    main_menu.set_fps(FPS)

    main_menu.add_option('SIGN_UP', signup_menu)
    main_menu.add_option('SIGN_IN', signin_menu)
    main_menu.add_option('RANK', rank_menu)
    main_menu.add_option('HELP', help_menu)
    main_menu.add_selector('Menu sounds',
                           [('Off', False), ('On', True)],
                           onchange=update_menu_sound)
    main_menu.add_option('Quit', pygameMenu.events.EXIT)

    assert main_menu.get_widget('ID', recursive=True) is wid1


    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
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


