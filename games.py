import pygame
from abc import ABCMeta, abstractclassmethod
from random import randint
from pygame.locals import *
import easygui
import time
import cv2
import os
import math
import torch
from torchvision.transforms import ToTensor
from cnet import CNet
from dface.core.detect import create_mtcnn_net, MtcnnDetector
import dface.core.vision as vision
import time
import numpy
import threading

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
        if x > 1000 or x < 10 or y > 1000 or y < 10:
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
        pygame.draw.rect(screen, self._color,(self._x, self._y, self._size, self._size), 0)
        pygame.draw.rect(screen, Black_color,(self._x, self._y, self._size, self._size), 1)

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
        pygame.draw.rect(screen, self._color,(self._x, self._y, self._width, self._height), 4)

class Food(GameObject):
    def __init__(self, x, y, size, color=Food_color):
        super().__init__(x, y, color)
        self._size = size
        self._hide = False
    def draw(self, screen):
        if not self._hide:
            pygame.draw.circle(screen, self._color,(self._x + self._size // 2, self._y + self._size // 2),self._size // 2, 0)
        # 处理圆和半径的中心点 否则无法相遇
        self._hide = not self._hide

def game():    
    def refresh():
        '''刷新游戏窗口'''
        screen.fill((242, 242, 242))
        snake.draw(screen)
        wall.draw(screen)
        food.draw(screen)
        pygame.display.flip()
    def handle_key_event(key_event):
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
    def handle_face_out(key):
        if key == 0:
            print(11111)
            return 0
        if key == 1:
            new_dir = UP
        elif key == 4:
            new_dir = RIGHT
        elif key == 2:
            new_dir = DOWN
        elif key == 3:
            new_dir = LEFT
        else:
            new_dir = key
        if new_dir != snake.dir:
            snake.change_dir(new_dir)        
    def create_food():
        row = randint(1, 28)
        col = randint(1, 28)
        return Food(10 + 20 * row, 10 + 20 * col, 20)
    def count_txt(snake):
        score = len(snake._nodes) - 5
        my_font = pygame.font.SysFont('楷体', 60)
        game_over = my_font.render('GAME OVER', False, [0, 0, 0])
        score = my_font.render('score:' + str(score), False, [255, 0, 0])
        screen.blit(score, (400, 30))
        screen.blit(game_over, (180, 260))
        pygame.display.flip()
    wall = Wall(10, 10, 1000, 800)
    food = create_food()
    snake = Snake()
    pygame.init()
    screen = pygame.display.set_mode((1020, 820))
    pygame.display.set_caption('贪吃蛇')
    background = screen.fill((242, 242, 242))
    pygame.display.flip()
    clock = pygame.time.Clock()
    running = True
    over = True

    global face_out
    face_out = 0
    while running:
        #----------------------------------------------#
        #for event in pygame.event.get():
        #    if event.type == pygame.QUIT:
        #        running = False
        #    elif event.type == pygame.KEYDOWN:
        #        handle_key_event(event)
        print(face_out)
        handle_face_out(face_out)

        if over:
            refresh()
        clock.tick(5)
        if over:
            snake.move()
            # time.sleep(0.1)
            if snake.eat_food(food):
                food = create_food()
            if snake.is_over() or snake.eat_me():
                count_txt(snake)
                Yes_or_No = easygui.buttonbox("不好意思，游戏结束", choices=['我不服我还要玩', '我不玩了886'])
                if Yes_or_No == '我不服我还要玩':
                    snake = Snake()
                    pygame.event.clear()
                else:
                    over = False
    pygame.quit()

def face_detection():
    global face_out
    global ready
    #face detection model
    p_model_path="./weights/pnet_epoch.pt"
    r_model_path="./weights/rnet_epoch.pt"
    o_model_path="./weights/onet_epoch.pt"
    pnet, rnet, onet = create_mtcnn_net(p_model_path, r_model_path, o_model_path, use_cuda=True)
    mtcnn_detector = MtcnnDetector(pnet=pnet, rnet=rnet, onet=onet, min_face_size=24)
    assert os.path.exists(p_model_path), "pnet Model Path is not exist!"
    assert os.path.exists(r_model_path), "rnet Model Path is not exist!"
    assert os.path.exists(o_model_path), "onet Model Path is not exist!"

    #face classification model
    cls_model_path='./weights/cnet_final.pth'
    assert os.path.exists(cls_model_path), "Cls Model Path is not exist!"
    net=CNet()
    net.load_state_dict(torch.load(cls_model_path))
    transform=ToTensor()

    #get face data (used for training)
    #save_dir='./data/null/'
    #if not os.path.isdir(save_dir):
    #    os.mkdir(save_dir)

    #打开摄像头
    capture=cv2.VideoCapture(0)
    
    i=0
    while True:
        ready=True
        print(ready)
        timer1=time.time()
        ret,frame=capture.read()
        faces,_= mtcnn_detector.detect_face(frame)
        
        for (top_x,top_y,bottom_x,bottom_y,s) in faces:
            i=i+1
            top_x = int(top_x)
            top_y = int(top_y)
            bottom_x=int(bottom_x)
            bottom_y=int(bottom_y)
            #矩形标记
            cv2.rectangle(frame,(int(top_x),int(top_y)),(int(bottom_x),int(bottom_y)),(0,255,0),2)
            frame_save=frame[top_y:bottom_y,top_x:bottom_x,:]
            try:
                #cv2.imwrite(save_dir+str(i)+'.jpg',frame_save)
                cls_input=transform(cv2.resize(frame_save,(28,28))).unsqueeze(0)
            except:
                continue
            out=net(cls_input)
            cls=torch.argmax(out,dim=1)
            print((top_x,top_y,bottom_x,bottom_y),'\t',cls.item())
            face_out=cls.item()
        timer2=time.time()
        #print(timer2-timer1)
        #显示图片
        cv2.imshow("faces in video",frame)
        #暂停窗口
        if cv2.waitKey(5) & 0xFF ==ord('q'):
            break
    #释放资源
    capture.release()
    #销毁窗口
    cv2.destroyAllWindows()

if __name__ == '__main__':
    global ready
    ready=False
    print(ready)
    
    thread_2=threading.Thread(target=face_detection)
    thread_2.start()
    while True:
        #print(ready)
        if ready==True:
            print('the model is ready!')
            thread_1=threading.Thread(target=game)
            thread_1.start()
            break
    