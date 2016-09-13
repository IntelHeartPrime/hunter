'''
 File name: GameFrame.py
 Description: The GameFrame above Pygame

 Author: Xin Yan
 next version :
    1,单例模式的摄像机
    2,可以互相嵌套的的GameObject   通过 **childGameObject 字典传入
    3,场景类 （场景开始，结束，切换）

    4，碰撞提类， 与GameObject类绑定  ，可以获取GamObject类的信息
        并随之变化而变化
        碰撞体类也是可以嵌套的。并且每一个对象都可以设置 状态：  起作用/失效

    5,内部脚本方法，script属性;   内部脚本方法 ： runScripts
'''

'''
使用规范：
1，要求嵌套的GameObject使用一个中心坐标
'''
import time
import pygame,sys
from pygame.locals import *
#import ConnectMysql

import random

#用户更改项
WINDOWWIDTH=900
WINDOWHEIGHT=600

camerax=WINDOWWIDTH/2
cameray=WINDOWHEIGHT/2
camera=(camerax,cameray)
sence_now=None            #用于存储当前场景的中间变量

#摄像机类
def Singleton(cls,*args,**kw):
    instances={}
    def _singleton(*args,**kw):
        if cls not in instances:
            instances[cls]=cls(*args,**kw)
        return instances[cls]
    return _singleton

@Singleton
class Camera():
    def __init__(self,logicPoint,paintPoint):
        '''
        摄像机类
        :param logicPoint: 逻辑坐标元组/设计坐标元组
        :param paintPoint: 绘制坐标元祖
        '''
        self.logicPointx=logicPoint[0]
        self.logicPointy=logicPoint[1]

        self.paintPointx=paintPoint[0]
        self.paintPointy=paintPoint[1]


#资源类
class Resource:                 #resource为单个资源 ， point为坐标元组 （资源的初始逻辑坐标） pont=(pointx.pointy)
    #length为资源长度元组 （lengthx,lengthy)
    def __init__(self,resource,logicPoint,paintPoint,length):
        '''
        资源类：单个资源
        :param resource: 资源文件/img对象
        :param logicPoint: 逻辑坐标元组/设计坐标元组
        :param paintPoint: 绘制坐标元组
        :param length: 长度元组（x方向长度，y方向长度）
        '''
        self.resource=resource
        self.bool=True      #用于判定是否需要绘制的标识
        self.logicPointx=logicPoint[0]
        self.logicPointy=logicPoint[1]

        self.lengthx=length[0]
        self.lengthy=length[1]

        self.paintPointx=paintPoint[0]
        self.paintPointy=paintPoint[1]


#GameOBject类         此处每一个资源就是一个gameObject类 ，  多资源版本
class GameObject:

    def __init__(self,camera,resources,paintsurface,**ChildGameObject) : #*resourse类列表   paintsurface 为画布
        '''
        GameObject类，子GameObject
        :param camera: 摄像机类
        :param resources: 资源类元组
        :param paintsurface: 画布
        :param *ChildGameObject:  子嵌套的任意多个GameObject类实例,必须以字典形式传入
        '''
        self.ChildGameObject=ChildGameObject  # the dictionary of childGameObject
        #print(self.ChildGameObject)           #output information of the tuple
        self.camera=camera
        self.resources=resources
        self.paintsurface=paintsurface
        self.timewaitflag=False
        self.time1=0
        self.time2=0
        self.step = 0
        self.runOnce()
        # 在外部定义方法传入script属性，直接对GameObject进行控制（支持在外部进行控制）
        self.script = lambda self: None  # 给一个默认值

        '''
        外部控制的GameObject示例：
        假设当前有GameObject实例GB1
        1，外部代码区直接添加GameObject类的子GameObject类
        GB1.childGameObject[childName]=childGameObject
        2,定义外部脚本控制函数
        def control1(self):
            self.childGameObject[childName].acton()
            xxxxxx任意操作都可以
        3，将外部函数传入到GB1的script属性
        GB1.script=control1
        4，执行方法
        gameobject.script(gameobject)
        '''


    #只运行一次的函数
    def runOnce(self):
        pass

    #求资源绘制坐标函数
    def getdrawpoint(self):
        '''
        由资源的逻辑坐标求出绘制坐标
        :return: None
        '''
        for resource1 in self.resources:
            resource1.paintPointx = self.camera.paintPointx+(resource1.logicPointx-self.camera.logicPointx)
            resource1.paintPointy = self.camera.paintPointy+(resource1.logicPointy-self.camera.logicPointy)



    #绘制判定函数
    def drawtesting(self):
        '''
        判定是否需要绘制 （如果超出窗口外部，则不需要绘制）
        :return: None
        '''
        self.getdrawpoint()
        for resource in self.resources:
            # 资源绘制坐标-边界坐标>资源长度
            if 0-resource.paintPointx > resource.lengthx:
                resource.bool = False
            else:
                if resource.paintPointx > 0+WINDOWWIDTH:
                    resource.bool = False
                else:
                    if 0-resource.paintPointy > resource.lengthy:
                        resource.bool = False
                    else:
                        if resource.paintPointy-0 > WINDOWHEIGHT:
                            resource.bool = False
                        else:
                            resource.bool = True

    def drawGameObject(self):
        pass   # 需要重写       方法不能是空的方法

    def timecontrol(self,delaystep):  # 时间控制，使得不需要多线程实现控制型动画
        '''
        每一个需要异步的动画都需要重写一个相关的函数，需要自己的time1，timewaitflage ,time2
        step可以共用

        当进行同变量动画突变时候，必须要进行时间控制函数重置

        :param delaystep:
        :return:
        '''
        if self.timewaitflag == False:
            self.time1=self.step
            self.timewaitflag=True
        self.time2=self.step
        if self.time2-self.time1==delaystep:
            self.timewaitflag=False
            return True
        return False

    #用于重置timecontrol的函数 ，在动画改变时使用
    def resetTimeControl(self):
        self.timewaitflag=False

    def operateControl(self):
        pass

    def runScripts(self):
        '''
        重写此方法，类似于unity3d 的脚本控制区;直接对传入的GameObject进行操作，此方法相当于update() 方法（每一帧绘制一次）
        :return:
        '''
        pass


    def action(self):
        self.drawtesting()
        self.drawGameObject()
        self.operateControl()
        self.step+=1

        self.script(self)   #运行外部脚本函数
        self.runScripts()   #运行内部脚本函数
        for x in self.ChildGameObject:
            x.action()


