'''
改造方法；
1，runscript化
2，控制器--动画标识   控制器改变动画状态  -------绘制函数中每一帧监听动画状态，并播放相应的动画
    静止，跳跃，移动，蹲下
'''
#! python3

from GameFrame import *
#########################
pygame.init()

FPS=60
fpsClock=pygame.time.Clock()    #时钟对象
DISPLAYSURF=pygame.display.set_mode((800,600),0,32)
pygame.display.set_caption('Game Frame')
WHITE=(255,255,255)

#############################################
#建立摄像机类资源
camera1=Camera((400,300),(400,300))
#建立资源类
#导入资源
headres = pygame.image.load('head.png')#导入头部资源
manhead = Resource(headres,(400,300),(100,100),(200,200)) #建立资源时，只需要建立初始的值就行了
characterRes=[]          #头部资源数组
characterfootname=[]    #足部资源名称数组
manresources=[]   #人物的资源类数组
manresources.append(manhead)
for x in range(1,8):
    characterfootname.append('man'+' '+'('+str(x)+')'+'.png')

for x in range(0,7):
    characterRes.append(pygame.image.load(characterfootname[x]))
for x in characterRes:
    manresources.append(Resource(x,(420,345),(100,120),(200,200)))

#HP条类：
class HPstatus:
    def __init__(self,surface,point,gameObject):
        '''
        :param surface: 画布对象
        :param point:   起始点
        '''
        self.surface=surface
        self.pointx=point[0]
        self.pointy=point[1]
        self.runOnce()
        self.gameObject=gameObject  #与Hp对象绑定的GameObject对象
        self.color=Color(250,128,114)
    def runOnce(self):
        #加载图片与字体:
        self.image=pygame.image.load('HP.PNG')
        self.titleNumber=pygame.font.Font('Microsoft yahei.ttf',20)
    def runScript(self):
        #根据当前血量建立绘制矩形与文字
        lengthx=(self.gameObject.HP/100)*200
        lengthy=5
        titlesurface_number=self.titleNumber.render(str(self.gameObject.HP),True,self.color)
        pygame.draw.rect(self.surface,Color(250,128,114),(self.pointx+50,self.pointy+10,lengthx,lengthy+6))
        self.surface.blit(self.image,(self.pointx,self.pointy))
        self.surface.blit(titlesurface_number,(self.pointx+80+lengthx,lengthy+6))
    def action(self):
        self.runScript()

#游戏开始场景
class Sence_start(Sence):
    '''
    1，游戏背景图片
    2，绘制logo： 追猎者
    3，绘制button：Play
    4，更换场景
    '''
    surface=None
    def runOnce(self):
        #加载资源
        self.background_image=pygame.image.load('background_start.jpg')
        self.logo_image=pygame.image.load('logo.PNG')
        self.play_image=pygame.image.load('play.PNG')

    #获取点击信息
    def getRect_Clicked(self,mousex,mousey):
        if mousex>=350 and mousex<=450 and mousey>=350 and mousey<=450:
            return self.play_image

    def runScripts(self):
        self.surface.blit(self.background_image,(0,0))
        self.surface.blit(self.logo_image,(280,150))
        self.surface.blit(self.play_image,(350,350))

        #事件监听
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.event.post(event)
            if event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                rect=self.getRect_Clicked(mousex,mousey)
                if rect==self.play_image:
                    global sence_now
                    sence_now=getGameSence()

