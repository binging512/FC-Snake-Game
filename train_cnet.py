import torch
import torch.nn as nn
import os
import cnet
import facedata
from tqdm import tqdm
from torch.utils.data import DataLoader,Dataset
from torch.optim import lr_scheduler

def train(epoches,batch_size,lr,root_weights,checkpoints=None,cuda=True):
    net=cnet.CNet()
    net.train()
    dataset=facedata.FaceData(root_data='./data/')
    dataloader=DataLoader(dataset,batch_size,shuffle=True,num_workers=2)

    if checkpoints is not None:
        net.load_state_dict(torch.load(checkpoints))
    if cuda is True:
        net=net.cuda()
    if not os.path.exists(root_weights):
        os.mkdir(root_weights)

    loss_func=nn.CrossEntropyLoss()
    optimizer=torch.optim.Adam(net.parameters(),lr=lr)
    scheduler = lr_scheduler.StepLR(optimizer, step_size=3, gamma=0.8)

    for epoch in tqdm(range(epoches),desc='Epoches:',ncols=80):
        n=0
        for img,label in tqdm(dataloader,desc='Batches:',ncols=80):
            n = n + 1
            optimizer.zero_grad()
            input=img
            target=label.long()
            if cuda is True:
                input=input.type(torch.FloatTensor).cuda()
                target=target.cuda()
            output=net(input)
            loss=loss_func(output,target)
            loss.backward()
            optimizer.step()

        scheduler.step()
        if epoch%1==0:
            torch.save(net.state_dict(),'./weights_epoch'+str(epoch)+'.pth')
        os.system('cls')
    torch.save(net.state_dict(),root_weights+'weights_final.pth')



if __name__=="__main__":
    epoches=10
    batch_size=32
    lr=0.001
    root_weights="./weights/"
    train(epoches,batch_size,lr,root_weights,checkpoints=None,cuda=True)