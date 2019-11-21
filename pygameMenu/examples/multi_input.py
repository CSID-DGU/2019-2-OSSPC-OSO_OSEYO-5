# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - MULTI-INPUT
Shows different inputs (widgets).

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2019 Pablo Pizarro R. @ppizarror

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
-------------------------------------------------------------------------------
"""

# Import libraries
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
MENU_BACKGROUND_COLOR = (169, 169, 169) #연보라로 바꿈
WINDOW_SIZE = (640, 480)

sound = None
surface = None
main_menu = None


# -----------------------------------------------------------------------------
# Methods
# -----------------------------------------------------------------------------
def main_background(): #surface를 선언하고 fill
    """
    Background color of the main menu, on this function user can plot
    images, play sounds, etc.

    :return: None
    """
    global surface
    surface.fill((150, 150, 150)) #게임창 외 부분 색깔 채우기


def check_name_test(value):
    """
    This function tests the text input widget.

    :param value: The widget value
    :type value: basestring
    :return: None
    """
    print('User name: {0}'.format(value))# 프린트 {0}{2}{1}.format(a,b,c) 하면 a,c,b순으로 출력됨


# noinspection PyUnusedLocal
def update_menu_sound(value, enabled):
    """
    Update menu sound.

    :param value: Value of the selector (Label and index)
    :type value: tuple
    :param enabled: Parameter of the selector, (True/False)
    :type enabled: bool
    :return: Nonelkd

    """
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
    pygame.display.set_caption('Example - Multi Input')
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
                                        onreturn=check_name_test,
                                        textinput_id='ID')
    signup_menu.add_text_input('PASSWORD: ',
                                        default=' ',
                                        maxchar=8,
                                        textinput_id='PASSWORD',
                                        input_underline='_')

    def data_func():
        """
        Print data of the menu.

        :return: None
        """
        print('signup data:')
        data = signup_menu.get_input_data()
        new_user_id = data['ID']
        new_user_pw = data['PASSWORD']
        new_user_sc = "0" #score 점수 0으로 초기화
        f = open("D:\Open\pygame-menu-master\pygameMenu\examples/account.txt", "a") #가입한 계정이 저장되는 위치
        f.write(new_user_id + " " + new_user_pw + " " + new_user_sc + "\n")
        f.close()

    signup_menu.add_option('Store data', data_func)  # Call function
    signup_menu.add_option('Return to main menu', pygameMenu.events.BACK,
                             align=pygameMenu.locals.ALIGN_CENTER)


    #signin_menu
    signin_menu = pygameMenu.Menu(surface,
                                  bgfun=main_background,
                                  color_selected=COLOR_WHITE,
                                  font=pygameMenu.font.FONT_BEBAS,
                                  font_color=COLOR_BLACK,
                                  font_size=25,
                                  font_size_title=50,
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
                               default=' ',
                               maxchar=8,
                               textinput_id='PASSWORD',
                               input_underline='_')

    def data2_func():

        print('sign in data : ')
        data = signin_menu.get_input_data() # UI상에 입력된 정보 받아서 data에 저장
        input_id = data['ID']
        input_pw = data['PASSWORD']
        f = open("D:\Open\pygame-menu-master\pygameMenu\examples/account.txt", "r")  # 가입한 계정이 저장되는 위치
        r = f.read()
        l = r.split()
        print(l)
        print(len(l))

        for i in l:  # 아이디 인덱스와 로그아웃 상태 확인
            id_idx = 0
            login_con = 0

            while id_idx < len(l):  # 아이디 인덱스가 리스트 길이보다 짧으면
                if input_id != l[id_idx]:  # 리스트 아이디와 아이디인덱스 value 비교
                    id_idx += 3
                    print(id_idx)
                    print(l[id_idx])

                elif input_id == l[id_idx]:  # 아이디 있으면 비밀번호 입력
                    print(l[1])
                    while login_con == 0:
                        if input_pw == l[id_idx + 1]:
                            print("로그인 성공")
                            login_con = 1
                        else:
                             print("비밀번호가 틀렸습니다")
        f.close()
    signin_menu.add_option('Login', data2_func)  # Call function
    signin_menu.add_option('Return to main menu', pygameMenu.events.BACK, align=pygameMenu.locals.ALIGN_CENTER)

    # Main menu
    main_menu = pygameMenu.Menu(surface,
                                bgfun=main_background,
                                color_selected=COLOR_WHITE,
                                font=pygameMenu.font.FONT_COMIC_NEUE,
                                font_color=COLOR_BLACK,
                                font_size=30,
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
    main_menu.add_option('RANK', signup_menu)
    main_menu.add_option('HELP', signup_menu)
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