#死亡场景
class Sence_died(Sence):
    '''
    死亡场景：
    绘制label：you have died
    绘制button：重新开始，退出游戏
    '''
    surface=None  #画布对象

    def runOnce(self):
        #加载内容
        self.titleFont=pygame.font.Font('Microsoft yahei.ttf',100)
        self.titleFont2=pygame.font.Font('Microsoft yahei.ttf',50)
        self.titleSurf_label=self.titleFont.render('you GO DIE!!',True,Color(220,20,60))
        self.titleSurf_button1=self.titleFont2.render('begin again',True,Color(184,134,11))
        self.titleSurf_button2 = self.titleFont2.render('exit game', True, Color(184,134,11))
        #加载场景背景图片：
        self.backgroundImage=pygame.image.load('background.jpg')

    #判定被点击的矩形对象
    def getRect_Clicked(self,mousex,mousey):
        if mousex > 250 and mousex < 800 and mousey > 250 and mousey < 350:
            return self.titleSurf_button1
        if mousex > 250 and mousex < 800 and mousey > 350 and mousey < 450:
            return self.titleSurf_button2

    def runScripts(self):
        #添加绘制代码
        self.surface.blit(self.backgroundImage,(0,0))
        self.surface.blit(self.titleSurf_label,(100,100))
        self.surface.blit(self.titleSurf_button1,(250,250))
        self.surface.blit(self.titleSurf_button2,(270,350))

        #事件判定
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.event.post(event)
            if event.type==MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                #判定哪一个矩形被点击了
                rect=self.getRect_Clicked(mousex,mousey)
                if rect==self.titleSurf_button1:
                    global  sence_now
                    sence_now=getGameSence()

                if rect==self.titleSurf_button2:
                    print('tui chu')
                    pygame.quit()
                    sys.exit()

#胜利场景
class Sence_vicitory(Sence_died):
    surface=None
    def runOnce(self):
        #加载内容
        self.titleFont=pygame.font.Font('Microsoft yahei.ttf',100)
        self.titleFont2=pygame.font.Font('Microsoft yahei.ttf',50)
        self.titleSurf_label=self.titleFont.render('VICITORY!!',True,Color(220,20,60))
        self.titleSurf_button1=self.titleFont2.render('begin again',True,Color(184,134,11))
        self.titleSurf_button2 = self.titleFont2.render('exit game', True, Color(184,134,11))
        #加载场景背景图片：
        self.backgroundImage=pygame.image.load('vicitory.jpg')
#子弹类
class Bullet(GameObject):
    x=0
    y=0   #初始逻辑位置
    x_now=0
    y_now=0   #实时的逻辑位置
    vectiy=20
    distanceToDestory=500
    isDied=False   #是否应该消亡的标识
    toward='left'
    def runScripts(self):
        #更新坐标
        if self.toward=='left':
            if self.x-self.x_now>=self.distanceToDestory:
                self.isDied=True
        if self.toward=='right':
            if self.x_now-self.x>=self.distanceToDestory:
                self.isDied=True
        #绘制方法
        if self.toward == 'left':
            self.paintsurface.blit(self.resources[0].resource,
                                   (self.resources[0].paintPointx, self.resources[0].paintPointy))
            self.x_now-=self.vectiy
        if self.toward=='right':
            self.paintsurface.blit(self.resources[0].resource,
                                   (self.resources[0].paintPointx+40, self.resources[0].paintPointy))
            self.x_now+=self.vectiy
        self.resources[0].logicPointx=self.x_now
        self.resources[0].logicPointy=self.y_now

#建立地形类Sence1
class Sence_terrain(GameObject):
    '''
    地形类
    '''
    def drawGameObject(self):
        '''
        绘制地形
        :return:
        '''
        for x in self.resources:
            if x.bool==True:
                self.paintsurface.blit(x.resource,(x.paintPointx,x.paintPointy))

#建立应用于底层的碰撞体类
class Colider_terrain(Colider):
    lengthx=1000
    lengthy=200
    fleft=None
    fright=None
    ftop=None
    fbottom=None

    def __init__(self):
        print('初始化')
        self.fleft = 200
        self.ftop = 610
        self.fright = self.fleft + self.lengthx
        self.fbottom = self.ftop + self.lengthy
        print(self.fleft)
        print(self.fright)
        print(self.ftop)
        print(self.fbottom)

    #更新矩形数据
    def judgeControl(self):
        self.fleft = 200
        self.ftop = 610
        self.fright = self.fleft + self.lengthx
        self.fbottom = self.ftop + self.lengthy

