import torch
import torch.nn as nn
import torch.nn.functional as F
import time

class Block(nn.Module):
    def __init__(self,in_channels,out_channels,kernel_size,stride,padding):
        super(Block,self).__init__()
        self.layer=nn.Sequential(
            nn.Conv2d(in_channels,out_channels,kernel_size,stride,padding,bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True)
            )
    def forward(self,x):
        out = self.layer(x)
        return out


class CNet(nn.Module):
    def __init__(self):
        super(CNet,self).__init__()
        self.conv1=Block(in_channels=3,out_channels=8,kernel_size=3,stride=2,padding=1)
        self.conv2=Block(in_channels=8,out_channels=16,kernel_size=3,stride=2,padding=1)
        self.conv3=Block(in_channels=16,out_channels=32,kernel_size=3,stride=2,padding=1)
        self.fc=nn.Linear(512,5)
    def forward(self, x):
        out = self.conv1(x)
        #print(out.shape)
        out = self.conv2(out)
        #print(out.shape)
        out = self.conv3(out)
        #print(out.shape)
        #out = F.avg_pool2d(out, 4)
        out = out.view(out.size(0), -1)
        out = self.fc(out)
        #print(out.shape)
        return out

if __name__=="__main__":
    model = CNet()
    model.eval()
    #print(model)
    #model = model.cuda()
    time_start=time.time()
    for i in range(30):
        input = torch.randn(1, 3, 28, 28)
        #input = input.cuda()
        out = model(input)
    time_end=time.time()
    print((time_end-time_start))
