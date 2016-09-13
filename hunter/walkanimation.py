import pygame,sys
from pygame.locals import *

pygame.init()

FPS=30
fpsClock=pygame.time.Clock()    #时钟对象

manx=400
many=200
drawWalkflage=0 #步进程序标识
tward='left'
DISPLAYSURF=pygame.display.set_mode((800,600),0,32)
pygame.display.set_caption('Game Frame')
headres=pygame.image.load('head.png')#导入头部资源
WHITE=(255,255,255)
#动画-行走
#res import
characterRes=[]          #头部资源数组
characterfootname=[]    #足部资源名称数组

for x in range(1,8):
    characterfootname.append('man'+' '+'('+str(x)+')'+'.png')

for x in range(0,7):
    characterRes.append(pygame.image.load(characterfootname[x]))

def drawWalk():
    global DISPLAYSURF
    global drawWalkflage
    DISPLAYSURF.blit(headres,(manx,many))
    DISPLAYSURF.blit(characterRes[drawWalkflage],(manx+18,many+44))
    drawWalkflage+=1
    while drawWalkflage==6:
        drawWalkflage=0
  
      

while True:
    DISPLAYSURF.fill(WHITE)
    if manx==10:
        manx+=10
        tward='right'
        
    if manx==400:
        manx-=10
        tward='left'
    if tward=='left':
        manx-=10
    if tward=='right':
        manx+=10
 

    drawWalk()
    
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
    

    pygame.display.update()
    fpsClock.tick(FPS)
           