#建立man 的 gameobject对象
class mancharacter(GameObject):
    drawflage=1
    manx=400
    many=400
    manlocation=(manx,many)
    manspeed=3
    #TWARD=('left','right','stop')
    tward='stop'
    toward='left'
    animation=None
    loactionForStore=None
    #第二动画状态机
    animation2='stay'
    animation3=None

    bullets=[]   #存储子弹对象的列表
    bullet1=None
    image1 = pygame.image.load('shoot.PNG')
    ResourcesForAttack_close=[]   #用于近战攻击的资源类
    drawflage_attackclose=0

    timewaitflag_close=False
    time1_close=0
    time2_close=0
    HP=100   #血量
    #在此函数中加载近战攻击资源
    def runOnce(self):
        images=[]
        for x in range(1,8):
            images.append(pygame.image.load('attack_close'+' '+'('+str(x)+')'+'.PNG'))
        for x in range(1,8):
            resource=Resource(images[x-1],(self.manx,self.many),(0,0),(200,200))
            self.ResourcesForAttack_close.append(resource)

    #通过manlocation计算各个资源的逻辑坐标  初始定位
    def location_sources(self):
        for resource in self.resources:
            if resource==self.resources[0]:
                resource.logicPointx=self.manx
                resource.logicPointy=self.many

            else:
                resource.logicPointx=self.manx+20
                resource.logicPointy=self.many+45


    #重写控制器
    def operateControl(self):
        for event in pygame.event.get():
            if event.type==KEYDOWN:
                if event.key in (K_LEFT,K_a):
                    self.tward='left'
                    self.toward='left'
                    self.animation2='left'
                    self.manx-=self.manspeed
                if event.key in (K_RIGHT,K_d):
                    self.tward='right'
                    self.toward='right'
                    self.animation2='right'
                    self.manx+=self.manspeed
                #跳跃动画
                if event.key == (K_SPACE):
                    self.animation='jump_start'
                #子弹动画
                if event.key==(K_j):
                    self.animation3='shoot'
                    self.timewaitflag_close = False
                #近战攻击动画
                if event.key==(K_k):
                    self.animation3='attack_close'
            if event.type==KEYUP:
                if event.key in (K_LEFT,K_a):
                    self.tward='stop'
                    self.animation2='stay'
                if event.key in (K_RIGHT,K_d):
                    self.tward='stop'
                    self.animation2='stay'
                if event.key in (K_j,):
                    self.animation3=None

            if event.type==QUIT:
                ###################################
                pygame.event.post(event)

    #方向—坐标控制函数
    def tward_point(self):
        if self.tward=='right':
            self.manx+=self.manspeed
        if self.tward=='left':
            self.manx-=self.manspeed
        if self.tward=='stop':
            self.manx=self.manx

    def controlCamera(self):
        #更新摄像机的位置
        self.camera.logicPointx=self.manx
        self.camera.logicPointy=self.many
    #脚本
    def runScripts(self):
        '''
        加入状态机等脚本
        :return:
        '''
        self.controlCamera()
        if self.animation=='jump_start':
            #记录many初值
            self.loactionForStore=self.many
            self.animation='jump'
        if self.animation=='jump':
            self.many-=8

        if self.animation2=='left':
            self.toward='left'
            # 重载drawGameObject方法
            # 绘制头部
            # print(self.resources[0].bool)
            if self.resources[0].bool == True:
                #print('绘制头部')
                self.paintsurface.blit(self.resources[0].resource,
                                       (self.resources[0].paintPointx, self.resources[0].paintPointy))
            # 绘制脚部的动画
            '''timecontrol函数需要改进，开辟独立线程或者包含可以中断挂起，很简单，多动画状态机'''
            if self.timecontrol(5):
                #print('绘制脚步')
                self.paintsurface.blit(self.resources[self.drawflage].resource, (
                self.resources[self.drawflage].paintPointx, self.resources[self.drawflage].paintPointy))
                self.drawflage += 1

            self.paintsurface.blit(self.resources[self.drawflage].resource, (
            self.resources[self.drawflage].paintPointx, self.resources[self.drawflage].paintPointy))
            if self.drawflage == 6:
                self.drawflage = 1

        #右方动画
        if self.animation2=='right':
            self.toward='right'
            if self.resources[0].bool == True:
                # print('绘制头部')
                self.paintsurface.blit(pygame.transform.flip(self.resources[0].resource,True,False),
                                       (self.resources[0].paintPointx, self.resources[0].paintPointy))
            # 绘制脚部的动画
            '''timecontrol函数需要改进，开辟独立线程或者包含可以中断挂起，很简单，多动画状态机'''
            if self.timecontrol(5):
                # print('绘制脚步')
                self.paintsurface.blit(pygame.transform.flip(self.resources[self.drawflage].resource,True,False), (
                    self.resources[self.drawflage].paintPointx-18, self.resources[self.drawflage].paintPointy))
                self.drawflage += 1

            self.paintsurface.blit(pygame.transform.flip(self.resources[self.drawflage].resource,True,False), (
                self.resources[self.drawflage].paintPointx-18, self.resources[self.drawflage].paintPointy))
            if self.drawflage == 6:
                self.drawflage = 1


        if self.animation2=='stay':
            if self.toward=='left':
                #绘制静态动画并且重置timecontrol方法
                if self.resources[0].bool==True:
                    self.paintsurface.blit(self.resources[0].resource,(self.resources[0].paintPointx,self.resources[0].paintPointy))
                    self.paintsurface.blit(self.resources[3].resource, (
                    self.resources[3].paintPointx, self.resources[3].paintPointy))
                self.resetTimeControl()

            if self.toward=='right':
                if self.resources[0].bool==True:
                    self.paintsurface.blit(pygame.transform.flip(self.resources[0].resource,True,False),(self.resources[0].paintPointx,self.resources[0].paintPointy))
                    self.paintsurface.blit(pygame.transform.flip(self.resources[3].resource,True,False),(
                    self.resources[3].paintPointx, self.resources[3].paintPointy))
                self.resetTimeControl()

        #子弹动画脚本
            '''
            1，创建一个子弹对象（包含位置信息，消减距离）
            2，遍历子弹对象列表，进行贴图
            3，更新子弹对象信息'''

        if self.animation3=='shoot':
            bulletresource=Resource(self.image1, (self.manx, self.many+30), (0, 0), (10, 10))
            BulletNow=Bullet(self.camera,[bulletresource,],self.paintsurface)
            #更改其初值
            BulletNow.x=self.manx
            BulletNow.y=self.many+30
            BulletNow.x_now=self.manx
            BulletNow.y_now=self.many+30
            if self.toward=='left':
                BulletNow.toward='left'
            if self.toward=='right':
                BulletNow.toward='right'

            self.bullets.append(BulletNow)
            #重置timeControl_attackclose函数
            self.timewaitflag_close=False

        #更新近战攻击资源的逻辑坐标
        for resource1 in self.ResourcesForAttack_close:
            resource1.logicPointx=self.manx
            resource1.logicPointy=self.many

        #更新近战攻击资源的绘制坐标
        for resource1 in self.ResourcesForAttack_close:
            resource1.paintPointx = self.camera.paintPointx+(resource1.logicPointx-self.camera.logicPointx)
            resource1.paintPointy = self.camera.paintPointy+(resource1.logicPointy-self.camera.logicPointy)

        #近战攻击动画
        #1，白色矩形遮盖
        #2，绘制近战攻击动画
        if self.animation3=='attack_close':
            if self.toward=='left':
                pygame.draw.rect(self.paintsurface,Color(255,255,255,255),(self.resources[0].paintPointx,self.resources[0].paintPointy,100,40),0)
                if self.timecontrol_AttackClose(3):
                    '''动画转换问题会带来时间控制函数崩溃，所以必须要进行reset'''
                    self.paintsurface.blit(self.ResourcesForAttack_close[self.drawflage_attackclose].resource,(self.ResourcesForAttack_close[self.drawflage_attackclose].paintPointx,self.ResourcesForAttack_close[self.drawflage_attackclose].paintPointy))
                    self.drawflage_attackclose+=1

                self.paintsurface.blit(self.ResourcesForAttack_close[self.drawflage_attackclose].resource, (
                        self.ResourcesForAttack_close[self.drawflage_attackclose].paintPointx,
                        self.ResourcesForAttack_close[self.drawflage_attackclose].paintPointy))
                if self.drawflage_attackclose == 6:
                    self.drawflage_attackclose = 0
                    self.animation3=None
            if self.toward=='right':
                pygame.draw.rect(self.paintsurface, Color(255, 255, 255, 255),
                                 (self.resources[0].paintPointx, self.resources[0].paintPointy, 100, 40), 0)
                if self.timecontrol_AttackClose(3):
                    self.paintsurface.blit(pygame.transform.flip(self.ResourcesForAttack_close[self.drawflage_attackclose].resource,True,False), (
                    self.ResourcesForAttack_close[self.drawflage_attackclose].paintPointx,
                    self.ResourcesForAttack_close[self.drawflage_attackclose].paintPointy))
                    self.drawflage_attackclose += 1

                self.paintsurface.blit(pygame.transform.flip(self.ResourcesForAttack_close[self.drawflage_attackclose].resource,True,False), (
                    self.ResourcesForAttack_close[self.drawflage_attackclose].paintPointx,
                    self.ResourcesForAttack_close[self.drawflage_attackclose].paintPointy))
                if self.drawflage_attackclose == 6:
                    self.drawflage_attackclose = 0
                    self.animation3 = None
        #遍历运行脚本
        for bullet in self.bullets:
            bullet.action()

        #删除死亡的目标
        for bullet in self.bullets:
            if bullet.isDied==True:
                self.bullet1=bullet

        if self.bullet1!=None:
            self.bullets.remove(self.bullet1)
            self.bullet1=None
        self.judgeIsDied()

    def judgeIsDied(self):
        #判定时否死亡
        if self.many>=1500 or self.HP<=0:
            global  sence_now
            sence_now=sence_died1
    #重写时间控制函数——近战攻击版本
    def timecontrol_AttackClose(self,delaystep):
        if self.timewaitflag_close == False:
            self.time1_close=self.step
            self.timewaitflag_close=True
        self.time2_close=self.step
        if self.time2_close-self.time1_close==delaystep:
            self.timewaitflag_close=False
            return True
        return False
    #重写action
    def action(self):
        self.location_sources()
        self.operateControl()
        self.tward_point()
        #####################################
        GameObject.action(self)
        #####################################

