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

#加载人脸模型库
def face_detection():
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
            print((top_x,top_y,bottom_x,bottom_y),'\t',cls)
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

if __name__=="__main__":
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
            print((top_x,top_y,bottom_x,bottom_y),'\t',cls)
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