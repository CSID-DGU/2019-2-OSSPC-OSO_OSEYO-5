import pygame, sys, datetime, time
from pygame.locals import *
from Piece import *
import random
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

# 이미지 불러오기, 아이템 리스트, 인벤토리 전역변수 선언
item_list, inven=[],[] ## item_block 리스트 삭제
snail=pygame.transform.scale(pygame.image.load("assets/images/snail.png"),(25,25))
quick=pygame.transform.scale(pygame.image.load("assets/images/quick.png"),(25,25))
change=pygame.transform.scale(pygame.image.load("assets/images/change.png"),(25,25))
squid=pygame.transform.scale(pygame.image.load("assets/images/squid.png"),(25,25))
updown=pygame.transform.scale(pygame.image.load("assets/images/updown.png"),(25,25))
delete=pygame.transform.scale(pygame.image.load("assets/images/delete.png"),(25,25))
question = pygame.transform.scale(pygame.image.load("assets/images/question.png"),(24,24))
squid_ink=pygame.transform.scale(pygame.image.load("assets/images/real-ink.png"),(250,250)) # 정사각형, 이미지 수정 필요

item_list.append(snail)
item_list.append(quick)
item_list.append(change)
item_list.append(squid)

class Board:
    COLLIDE_ERROR = {'no_error' : 0, 'right_wall':1, 'left_wall':2,
                     'bottom':3, 'overlap':4}

    def __init__(self, screen):
        self.screen = screen
        self.width = 10
        self.height = 20
        self.block_size = 25
        self.init_board()
        self.generate_piece()

    def init_board(self):
        self.board = []
        self.score = 0
        self.level = 1
        self.goal = 5
        self.skill = 0
        for _ in range(self.height):
            self.board.append([0]*self.width)
                                   
    def generate_piece(self):
        self.piece = Piece()
        self.next_piece = Piece()
        self.piece_x, self.piece_y = 3,0
               
    def nextpiece(self):
        self.piece = self.next_piece
        self.next_piece = Piece()
        self.piece_x, self.piece_y = 3,0
        
    def absorb_piece(self):
        for y, row in enumerate(self.piece):
            for x, block in enumerate(row):
                if block:
                    self.board[y+self.piece_y][x+self.piece_x] = block
        self.nextpiece()
        self.score += self.level
        if self.skill < 100:
            self.skill += 5

    def block_collide_with_board(self, x, y):
        if x < 0:
            return Board.COLLIDE_ERROR['left_wall']
        elif x >= self.width:
            return Board.COLLIDE_ERROR['right_wall']
        elif y >= self.height:
            return Board.COLLIDE_ERROR['bottom']
        elif self.board[y][x]:
            return Board.COLLIDE_ERROR['overlap']
        return Board.COLLIDE_ERROR['no_error']

    def collide_with_board(self, dx, dy):
        for y, row in enumerate(self.piece):
            for x, block in enumerate(row):
                if block:
                    collide = self.block_collide_with_board(x=x+dx, y=y+dy)
                    if collide:
                        return collide
        return Board.COLLIDE_ERROR['no_error']

    def can_move_piece(self, dx, dy):
        _dx = self.piece_x + dx
        _dy = self.piece_y + dy
        if self.collide_with_board(dx = _dx, dy = _dy):
            return False
        return True

    def can_drop_piece(self):
        return self.can_move_piece(dx=0, dy=1)

    def try_rotate_piece(self, clockwise=True):
        self.piece.rotate(clockwise)
        collide = self.collide_with_board(dx=self.piece_x, dy=self.piece_y)
        if not collide:
            pass
        elif collide == Board.COLLIDE_ERROR['left_wall']:
            if self.can_move_piece(dx=1, dy=0):
                self.move_piece(dx=1, dy=0)
            elif self.can_move_piece(dx=2, dy=0):
                self.move_piece(dx=2, dy=0)
            else:
                self.piece.rotate(not clockwise)
        elif collide == Board.COLLIDE_ERROR['right_wall']:
            if self.can_move_piece(dx=-1, dy=0):
                self.move_piece(dx=-1, dy=0)
            elif self.can_move_piece(dx=-2, dy=0):
                self.move_piece(dx=-2, dy=0)
            else:
                self.piece.rotate(not clockwise)
        else:
            self.piece.rotate(not clockwise)

    def move_piece(self, dx, dy):
        if self.can_move_piece(dx, dy):
            self.piece_x += dx
            self.piece_y += dy

    def drop_piece(self):
        if self.can_drop_piece():
            self.move_piece(dx=0, dy=1)
        else:
            self.absorb_piece()
            self.delete_lines()
            
    def full_drop_piece(self):
        while self.can_drop_piece():
            self.drop_piece()
        self.drop_piece()

    def rotate_piece(self, clockwise=True):
        self.try_rotate_piece(clockwise)

    def pos_to_pixel(self, x, y):
        return self.block_size*x, self.block_size*(y-2)

    def pos_to_pixel_next(self, x, y):
        return self.block_size*x*0.6, self.block_size*(y-2)*0.6

    def delete_line(self, y):
        for y in reversed(range(1, y+1)):
            self.board[y] = list(self.board[y-1])

    def delete_under(self):     # 맨 밑줄 없애는 아이템
        self.delete_line(19)
    
    def delete_vertical(self,x): # 세로로 없애는 아이템
        for i in range(len(self.board)):
            self.board[i][x]=0
    
    def delete_lines(self):
        for y,row in enumerate(self.board):
            if all(row):
                flag=False
                for x, block in enumerate(row): # 물음표가 존재하는 블럭이 사라지면 get_item()
                    num=self.col_num(block)
                    if num==8:
                        self.get_item()
                    elif num==15 and y!=19: # 라인에 맨 밑줄 사라지는 아이템이 있으면 그리고 그 라인이 맨 밑줄이 아니면 
                        flag=True
                    elif num==22 : # 라인에 세로로 사라지는 아이템이 있으면
                        self.delete_vertical(x)
                    
                line_sound=pygame.mixer.Sound("assets/sounds/Line_Clear.wav")
                line_sound.play()

                self.delete_line(y)

                if flag==True: # flag가 True이면 맨 밑줄 사라지는 아이템이 있으면 맨 밑줄을 없앰
                    self.delete_under()

                self.score += 10 * self.level

        
                '''self.goal -= 1
                
                if self.goal == 0:
                    if self.level < 10:
                        self.level += 1 # goal과 따로 level 올리는 부분 필요
                        self.goal = 5 * self.level
                    else:
                        self.goal = '-'
                '''
                ###
                if self.level <= 9:
                    pygame.time.set_timer(pygame.USEREVENT, (500 - 50 * (self.level-1)))
                else:
                    pygame.time.set_time(pygame.USEREVENT, 100)
    
    def get_item(self):     #인벤토리에 아이템 생성
        if len(inven)<3:
            inven.append(item_list[random.randrange(0,4)])
        return inven
    
    def use_item(self):     #인벤토리의 아이템 사용
        if len(inven)>0:
            item=inven[0]
            inven.pop(0)
            if item==item_list[0]:
                self.slow()
                t=threading.Timer(3,self.back_to_origin,args=None,kwargs=None)
                t.start()
            elif item==item_list[1]:
                self.fast()
                t=threading.Timer(3,self.back_to_origin,args=None,kwargs=None)
                t.start()
            elif item==item_list[2]:
                self.change()
            else:
                t=threading.Thread(target=self.squid_ink,args=(0,100))
                t.start()
        
    def show_item(self):    #인벤토리의 아이템들을 보여줌
            if len(inven)>=1:
                self.screen.blit(inven[0],(260,145))
                if len(inven)>=2:
                    self.screen.blit(inven[1],(288,145))
                    if len(inven)==3:
                        self.screen.blit(inven[2],(316,145))
                
    def back_to_origin(self): # 원래 속도로 돌아옴
        pygame.time.set_timer(pygame.USEREVENT,(500 - 50 * (self.level-1)))
        
    def slow(self): # 달팽이 아이템 기능
        pygame.time.set_timer(pygame.USEREVENT,1000)

    def fast(self): # 번개 아이템 기능
        pygame.time.set_timer(pygame.USEREVENT,100)

    def change(self):
        self.next_piece=Piece()

    def squid_ink(self,a,b): # 오징어 먹물 아이템 기능
        # 잉크 사운드 추가ink_sound=pygame.mixer.Sound('소리 파일')
        for i in range(3000):
            ink=self.screen.blit(squid_ink,(a, b))
        #ink_sound.play()
        
    def game_over(self):
        return sum(self.board[0]) > 0 or sum(self.board[1]) > 0

    def col_num(self, block):	#블록의 번호에 따라 색깔 맞게 지정하는 함수
        if block<8 and block:
            return 1
        elif block>7 and block<15: 
            return 8
        elif block>14 and block<22:
            return 15
        elif block>21 :
            return 22  
            
    def draw_blocks(self, array2d, color=WHITE, dx=0, dy=0):	#조건문으로 물음표,아이템들 블록에 띄움
        for y, row in enumerate(array2d):
            y += dy
            if y >= 2 and y < self.height:
                for x, block in enumerate(row):
                    if block:
                        x += dx
                        x_pix, y_pix = self.pos_to_pixel(x, y)
                        num = self.col_num(block)       
                        pygame.draw.rect(self.screen, self.piece.T_COLOR[block - num],
                                                (x_pix, y_pix, self.block_size, self.block_size))
                        pygame.draw.rect(self.screen, BLACK,
                                                (x_pix, y_pix, self.block_size, self.block_size), 1)
                                
                        if num==8:
                            self.screen.blit(question,(x_pix,y_pix))
                        elif num==15:
                            self.screen.blit(delete,(x_pix,y_pix))
                        elif num==22:
                            self.screen.blit(updown,(x_pix,y_pix))
                          
    def draw_shadow(self, array2d, dx, dy): # 그림자 오류 디버깅                    
        for y, row in enumerate(array2d):
            y+=dy
            if y >= 2 and y < self.height:
                for x, block in enumerate(row):
                    x+=dx
                    if block:
                        tmp = 1
                        while self.can_move_piece(0, tmp):
                            tmp += 1
                        x_s, y_s = self.pos_to_pixel(x, y+tmp-1)

                        pygame.draw.rect(self.screen, self.piece.T_COLOR[7],
                                                            (x_s, y_s, self.block_size, self.block_size))
                        pygame.draw.rect(self.screen, BLACK,
                                                            (x_s, y_s, self.block_size, self.block_size),1)

    def draw_next_piece(self, array2d, color=WHITE):	#col_num으로 단순화
        for y,row in enumerate(array2d):
            for x,block in enumerate(row):
                x_pix, y_pix = self.pos_to_pixel_next(x,y)
                if block:
                    num=self.col_num(block)

                    pygame.draw.rect(self.screen, self.piece.T_COLOR[block - num],
                                        (x_pix+255, y_pix+65, self.block_size * 0.5, self.block_size * 0.5))
                    pygame.draw.rect(self.screen, BLACK,
                                        (x_pix+255, y_pix+65, self.block_size * 0.5, self.block_size * 0.5),1)

    def draw(self, input_id): #글씨나 값들이 가운데에 오도록 조정함
        now = datetime.datetime.now()
        nowTime = now.strftime('%H:%M:%S')
        self.screen.fill(BLACK)
        for x in range(self.width):
            for y in range(self.height):
                x_pix, y_pix = self.pos_to_pixel(x, y)
                pygame.draw.rect(self.screen, (26,26,26),
                 (x_pix, y_pix, self.block_size, self.block_size))
                pygame.draw.rect(self.screen, BLACK,
                 (x_pix, y_pix, self.block_size, self.block_size),1)
        self.draw_shadow(self.piece, dx=self.piece_x, dy=self.piece_y)
        self.draw_blocks(self.piece, dx=self.piece_x, dy=self.piece_y)
        
        self.draw_blocks(self.board)
        pygame.draw.rect(self.screen, WHITE, Rect(250, 0, 350, 450))
        self.draw_next_piece(self.next_piece)
        next_text = pygame.font.Font('assets/Roboto-Bold.ttf', 18).render('NEXT  ', True, BLACK)
        item_text = pygame.font.Font('assets/Roboto-Bold.ttf', 18).render('ITEM  ', True, BLACK)
        self.show_item()
        
        pygame.draw.rect(self.screen, BLACK, [260, 145, 25, 25], 1)
        pygame.draw.rect(self.screen, BLACK, [288, 145, 25, 25], 1)
        pygame.draw.rect(self.screen, BLACK, [316, 145, 25, 25], 1)
        score_text = pygame.font.Font('assets/Roboto-Bold.ttf', 18).render('SCORE', True, BLACK)
        score_value = pygame.font.Font('assets/Roboto-Bold.ttf', 16).render(str(self.score), True, BLACK)
        level_text = pygame.font.Font('assets/Roboto-Bold.ttf', 18).render('LEVEL', True, BLACK)
        level_value = pygame.font.Font('assets/Roboto-Bold.ttf', 16).render(str(self.level), True, BLACK)
        time_text = pygame.font.Font('assets/Roboto-Bold.ttf', 18).render('TIMER', True, BLACK)        
        time_value = pygame.font.Font('assets/Roboto-Bold.ttf', 16).render(str(nowTime), True, BLACK)
        player_text = pygame.font.Font('assets/Roboto-Bold.ttf',18).render('PLAYER',True,BLACK)
        player_value = pygame.font.Font('assets/Roboto-Bold.ttf',16).render(input_id,True,BLACK)

        self.screen.blit(next_text, (275, 20))
        self.screen.blit(item_text, (275, 120))
        
        self.screen.blit(score_text, (270, 200))
        self.screen.blit(score_value, (290,225))
        self.screen.blit(level_text, (270, 270))
        self.screen.blit(level_value, (290,295))
        self.screen.blit(player_text, (270,340))
        self.screen.blit(player_value, (265, 365))
        self.screen.blit(time_text,(265,405))
        self.screen.blit(time_value,(275,430))

    def pause(self):
        fontObj = pygame.font.Font('assets/Roboto-Bold.ttf', 32)
        textSurfaceObj = fontObj.render('Paused', True, GREEN)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (175, 185)
        fontObj2 = pygame.font.Font('assets/Roboto-Bold.ttf', 16)
        textSurfaceObj2 = fontObj2.render('Press p to continue', True, GREEN)
        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj2.center = (175, 235)
        self.screen.blit(textSurfaceObj, textRectObj)
        self.screen.blit(textSurfaceObj2, textRectObj2)
        pygame.display.update()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYUP and event.key == K_p:
                    running = False

    def GameOver(self):    
        fontObj = pygame.font.Font('assets/Roboto-Bold.ttf', 32)
        textSurfaceObj = fontObj.render('Game over', True, GREEN)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (175, 185)
        fontObj2 = pygame.font.Font('assets/Roboto-Bold.ttf', 16)
        textSurfaceObj2 = fontObj2.render('Press a key to continue', True, GREEN)
        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj2.center = (175, 235)
        self.screen.blit(textSurfaceObj, textRectObj)
        self.screen.blit(textSurfaceObj2, textRectObj2)
        del inven[:]         #인벤토리와 속도 리셋되도록 설정
        self.back_to_origin()
        pygame.display.update()
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    running = False

    def newGame(self):
        fontObj = pygame.font.Font('assets/Roboto-Bold.ttf', 32)
        textSurfaceObj = fontObj.render('Tetris', True, GREEN)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (175, 185)
        fontObj2 = pygame.font.Font('assets/Roboto-Bold.ttf', 16)
        textSurfaceObj2 = fontObj2.render('Press a key to continue', True, GREEN)
        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj2.center = (175, 235)
        self.screen.fill(BLACK)
        self.screen.blit(textSurfaceObj, textRectObj)
        self.screen.blit(textSurfaceObj2, textRectObj2)
        pygame.display.update()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    running = False

    def HS(self, txt=[]):
        if txt != []:
            fontObj = pygame.font.Font('assets/Roboto-Bold.ttf', 25)
            fontObj2 = pygame.font.Font('assets/Roboto-Bold.ttf', 16)
            textSurfaceObj = fontObj.render("~Top 10 Score~", True, WHITE)
            textSurfaceObj2 = fontObj2.render('Press a key to continue', True, GREEN)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj2 = textSurfaceObj2.get_rect()
            textRectObj.center = (175, 35)
            textRectObj2.center = (175, 435)
            self.screen.fill(BLACK)
            self.screen.blit(textSurfaceObj, textRectObj)
            self.screen.blit(textSurfaceObj2, textRectObj2)
            for i,score in enumerate(txt):
                textSurfaceObj3_1 = fontObj.render("No."+str(i+1), True, WHITE)
                textSurfaceObj3_2 = fontObj.render(str(score[0]), True, WHITE)
                textSurfaceObj3_3 = fontObj.render(str(score[1]), True, WHITE)
                textRectObj3_1 = textSurfaceObj3_1.get_rect(); textRectObj3_1.center=(80,100+i*30)
                textRectObj3_2 = textSurfaceObj3_2.get_rect();textRectObj3_2.center=(180,100+i*30)
                textRectObj3_3 = textSurfaceObj3_3.get_rect();textRectObj3_3.center=(260,100+i*30)
                self.screen.blit(textSurfaceObj3_1, textRectObj3_1)
                self.screen.blit(textSurfaceObj3_2, textRectObj3_2)
                self.screen.blit(textSurfaceObj3_3, textRectObj3_3)



            pygame.display.update()
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == KEYDOWN:
                        running = False

    def ultimate(self):
        if self.skill == 100:
            bomb = pygame.image.load("assets/images/bomb.jpg")
            bomb = pygame.transform.scale(bomb, (350, 450))
            bomb_sound = pygame.mixer.Sound('assets/sounds/bomb.wav')
            self.screen.blit(bomb, (0, 0))
            pygame.display.update()
            bomb_sound.play()
            time.sleep(1)
            self.board = []
            self.skill = 0
            for _ in range(self.height):
                self.board.append([0]*self.width)