#建立man 的 colider对象
class manColider(Colider):
    '''
    实现功能，简单矩形与矩形碰撞检测，函数实现
    重力功能
    '''
    #属性定义
    lengthx=80
    lengthy=80
    location=None
    locationbuffer=None
    useGravity=False
    fleft=None
    fright=None
    ftop=None
    fbottom=None
    ToAdd=100
    LineJugeColiders=[]   #不在初始化函数中的变量会在不同实例中公有 ，内存陷阱
    vecity=2

    def addColier(self):
        '''
        一次性执行函数
        :return:
        '''
        self.location=(self.GameObject.manx,self.GameObject.many)
        #矩形对象的所有参数：
        self.fleft = self.GameObject.manx
        self.ftop = self.GameObject.many
        self.fright = self.fleft + self.lengthx
        self.fbottom = self.ftop + self.lengthy

        print(self.fleft)
        print(self.fright)
        print(self.ftop)
        print(self.fbottom)
    #update函数
    def judgeControl(self):
        '''
        1,矩形判定
        :return:
        '''
        self.fleft = self.GameObject.manx
        self.ftop = self.GameObject.many
        self.fright = self.fleft + self.lengthx
        self.fbottom = self.ftop + self.lengthy
        for x in self.judgeColider:
            self.locationbuffer = self.location
            if self.rectTest(x):
                if self.rectTestV(x):
                    self.location = self.locationbuffer
                    self.GameObject.many = self.location[1]
                    self.vecity=2
                    self.GameObject.animation=None
        for x in self.LineJugeColiders:
            self.locationbuffer=self.location
            if x.getColiderStatus(self):
                print(x.getColiderStatus(self))
                self.location=self.locationbuffer
                self.GameObject.manx=self.location[0]

    def rectTest(self,colider):
        '''
        :param colider: 传入的colider对象
        :return: bool  True:碰撞   False:失败
        '''
        if(self.fright>=colider.fleft) and (self.fleft<=colider.fright):
            if(self.fbottom>=colider.ftop) and (self.ftop<=colider.fbottom):
                return True
        return False

    #水平面的碰撞判定：
    def rectTestH(self,colider):
        if (self.fright >= colider.fleft) and (self.fleft <= colider.fright):
            return True
        return False

    #垂直面的碰撞判定：
    def rectTestV(self,colider):
        if (self.fbottom >= colider.ftop) and (self.ftop <= colider.fbottom):
            return True
        return False

    def runColider(self):
        #不包含速度变量的伪重力

        if self.useGravity:
            self.GameObject.many+=self.vecity

    def action(self):
        self.actionOnce()
        self.runColider()
        self.judgeControl()
        #更新locaiton
        self.location=(self.GameObject.manx,self.GameObject.many)
        self.vecity+=0.1