def Change_Sence(sence):
    '''
    :param sence: 要切换到的场景对象
    实现原理：游戏中需要存在一个用于存储当前场景的中间变量
    替换这个变量
    :return:
    '''
    global sence_now
    sence_now=sence


class Sence():
    '''
    面临的问题：  绘图层级问题
    '''
    def __init__(self,name):
        '''
        :param name: 场景名称
        '''
        self.name=name
        self.GameObjects=[]    #Sence的GameObject列表，通过遍历action()函数来切换场景
        self.runOnce()
    def ControlDrawLevel(self):
        pass
    def runOnce(self):
        pass
    def runScripts(self):
        pass

    def action(self):
        self.runScripts()
        for x in self.GameObjects:
            x.action()


class Colider():
    '''
    1，在逻辑坐标中进行碰撞
    2，将GameObject传入Colider中进行绑定
    3，支持图形化添加碰撞体
    4，重力功能
    5，刚体功能  物理判定方法 physics()  ,可以对GameObject类进行操作。
    6，Colider支持嵌套

    矩形， 刚体 ， 判定框

    Colider标识符：   与xxx （多参数）碰撞 、Ture or False
    '''
    def __init__(self,GameObject):
        '''

        :param childColider: 方式传入的
        '''
        self.judgeColider=[]                       #默认为一个列表，在外部或者脚本中进行修改
        self.GameObject=GameObject
        self.flage=0

    def addColier(self):
         pass

    def judgeControl(self):
        pass

    def actionOnce(self):
        if self.flage==0:
            self.addColier()
            self.flage=1

    def action(self):
        self.actionOnce()
        self.judgeControl()



