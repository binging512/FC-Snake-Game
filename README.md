# FC-Snake-Game
基于头部控制的贪吃蛇游戏
## 简介
本游戏分为游戏本体与控制算法。游戏本体为贪吃蛇游戏，使用pygame框架实现。控制算法为使用电脑摄像头获取人脸朝向的算法，用于对人脸朝向进行捕捉，并用于对游戏中的贪吃蛇进行控制。
游戏本体我们借用了别人的部分代码，参考链接如下：
https://blog.csdn.net/weixin_41775042/article/details/79575925
人脸朝向算法分为两部分：人脸检测算法与人脸朝向分类算法。其中人脸检测算法我们借用了DFace (Deeplearning Face)，参考链接如下：
https://github.com/kuaikuaikim/DFace
为了保证实时性，人脸朝向分类算法我们采用一个小型的网络进行分类。

## 安装
### 测试运行环境
- Python 3.7
- Cuda 10.1
- torch==1.6.0
- torchvision==0.7.0
- opencv_python==4.4.0
- easygui==0.98.1
- pygame==1.9.6
- numpy==1.19.4

以上环境及资源包版本全部是我们进行测试时采用的，对于其他版本的资源包也可能让程序正常运行。
### 安装步骤
1. 下载程序
'''shell
git clone https://github.com/binging512/FC-Snake-Game.git
'''
2. 安装资源包
'''shell
python3 -m pip install -r requirements.txt
'''
3.下载模型权重文件（百度网盘）
链接：https://pan.baidu.com/s/1BvIJI0EQoiAxJpFrEv9HRg 
提取码：y46f
4. 运行游戏
'''shell
python games.py
'''
## 训练模型
1. DFace模型训练
对于DFace人脸检测模型的训练，请参见官方文档：https://github.com/kuaikuaikim/DFace
2. 人脸朝向分类器的训练
- 准备数据集
将个人准备的数据图像全部放入 ./data 文件夹下，并将每个人脸朝向分别放入多个文件夹中，例如：
'''
./data/xxx_up ->存放xxx的头部向上的图像
./data/yyy_down ->存放yyy的头部向下的图像
'''
由于需要将人脸朝向分为5类，向上、向下、向左、向右以及正向，因此请将每个人的人脸图像放入相应的文件夹中（up，down，left，right，front）。由于内部代码需要，请严格对每个文件夹进行命名，保证文件夹最后一个下划线后为以上五个单词中的一个。（如果出现其他的命名格式，即会报错）
- 训练
'''shell
python train_cnet.py
'''
## 界面预览