#建立基于运算检测的 FireFormSky类
class FireFromSky(GameObject):
    '''
    1，在runOnce函数中建立资源
    2，随机逻辑位置开始下落
    3，runscripts函数中进行击中检测，关联到man对象的hp属性
    '''
    def __init__(self,camera,paintsurface,mans):
        self.camera=camera
        self.resources=[]
        self.paintsurface=paintsurface
        self.timewaitflag=False
        self.time1=0
        self.time2=0
        self.step = 0
        self.pointx=0
        self.pointy=0
        self.vecity=2

        self.power_changed=True   #一个FIRE在自己的历程中只能造成一次伤害

        self.mans = mans  # 要进行击中检测的对象列表
        self.runOnce()

        # 在外部定义方法传入script属性，直接对GameObject进行控制（支持在外部进行控制）
        self.script = lambda self: None  # 给一个默认值

        self.distanceToDied=2000#销毁距离
        self.isDied=False

        self.ChildGameObject=[]
    def runOnce(self):
        image=pygame.image.load('fire.PNG')
        #获取随机位置
        x=random.randint(self.mans[0].manx-2000,self.mans[0].manx+2000)
        y=-200
        self.pointx=x
        self.pointy=y
        resouce=Resource(image,(x,y),(0,0),(20,100))
        self.resources.append(resouce)

    def drawGameObject(self):
        self.paintsurface.blit(self.resources[0].resource,(self.resources[0].paintPointx,self.resources[0].paintPointy))

    def runScripts(self):
        self.resources[0].logicPointx=self.pointx
        self.resources[0].logicPointy=self.pointy
        for x in self.mans:
            if self.pointy<=x.many+200:
                if self.pointy>=x.many and self.pointx>(x.manx-40) and self.pointx<(x.manx+40) and self.power_changed:
                    x.HP-=10   #掉血
                    self.power_changed=False
        #自我坐标移动
        self.pointy+=self.vecity
        self.vecity+=0.1
        if self.vecity>=5:
            self.vecity=5
        #死亡判定
        if self.pointy>=self.distanceToDied:
            self.isDied=True

