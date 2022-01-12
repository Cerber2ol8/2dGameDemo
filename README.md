# 2dGameDemo
Pygame Simple 2d game demo

#使用Pygame构建的2d动作游戏demo
![image](https://github.com/Cerber2ol8/2dGameDemo/blob/master/imgs/01.png)
![image](https://github.com/Cerber2ol8/2dGameDemo/blob/master/imgs/02.png)
![image](https://github.com/Cerber2ol8/2dGameDemo/blob/master/imgs/03.png)
Demo目前主要包括以下部分：

角色多状态转换，共15种状态
actionSpace = {'stand':0,'walk':1,'run':2,'jump':3,'attack':4,'stick':5, 
'jumpCut':6,'pickOn':7,'hurt':8, 'attackRig':9,'fall':10,
'dead':11,'combo':12,'con_combo':13,'swordSkill':14}
图像资源加载和处理、序列帧的播放和控制、镜头移动和跟随、地图碰撞检测
![image](https://github.com/Cerber2ol8/2dGameDemo/blob/master/imgs/normal.gif)

角色碰撞和攻击检测
简单UI（血条动画）
简单敌人AI控制
![image](https://github.com/Cerber2ol8/2dGameDemo/blob/master/imgs/combat.gif)
简单背包系统
![image](https://github.com/Cerber2ol8/2dGameDemo/blob/master/imgs/04.png)

简单的地图边界编辑器（地图边界绘制）
![image](https://github.com/Cerber2ol8/2dGameDemo/blob/master/imgs/05.png)
![image](https://github.com/Cerber2ol8/2dGameDemo/blob/master/imgs/06.png)
文本播放（加载和裁剪字符串并控制实现顺序播放文本，控制播放速度）
![image](https://github.com/Cerber2ol8/2dGameDemo/blob/master/imgs/textbox.gif)
