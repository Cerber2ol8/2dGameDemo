# 2dGameDemo
Pygame Simple 2d game demo

# 使用Pygame制作的2d动作游戏demo
pygame版本1.9.6
使用pygame库编写的2d动作游戏demo，可以直接下载game.exe 运行（由pyinstaller生成的可执行程序,体积偏大无法上传github）
链接：https://pan.baidu.com/s/19e5o-idWOZ03OVp_vP7h7w?pwd=bifi 
提取码：bifi 

（运行该demo需要提前下载资源目录src和data）


![image](https://raw.githubusercontent.com/Cerber2ol8/2dGameDemo/master/imgs/01.png)
![image](https://raw.github.com/Cerber2ol8/2dGameDemo/master/imgs/02.png)
![image](https://raw.github.com/Cerber2ol8/2dGameDemo/master/imgs/03.png)
Demo目前主要包括以下部分：

# 角色多状态转换，共15种状态
actionSpace = {'stand':0,'walk':1,'run':2,'jump':3,'attack':4,'stick':5, 
'jumpCut':6,'pickOn':7,'hurt':8, 'attackRig':9,'fall':10,
'dead':11,'combo':12,'con_combo':13,'swordSkill':14}  

# 图像资源加载和处理、序列帧的播放和控制、镜头移动和跟随、地图碰撞检测
![image](https://raw.github.com/Cerber2ol8/2dGameDemo/master/imgs/normal.gif)

# 动作系统combat
角色碰撞和攻击检测，简单UI（血条动画），简单敌人AI控制
![image](https://raw.github.com/Cerber2ol8/2dGameDemo/master/imgs/combat.gif)
# 简单背包实现
![image](https://raw.github.com/Cerber2ol8/2dGameDemo/master/imgs/04.png)

# 简单的地图边界编辑器（地图边界绘制）
![image](https://raw.github.com/Cerber2ol8/2dGameDemo/master/imgs/05.png)
![image](https://raw.github.com/Cerber2ol8/2dGameDemo/master/imgs/06.png)
# 文本播放（加载和裁剪字符串并控制实现顺序播放文本，控制播放速度）
![image](https://raw.github.com/Cerber2ol8/2dGameDemo/master/imgs/textbox.gif)