#生成并销毁FireFromSky的函数
def GetFires(camera,surface,mans):
    GetNewFire=False
    x=random.randint(1,30)
    if x<=4:
        GetNewFire=True
    if GetNewFire:
        return FireFromSky(camera,surface,mans)
    return None



#第二角色的建立;AI角色
class AI_Character(mancharacter):

    '''
    有限状态机原理
    状态1：duck_colider    (闪避障碍）
    状态2：火焰对npc没有用，duck_deep（闪避深渊）,escape（逃离）,hunt（追逐）
    状态3：发射子弹 shoot
    状态4: kill      （秒杀）
    '''
    status_1=None
    status_2=None
    status_3=None
    status_4=None
    status_5='idle'   #普通状态
    #用于ai判定的地图数据
    StandardColiders=[]
    LineColiders=[]
    Play1=None    #玩家对象
    toward = 'left'
    manspeed = 1.5
    def controlCamera(self):
        pass
    def judgeIsDied(self):
        if self.HP<=0:
            global  sence_now
            sence_now=sence_vicitory1
    #触发-切换状态
    def Trigger(self):
        #1,
        self.status_1=None
        if self.toward=='left':
            x_new=self.manx-150
            for x in self.LineColiders:
                if (self.manx>x.point[0]) and (x_new<=x.point[0]):
                    #print('come on')
                    self.status_1='duck_colider'
        if self.toward=='right':
            #print(self.toward)
            x_new=self.manx+150
            #print(x_new)
            #print('---')
            for x in self.LineColiders:

                #print(x.point[0])
                if (self.manx<x.point[0]) and (x_new>=x.point[0]):
                    self.status_1='duck_colider'
                    #print(self.status_1)
            #print('---')

        #2
        self.status_2=None
        #判定前方是否有深渊
        #判断当下处于那一个碰撞体的位置
        index=-1
        indexForCount=0    #length for
        for x in self.StandardColiders:
            indexForCount+=1
        for x in self.StandardColiders:
            index+=1
            if self.toward=='left':
                if (self.manx>=x.fleft) and (self.manx<=x.fright):
                    #判断前方是否有深渊
                    if index==0:
                        self.status_2='duck_deep'
                    if index>0:
                        if self.StandardColiders[index-1].fright<x.fleft:
                            self.status_2='duck_deep'
            if self.toward=='right':
                if (self.manx>=x.fleft) and (self.manx<=x.fright):
                    if index==indexForCount-1:
                        self.status_2=='duck_deep'
                    if index<indexForCount-1:
                        if x.fright<self.StandardColiders[index+1].fleft:
                            self.status_2='duck_deep'

        if (self.Play1.HP-self.HP>=10) or ((self.Play1.HP>self.HP) and (self.HP<=10)):
            self.status_2='escape'
        if (self.HP-self.Play1.HP>=10) or ((self.Play1.HP<self.HP) and (self.Play1.HP<=10)):
            self.status_2='hunt'


        #3
        self.status_3=None
        if self.status_2=='hunt':
            self.status_3='shoot'

        #4
        self.status_4=None
        if self.status_2=='hunt':
            if self.toward=='left':
                if self.manx-self.Play1.manx<=100:
                    self.status_4='kill'
            if self.toward=='right':
                if self.Play1.manx-self.manx<=100:
                    self.status_4='kill'

        if  self.status_5=='idle':
            # 更新朝向
            if self.Play1.manx >=self.manx+50:
                self.toward = 'right'
            if self.manx > self.Play1.manx+50:
                self.toward = 'left'

        if (self.status_1==None) and (self.status_2==None) and (self.status_3==None) and (self.status_4==None):
            self.status_5='idle'

    #状态执行
    def runAiFunction(self):
        if self.Play1.animation3=='attack_close' and (self.Play1.HP-self.HP>=10):
            if (abs(self.Play1.many - self.many) <= 50) and abs(self.manx - self.Play1.manx <= 100):
                self.HP-=50
        if self.Play1.animation3=='shoot':
            if self.manx<=self.Play1.manx:
                if self.Play1.toward=='left':
                    if (abs(self.Play1.many - self.many) <= 50) and abs(self.manx - self.Play1.manx <= 500):
                        self.HP -= 0.5
            if self.manx>self.Play1.manx:
                if self.Play1.toward=='right':
                    if (abs(self.Play1.many - self.many) <= 50) and abs(self.manx - self.Play1.manx <= 500):
                        self.HP -= 0.5

        if self.status_1==None:
            self.animation=None
        if self.status_1=='duck_colider':
            self.animation='jump'
            self.status_5=None
        #if self.status_2=='duck_deep':
            #elf.animation='iump'
            #self.status_5=None
        if self.status_2=='escape':
            #更新朝向
            if self.Play1.manx<self.manx:
                self.toward='right'
            if self.manx<self.Play1.manx:
                self.toward='left'
            self.status_5=None

        if self.status_2=='hunt':
            if self.Play1.manx>self.manx:
                self.toward='right'
            if self.manx>self.Play1.manx:
                self.toward='left'
            self.status_5=None
        #更新移动
        if self.toward=='left':
            self.tward='left'
            self.animation2='left'
            self.manx -= self.manspeed
        if self.toward=='right':
            self.tward='right'
            self.animation2='right'
            self.manx+=self.manspeed

        if self.status_3=='shoot':
            self.animation3='shoot'
            self.timewaitflag_close = False
            self.status_5=None
            if (abs(self.Play1.many - self.many) <= 50) and abs(self.manx - self.Play1.manx <= 500):
                self.Play1.HP -= 0.5
        if self.status_4=='kill':
            self.animation3='attack_close'
            self.status_5=None
            if (abs(self.Play1.many - self.many) <= 50):
                self.Play1.HP-=50

        #调试信息
        '''
        print('status_1',end=' ')
        print(self.status_1)
        print('status_2', end=' ')
        print(self.status_2)
        print('status_3', end=' ')
        print(self.status_3)
        print('status_4', end=' ')
        print(self.status_4)
        print('status_5', end=' ')
        print(self.status_5)
        '''


    def action(self):
        self.location_sources()
        self.operateControl()
        self.tward_point()
        self.Trigger()
        self.runAiFunction()
        #####################################
        GameObject.action(self)
        #####################################