class ReadDataFromDataBase:
    '''
    从数据库中读取关卡信息的工具类。
    '''
    def __init__(self,DataBaseName,TabelName):
        '''

        :param DataBaseName: 要读取的数据库名称
        '''
        self.DataBaseName=DataBaseName
        # 连接数据库
        stringToRead='select * from '+ TabelName
        ConnectMysql.ConnectMysql(DataBaseName)
        self.result=ConnectMysql.SelectData(stringToRead)  # result为一个元组，元组单元为字典结构
        #用于存储自动生成的GameObject对象的数据结构
        self.GameObjects=[]

    # 由字典对象得到Resource类
    def getresourceUnit(self, dict):
        '''

        :param dict: 要传入一个字典对象，来自于数据库
        :return: Resource对象
        '''
        image = pygame.image.load(dict['hunter_imagefilename'])
        location_x = dict['location_X']
        location_y = dict['location_Y']
        # 获取长度
        lengthx = dict['lengthx']
        lengthy = dict['lengthy']
        re = Resource(image, (location_x, location_y), (0, 0), (lengthx, lengthy))
        return re



    #非脚本控制版本，【内部重写版本】
    def getResources(self):
        '''
        1，遍历数据表，构建resource类
        2，构成resources列表
        :return: 资源的列表。
        '''
        Resources=[]
        for x in self.result:
            re=self.getresourceUnit(x)
            #print information
            print(x['hunter_imagefilename'],end='')
            print('--------',end='')
            print(x['location_X'],end='')
            print(',',end='')
            print(x['location_Y'],end='')
            print('.')
            Resources.append(re)
        return Resources



    #自动读取版本
    def createGameObjects(self,surface,camera):
        '''
        1，遍历result元组
        2，由索引逐步建立一级GameObject，建立二级GameObject对像字典
        3，根据碰撞体值 建立 碰撞体对象  ， 并绑定对象
        :param surface:  画布对象
        :param camera:   摄像机对象
        :return:        自动生成的GameObject列表,Colider列表
        '''
        GameObjects=[]
        Coliders=[]
        for x in self.result:
            if (x['hunter_fatherindex']==None) and (x['hunter_iscolider']==0):
                #由资源类以及Camera类创建GameObject对象
                #建立一级resources元组
                resources=[]
                re=self.getresourceUnit(x)
                resources.append(re)
                gb=GameObject(camera,resources,surface)
                GameObjects.append(gb)
            if x['hunter_fatherindex']!=None:
                i=x['hunter_fatherindex']
                re=self.getresourceUnit(x)
                GameObjects[i].resources.append(re)

            if x['hunter_iscolider']!=0:
                gbfather=GameObjects[x['hunter_fatherindex']]
                colider=Colider(gbfater)
                Coliders.append(colider)
        return GameObjects,Coliders



#创建一种标准组件固定型Colider，自带绘制功能，并且能和传入的Colider相检测
'''
矩形
颜色
碰撞
'''
class StandardColider(Colider):
    def __init__(self,point,size,color,camera,paintsurface):
        '''

        :param point: 绘制的逻辑位置
        :param size:  矩形的大小
        :param color: 颜色
        '''
        self.point=point
        self.color=color
        self.size=size
        self.camera=camera
        self.paintsurface=paintsurface

        #绘制坐标
        self.PaintPointx=100
        self.PaintPointy=100
        self.Coliders=[]      #用于碰撞检测的Coliders

        self.fleft=self.point[0]
        self.ftop=self.point[1]
        self.fright=self.fleft+size[0]
        self.fbottom=self.ftop+size[1]


    #一个填充的矩形
    def drawColider(self):
        pygame.draw.rect(self.paintsurface,self.color,(self.PaintPointx,self.PaintPointy,self.size[0],self.size[1]))


    #求资源绘制坐标函数
    def getdrawpoint(self):
        '''
        由资源的逻辑坐标求出绘制坐标
        :return: None
        '''
        self.PaintPointx = self.camera.paintPointx+(self.point[0]-self.camera.logicPointx)
        self.PaintPointy = self.camera.paintPointy+(self.point[1]-self.camera.logicPointy)

    def action(self):
        self.getdrawpoint()
        self.drawColider()


#竖直空气墙，线性碰撞体
class LineColider(Colider):
    def __init__(self,point,size,models):
        '''

        :param point: 起始点：逻辑坐标
        :param size:  长度
        :param models: 模式：1，水平'H'    2，垂直 'V'
        '''
        self.point=point
        self.size=size
        self.models=models

    def getColiderStatus(self,Colider):
        '''
        :param gameObject:  传入的矩形碰撞体类
        :return:  True Or False
        '''
        if self.models=='V':
            if self.point[0]>=Colider.fleft and self.point[0]<=Colider.fright:
                middle_self=(self.point[1]+self.point[1]+self.size)/2
                middle_Colier=(Colider.ftop+Colider.fbottom)/2
                Raduis_self=(self.size)/2
                Raduis_Colider=abs((Colider.ftop-Colider.fbottom)/2)
                if abs(Raduis_Colider+Raduis_self)>=abs(middle_Colier-middle_self):
                    return True
            return False

        if self.models=='H':
            if self.point[1]>=Colider.ftop and self.point[1]<=Colider.fbottom:
                middle_self=(self.point[0]+self.size)/2
                middle_Colier=(Colider.fleft+Colider.fright)/2
                Raduis_self=(self.size)/2
                Raduis_Colider=abs((Colider.fleft-Colider.fright)/2)
                if abs(Raduis_Colider-Raduis_self)<=abs(middle_Colier-middle_self):
                    return True
            return False


