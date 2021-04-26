import pygame
from abc import ABCMeta, abstractclassmethod
from random import randint
from pygame.locals import *
import easygui
import time
Black_color = (0, 0, 0)
Food_color = (236, 189, 187)
Green_color = (0, 255, 0)

# 顺时针或者逆时针
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class GameObject(object, metaclass=ABCMeta):
    def __init__(self, x, y, color):
        self._x = x
        self._y = y
        self._color = color
    @property
    def x(self):
        return self._x
    @property
    def y(self):
        return self._y
    @abstractclassmethod
    def draw(self, screen):
        pass 

class Snake(GameObject):
    def __init__(self):
        self._dir = LEFT
        self._nodes = []
        self.has_eat_food = False
        for index in range(5):
            node = SnakeNode(290 + index * 20, 250, 20)
            self._nodes.append(node)
    @property
    def dir(self):
        return self._dir 
    def change_dir(self, new_dir):
        if (self._dir + new_dir) % 2 != 0:
            self._dir = new_dir
    def draw(self, screen):
        for node in self._nodes:
            node.draw(screen)
    def move(self):
        head = self._nodes[0]
        sdir = self._dir
        x, y, size = head.x, head.y, head.size
        if sdir == UP:
            y -= size
        elif sdir == RIGHT:
            x += size
        elif sdir == DOWN:
            y += size
        else:
            x -= size
        new_head = SnakeNode(x, y, size)
        self._nodes.insert(0, new_head)
        if self.has_eat_food:
            self.has_eat_food = False
        else:
            self._nodes.pop()
    def is_over(self):
        '''撞墙返回真，否则返回假'''
        head = self._nodes[0]
        x, y, size = head.x, head.y, head.size
        if x > 600 or x < 10 or y > 600 or y < 10:
            return True
        return False
    def eat_food(self, food):
        head = self._nodes[0]
        if food.x == head.x and food.y == head.y:
            self.has_eat_food = True
            return True
        return False
    def eat_me(self):
        for a in range(4, len(self._nodes)):
            if self._nodes[0].x == self._nodes[a].x and self._nodes[0].y == self._nodes[a].y:
                return True
        return False

class SnakeNode(GameObject):
    def __init__(self, x, y, size, color=Green_color):
        super().__init__(x, y, color)
        self._size = size
        self._color = color
    @property
    def size(self):
        return self._size
    def draw(self, screen):
        pygame.draw.rect(screen, self._color,
                         (self._x, self._y, self._size, self._size), 0)
        pygame.draw.rect(screen, Black_color,
                         (self._x, self._y, self._size, self._size), 1)

class Wall(GameObject):
    def __init__(self, x, y, width, height, color=Black_color):
        super().__init__(x, y, color)
        self._width = width
        self._height = height
    @property
    def width(self):
        return self._width
    @property
    def height(self):
        return self._height
    def draw(self, screen):
        pygame.draw.rect(screen, self._color,
                         (self._x, self._y, self._width, self._height), 4)