#建立第二角色的HPUI
class HP_AI(HPstatus):
    color=Color(10,0,255)
#游戏场景对象建立的函数
def getGameSence():
    '''
    得到游戏运行场景。
    :return: 场景对象
    '''
    #游戏对象建立
    sence_now=Sence('sence_now')
    man1=mancharacter(camera1,manresources,paintsurface=DISPLAYSURF)

    Colider1=manColider(man1)

    Colider1.useGravity=True

    Coliders,LineColiders=getRandomMap(1000,(100,500),(300,500),20,camera1,DISPLAYSURF)
    sence_now.GameObjects.append(man1)

    Colider1.LineJugeColiders=[]
    for x in Coliders:
        Colider1.judgeColider.append(x)
        sence_now.GameObjects.append(x)
    for x in LineColiders:
        Colider1.LineJugeColiders.append(x)


    sence_now.GameObjects.append(Colider1)

    hp_man1=HPstatus(DISPLAYSURF,(10,10),man1)
    sence_now.GameObjects.append(hp_man1)

    #创建AI角色，以及添加各个信息
    player_AI=AI_Character(camera1,manresources,paintsurface=DISPLAYSURF)
    player_AI.Play1=man1
    player_AI.manx=man1.manx-200
    hp_AI=HP_AI(DISPLAYSURF,(400,10),player_AI)
    hp_AI.color=Color(10,0,255)
    Colider_AI=manColider(player_AI)

    Colider_AI.useGravity=True

    #1,standardCOliders  , LinColiders
    Colider_AI.LineJugeColiders=[]
    for x in Coliders:
        Colider_AI.judgeColider.append(x)
        player_AI.StandardColiders.append(x)
    for x in LineColiders:
        Colider_AI.LineJugeColiders.append(x)
        player_AI.LineColiders.append(x)
    sence_now.GameObjects.append(player_AI)
    sence_now.GameObjects.append(Colider_AI)
    sence_now.GameObjects.append(hp_AI)
    #HP信息
    return sence_now