def getRandomMap(bottom,RxRange,RyRange,counts,camera,surface):
    '''

    :param bottom: 底部坐标
    :param RxRange: （Rxmin，Rxmanx）
    :param RyRange: （Rymin，Ryman）
    :param counts:  数目
    :return:  list[]    StandardColider类型  和 LineColiders list
    '''
    Rx=[]
    Ry=[]
    Distance=[]
    left=[]
    top=[]
    lengthx=[]
    S_lengthx=[]
    lengthy=[]

    StandardColiders=[]
    LineColiders=[]

    for x in range(0,counts-1):
        Rx.append(random.randint(RxRange[0],RxRange[1]))
        Ry.append(random.randint(RyRange[0],RyRange[1]))
        Random1=random.randint(0,1)
        if Random1==0:
            Distance.append(0)
        if Random1==1:
            Distance.append(150)   #陷阱距离


    S=0
    for x in range(0,counts-1):
        S=S+Rx[x]+Distance[x]
        S_lengthx.append(S)


    for x in range(0,counts-1):
        if x==0:
            left.append(0)
        if x!=0:
            left.append((0+S_lengthx[x-1]))

    for x in range(0,counts-1):
        top.append(bottom-Ry[x])
        lengthx.append(Rx[x])
        lengthy.append(Ry[x])

    for x in range(0, counts - 1):
        colider=StandardColider((left[x],top[x]),(lengthx[x],lengthy[x]),Color(205,133,63),camera,surface)
        StandardColiders.append(colider)

    for x in range(0,counts-1):
        lineColider_left=LineColider((left[x],top[x]+10),lengthy[x],'V')
        LineColiders.append(lineColider_left)

    for x in range(0,counts-1):
        lineColider_right=LineColider((left[x]+lengthx[x],top[x]+10),lengthy[x],'V')
        LineColiders.append(lineColider_right)
        print(left[x]+lengthx[x],end=' ')
        print(top[x]+10,end=' ')
        print(lengthy[x])
    return  StandardColiders,LineColiders



#力对象
class Force:
    def __init__(self,vector2):
        self.vector2=vector2
        self.x=vector2[0]
        self.y=vector2[1]


#刚体组件
class RigidBody:
    '''
    刚体类，实现一切物理效果，与GmeObject绑定
    默认力的方向作用于质心上。
    '''
    def __init__(self,gameObject):
        '''
        :param gameObject: 绑定的 GameObject对象
        '''
        self.gameObject=gameObject

        self.mass=None   #质量
        self.location=None  #位置
        self.size=None   #大小

        self.rotation_angel=0    #目前的角度, 弧度制

        self.vecity_x=0#速度
        self.vecity_y=0

        self.acce_x=0  #加速度
        self.acce_y=0

        self.angleV=0  #角速度
        self.angleAcce=0  #角加速度
        self.centriod=None  #质心位置
        self.Forces=[]   #作用力列表
        self.Torques=[]    #力矩列表
        self.I=100           #伪转动惯量
        self.deltaTime=1/60   #单位时间长度

    def AddForce(self,vector2):
        '''
        :param vector2: 力的向量
        :return:
        '''
        force=Force(vector2)
        self.Forces.append(force)

    def runUpdate(self):
        '''
        每一桢运行一次的函数，用于力的运算
        1，运算，加速度，角加速度
        2，运算，速度，角速度
        3，更新坐标与旋转
        '''
        #1
        for force in self.Forces:
            acce1=force.x/self.mass
            self.acce_x+=acce1
            acce2=force.y/self.mass
            self.acce_y+=acce2

        for x in self.Torques:
            angeAcce=x/self.I
            self.angleAcce+=angeAcce
        #2
        deltaV_x=self.acce_x*self.deltaTime
        self.vecity_x+=deltaV_x

        deltaV_y=self.acce_y*self.deltaTime
        self.vecity_y+=deltaV_y

        deltaAngelV=self.angleAcce*self.deltaTime
        self.angleV+=deltaAngelV

        #3
        self.location[0]+=self.vecity_x*self.deltaTime
        self.location[1]+=self.vecity_y*self.deltaTime

        self.rotation_angel+=self.angleV*self.deltaTime

    def UpdateGameObect(self):
        '''
        更新与之绑定的GameObject对像的属性，需要重写
        :return:
        '''
        pass

    def action(self):
        self.runUpdate()
        self.UpdateGameObect()


#test code
''''
db=ReadDataFromDataBase("hunter","hunter_1")
db.getResources()'''

'''camera=Camera((0,0) ,(0,0))
surface=1
#test 自动生成gameObjects代码
GameObjects,Coliders=db.createGameObjects(surface,camera)

for x in GameObjects:
    print(x)'''

#为sence_now对象赋值
sence_now=Sence('sence_now')



