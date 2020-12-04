import threading
import cv2

def f1():
    global x
    x=0
    while True:
        print(int(x/10))

def f2():
    global x
    x=0
    while True:
        x=x+1
        print(x)
        cv2.waitKey(100)


if __name__=="__main__":
    t1=threading.Thread(target=f1)