FireCounts=0
Fires=[]
#开始场景实例
sence_start1=Sence_start('sence_start')
sence_start1.surface=DISPLAYSURF

#死亡场景实例
sence_died1=Sence_died('died')
sence_died1.surface=DISPLAYSURF

#胜利场景实例
sence_vicitory1=Sence_vicitory('sence_vicitory')
sence_vicitory1.surface=DISPLAYSURF
sence_now=sence_start1
while True:

    DISPLAYSURF.fill(WHITE)
    sence_now.action()
    if sence_now.name=='sence_now':
        fire1=GetFires(camera1,DISPLAYSURF,[sence_now.GameObjects[0],])
        UpdateAll=True    #用于更新一波子弹的标识
        for x in Fires:
            if x.isDied==False:
                UpdateAll=False

        if fire1!=None and FireCounts<=20:
            Fires.append(fire1)
            FireCounts+=1
        for x in Fires:
            x.action()
        if FireCounts>=19 and UpdateAll:
            print('clear ALL Fire')
            Fires=[]
            FireCounts=0

    if sence_now.name=='sence_new':
        #将man1_local添加到Fire中
        fire1 = GetFires(camera1, DISPLAYSURF, [sence_now.GameObjects[0], ])
        UpdateAll = True  # 用于更新一波子弹的标识
        for x in Fires:
            if x.isDied == False:
                UpdateAll = False

        if fire1 != None and FireCounts <= 20:
            Fires.append(fire1)
            FireCounts += 1
        for x in Fires:
            x.action()
        if FireCounts >= 19 and UpdateAll:
            print('clear ALL Fire')
            Fires = []
            FireCounts = 0

    for event in pygame.event.get():
        if event.type==QUIT:
            print('tui chu')
            pygame.quit()
            sys.exit()
    pygame.display.update()
    fpsClock.tick(FPS)








