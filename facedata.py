import os 
import torch
from torch.utils.data import DataLoader,Dataset
from torchvision import transforms
from pathlib import Path
import cv2

cls_dic={
        "front":0,
        "up":1,
        "down":2,
        "left":3,
        "right":4
    }


class FaceData(Dataset):
    def __init__(self, root_data='./data/'):
        self.root_data=root_data
        p=Path(root_data)
        self.FileList=list(p.glob('**/*.jpg'))
        self.transformer=transforms.ToTensor()
        
    def __getitem__(self, index):
        img=cv2.imread('./'+str(self.FileList[index]))
        img=cv2.resize(img,(28,28),cv2.INTER_LINEAR)
        img=self.transformer(img)
        cls=cls_dic[str(self.FileList[index]).split('\\')[1].split('_')[-1]]
        #print(img.shape)
        #print(cls)
        return img,cls

    def __len__(self):
        return len(self.FileList)


if __name__=="__main__":
    dataset=FaceData("./data/")
    dataloader=DataLoader(dataset)
    for image in dataloader:
        print(image)
        break
    