class Food(GameObject):
    def __init__(self, x, y, size, color=Food_color):
        super().__init__(x, y, color)
        self._size = size
        self._hide = False
    def draw(self, screen):
        if not self._hide:
            pygame.draw.circle(screen, self._color,
                             (self._x + self._size // 2, self._y + self._size // 2),
                              self._size // 2, 0)
        # 处理圆和半径的中心点 否则无法相遇
        self._hide = not self._hide

def main():
    def refresh(screen, snake, wall, food):
        '''刷新游戏窗口'''
        screen.fill((242, 242, 242))
        snake.draw(screen)
        wall.draw(screen)
        food.draw(screen)
        pygame.display.flip()
    def handle_key_event(key_event,snake):
        key = key_event.key
        if key == K_UP:
            new_dir = UP
        elif key == K_RIGHT:
            new_dir = RIGHT
        elif key == K_DOWN:
            new_dir = DOWN
        elif key == K_LEFT:
            new_dir = LEFT
        else:
            new_dir = key
        if new_dir != snake.dir:
            snake.change_dir(new_dir)
    def handle_face_out(key, snake):
        if key == None:
            return 0
        if key == 'up':
            new_dir = UP
        elif key == 'right':
            new_dir = RIGHT
        elif key == 'down':
            new_dir = DOWN
        elif key == 'left':
            new_dir = LEFT
        else:
            new_dir = key
        if new_dir != snake.dir:
            snake.change_dir(new_dir)
    def create_food():
        row = randint(1, 28)
        col = randint(1, 28)
        return Food(10 + 20 * row, 10 + 20 * col, 20)
    def count_txt(snake, screen):
        score = len(snake._nodes) - 5
        my_font = pygame.font.SysFont('楷体', 60)
        game_over = my_font.render('GAME OVER', False, [0, 0, 0])
        score = my_font.render('score:' + str(score), False, [255, 0, 0])
        screen.blit(score, (400, 30))
        screen.blit(game_over, (180, 260))
        pygame.display.flip()
    pygame.init()
    ck = pygame.display.set_mode((800,600))
    pygame.display.set_caption("贪吃蛇")    
    clock = pygame.time.Clock()                       
    start_ck = pygame.Surface(ck.get_size())    
    start_ck2 = pygame.Surface(ck.get_size())  
    start_ck = start_ck.convert()
    start_ck2 = start_ck2.convert()
    start_ck.fill((255,255,255))  
    start_ck2.fill((0,255,0))
    i1 = pygame.image.load("./image3.png")
    i1.convert()
    i11 = pygame.image.load("./image2.png")
    i11.convert()
    running = True
    while running:
        start_ck.blit(i11, (300, 400))
        start_ck.blit(i1, (120, 240))
        ck.blit(start_ck,(0,0))
        pygame.display.update()
        # while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                key = event.key
                if key == K_DOWN:
                    running = False
                    pygame.quit()
            elif event.type == pygame.QUIT:
                print("游戏退出...")
                # quit 卸载所有的模块
                pygame.quit()
                # exit() 直接终止当前正在执行的程序
                exit()
    def game_init():
        wall = Wall(10, 10, 600, 600)
        food = create_food()
        snake = Snake()
        pygame.init()
        screen = pygame.display.set_mode((620, 620))
        pygame.display.set_caption('贪吃蛇')
        background = screen.fill((242, 242, 242))
        pygame.display.flip()
        clock = pygame.time.Clock()
        # game_init()
        running = True
        over = True
        face_out = None
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    handle_key_event(event,snake)
                else:
                    handle_face_out(face_out, snake)
            if over:
                refresh(screen, snake, wall, food)
            clock.tick(10)
            if over:
                snake.move()
                # time.sleep(0.1)
                if snake.eat_food(food):
                    food = create_food()
                if snake.is_over() or snake.eat_me():
                    count_txt(snake, screen)
                    time.sleep(1)
                    pygame.quit()
                    return 0
    def controlGame_init():
        pygame.init()
        ck = pygame.display.set_mode((800,600))   
        pygame.display.set_caption("贪吃蛇")    
        clock = pygame.time.Clock()                         
        start_ck = pygame.Surface(ck.get_size())   
        start_ck2 = pygame.Surface(ck.get_size())  
        start_ck = start_ck.convert()
        start_ck2 = start_ck2.convert()
        start_ck.fill((255,255,255)) 
        start_ck2.fill((0,255,0))
        i1 = pygame.image.load("./image5.png")
        i1.convert()
        i11 = pygame.image.load("./image4.png")
        i11.convert()
        running = True
        while running:
            start_ck.blit(i11, (300, 240))
            start_ck.blit(i1, (120, 400))
            ck.blit(start_ck,(0,0))
            pygame.display.update()
            # while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    key = event.key
                    if key == K_DOWN:
                        running = False
                        pygame.quit()
                        return True
                    elif key == K_RIGHT or key == K_LEFT:
                        pygame.quit()
                        exit()
                elif event.type == pygame.QUIT:
                    print("游戏退出...")
                    pygame.quit()
                    exit()
    while(True):
        game_init()
        ifquit = controlGame_init()
        if ifquit:
            continue
        else:
            break

if __name__ == '__main__':
    main()
