import pygame, sys, math, time, os, random, noise, threading, platform
from pygame.locals import *
pygame.init()
VERSION=0.05
screenObj=pygame.display.Info()
screenW=screenObj.current_w
screenH=screenObj.current_h
screenW,screenH=1200,1000
screen=pygame.display.set_mode((screenW,screenH))#,FULLSCREEN)
pygame.display.set_caption("fegararia v"+str(VERSION))
overworldbkg=pygame.transform.scale(pygame.image.load("Textures/overworldbkg.png"),(screenW,screenH))
playerscale=1
#when saving the following need to be saved:
#Player class
#mapData array
#chest Data array
showHitBoxes=False
def loadMiscIcons():
    global miscIcons
    miscIconTilesheet=pygame.transform.scale(pygame.image.load("Textures/misc.png"),(50,100))
    miscIcons=[]
    for j in range(1):
      for i in range(2):
         surf=pygame.Surface((50,50))
         surf.blit(miscIconTilesheet,(-i*50,-j*50))
         miscIcons.append(surf)
def loadLightingImages():
   specialLightingTilesheet=pygame.transform.scale(pygame.image.load("Textures/special lighting tilesheet.png"),(BLOCKSIZE*16,BLOCKSIZE*16))
   global specialLightingImages
   specialLightingImages=[]
   for j in range(16):
      for i in range(16):
         surf=pygame.Surface((BLOCKSIZE,BLOCKSIZE))
         surf.set_colorkey((255,0,255))
         surf.blit(specialLightingTilesheet,(-i*BLOCKSIZE,-j*BLOCKSIZE))
         specialLightingImages.append(surf)
def loadBirdImages():
   birdTilesheet=pygame.transform.scale(pygame.image.load("Textures/birds.png"),(80,40))
   birdTilesheet.set_colorkey((255,0,255))
   global birdImages
   birdImages=[]
   for j in range(2):
      for i in range(4):
         surf=pygame.Surface((20,20))
         surf.set_colorkey((255,0,255))
         surf.blit(birdTilesheet,(-i*20,-j*20))
         birdImages.append(surf)
def loadItemImages():
   global itemImages  
   itemTilesheet=pygame.transform.scale(pygame.image.load("Textures/itemTilesheet.png"),(int(BLOCKSIZE/1.5*16),int(BLOCKSIZE/1.5*16)))
   itemImages=[]
   for i in range(16):
      for j in range(16):
         surf=pygame.Surface((int(BLOCKSIZE/1.5),int(BLOCKSIZE/1.5)))
         surf.set_colorkey((255,0,255))
         surf.blit(itemTilesheet,(-j*(BLOCKSIZE/1.5),-i*(BLOCKSIZE/1.5)))
         itemImages.append(surf)
def loadHotbarImages():
   global hotbarItemImages
   hotbarItemTilesheet=pygame.transform.scale(pygame.image.load("Textures/itemTilesheet.png"),(576,576))
   hotbarItemImages=[]
   for i in range(16):
      for j in range(16):
         surf=pygame.Surface((36,36))
         surf.set_colorkey((255,0,255))
         surf.blit(hotbarItemTilesheet,(-j*36,-i*36))
         hotbarItemImages.append(surf)
def assembleHotbarBack():
   global hotbarback
   hotbarback=pygame.Surface((610,60))
   pygame.draw.rect(hotbarback,(150,150,150),Rect(0,0,610,60),0)
   for i in range(10):
      pygame.draw.rect(hotbarback,(200,200,200),Rect(i*61,0,60,60),5)
   hotbarback.set_alpha(200)
def assembleAmmunitionBack():
   global ammunitionBack
   ammunitionBack=pygame.Surface((60,240))
   pygame.draw.rect(ammunitionBack,(150,150,150),Rect(0,0,60,240),0)
   for j in range(4):
      pygame.draw.rect(ammunitionBack,(200,200,200),Rect(0,j*61,60,60),5)
   ammunitionBack.set_alpha(200)
def assembleInventoryBack():
   global inventoryback
   inventoryback=pygame.Surface((610,243))
   pygame.draw.rect(inventoryback,(150,150,150),Rect(0,0,610,243),0)
   for i in range(10):
      for j in range(4):
         pygame.draw.rect(inventoryback,(200,200,200),Rect(i*61,j*61,60,60),5)
   inventoryback.set_alpha(200)
def assembleChestBack():
   global chestBack
   chestBack=pygame.Surface((430,240))
   pygame.draw.rect(chestBack,(150,150,150),Rect(0,0,430,240),0)
   for i in range(7):
      for j in range(4):
         pygame.draw.rect(chestBack,(200,200,200),Rect(2+i*61,2+j*59,60,60),5)
   chestBack.set_alpha(200)
def assembleCraftingBack():
    global craftingBack
    craftingBack=pygame.Surface((55,510))
    pygame.draw.rect(craftingBack,(150,150,150),Rect(0,0,55,510),0)
    pygame.draw.rect(craftingBack,(200,200,200),Rect(2,2,51,506),5)
    inventoryback.set_alpha(200)
def loadCharacterAnimation():
   global characterFrames
   characterimages=pygame.transform.scale(pygame.image.load("Textures/player tilesheet.png"),(int(BLOCKSIZE*4*playerscale),int(BLOCKSIZE*4*playerscale)))
   characterimages.set_colorkey((255,0,255))
   characterFrames=[]
   for i in range(2):
      for j in range(4):
         surf=pygame.Surface((BLOCKSIZE*playerscale,BLOCKSIZE*2*playerscale))
         surf.set_colorkey((255,0,255))
         surf.blit(characterimages,(-j*BLOCKSIZE*playerscale,-i*BLOCKSIZE*2*playerscale))
         characterFrames.append(surf)
def loadTileImages():
   global images
   tilesheet=pygame.transform.scale(pygame.image.load("Textures/tilesheet.png"),(BLOCKSIZE*16,BLOCKSIZE*16))
   images=[]
   for j in range(16):
      for i in range(16):
         surf=pygame.Surface((BLOCKSIZE,BLOCKSIZE))
         surf.set_colorkey((255,0,255))
         surf.blit(tilesheet,(-i*BLOCKSIZE,-j*BLOCKSIZE))
         images.append(surf)
def loadBackTileImages():
   global backImages
   backTilesheet=pygame.transform.scale(pygame.image.load("Textures/backTilesheet.png"),(BLOCKSIZE*16,BLOCKSIZE*16))
   backImages=[]
   for j in range(16):
      for i in range(16):
         surf=pygame.Surface((BLOCKSIZE,BLOCKSIZE))
         surf.blit(backTilesheet,(-i*BLOCKSIZE,-j*BLOCKSIZE))
         backImages.append(surf)
class Enemy():
   def __init__(self,pos,enemyType):
      self.pos=pos
      self.vel=(0,0)
      self.type=enemyType
class NPC():
   def __init__(self,pos,NPCtype,vel=(0,0)):
      self.pos=pos
      self.vel=vel
      self.type=NPCtype
   def getCollide(self,handle=True):
      collides=[False,False,False,False]
      blockpos=(math.floor(self.rect.centerx//BLOCKSIZE),math.floor(self.rect.centery//BLOCKSIZE))
      for i in range(3):
         for j in range(3):
            if mapData[blockpos[1]+j-1-CHUNKSIZE][blockpos[0]+i-1-CHUNKSIZE][0]>0:
               blockrect=Rect(BLOCKSIZE*(blockpos[0]+i-1),BLOCKSIZE*(blockpos[1]+j-1),BLOCKSIZE,BLOCKSIZE)
               if blockrect.colliderect(self.rect):
                  deltaX = self.rect.centerx-blockrect.centerx
                  deltaY = self.rect.centery-blockrect.centery
                  if abs(deltaX) > abs(deltaY):
                      if deltaX > 0:
                         collides[2]=True
                         if handle:
                            self.pos=(blockrect.right+self.rect.width/2,self.pos[1])
                            self.vel=(0,self.vel[1])
                      else:
                         collides[0]=True
                         if handle:
                            self.pos=(blockrect.left-self.rect.width/2,self.pos[1])
                            self.vel=(0,self.vel[1])
                  else:
                      if deltaY > 0:
                         collides[3]=True
                         if handle:
                            self.pos=(self.pos[0],blockrect.bottom+self.rect.height/2)
                            if self.vel[1]<0:
                               self.vel=(self.vel[0],0)
                      else:
                         collides[1]=True
                         if handle:
                            self.pos=(self.pos[0],blockrect.top-self.rect.height/2)
                            if self.vel[1]>0:
                               self.vel=(self.vel[0]*0.5,0)
      return collides
   def damage(self,val,crit):
       if crit:col=(255,0,0)
       else:col=(200,100,0)
       damagePopUps.append([val,col,100,(self.pos[0]+random.randint(-20,20),self.pos[1]+30+random.randint(-20,20))])
       self.hp-=val
       if self.hp<=0:
           self.kill()
class bird(NPC):
   def __init__(self,pos,vel):
      global birdNum
      self.rect=Rect(pos[0]-10,pos[1]-10,20,20)
      super().__init__(pos,"bird",vel)
      self.animationFrame=0
      if self.vel[0]>0:
         self.direction=1
      else:
         self.direction=0
      self.animationTick=0
      self.col=random.randint(0,1)
      self.hp=5
      NPCS.append(self)
      birdNum+=1
   def update(self):
      global birdNum
      if self.animationTick<=0:
         self.animationFrame=1
      else:
         self.animationFrame=0
         self.animationTick-=1
      if abs(p.pos[0]-self.pos[0])>screenW:
         birdNum-=1
         NPCS.remove(self)
      collides=self.getCollide()
      if collides[0]:
         self.vel=(-2,self.vel[1])
         self.direction=0
      elif collides[1]:
         self.vel=(self.vel[0],-2)
      elif collides[2]:
         self.vel=(2,self.vel[1])
         self.direction=1
      if self.vel[1]>1:
         self.vel=(self.vel[0],-1)
         self.animationTick=20
      self.vel=(self.vel[0],self.vel[1]+0.05)
      self.pos=(self.pos[0]+self.vel[0],self.pos[1]+self.vel[1])
      self.rect=Rect(self.pos[0],self.pos[1],20,20)
   def draw(self):
      screen.blit(birdImages[self.animationFrame+self.direction*2+self.col*4],(self.pos[0]-CAM.pos[0],self.pos[1]-CAM.pos[1]))
      if showHitBoxes:
          pygame.draw.rect(screen,(255,0,0),Rect(self.rect.left-CAM.pos[0],self.rect.top-CAM.pos[1],self.rect.width,self.rect.height),2)
   def kill(self):
       global birdNum
       birdNum-=1
       NPCS.remove(self)
class WorldItem():
   def __init__(self,name,amnt,pos):
      global worldItems
      self.name=name
      self.tags=getTagsFromName(name)
      self.imgIndex=getItemImgIndex(name)
      self.pos=(pos[0]-BLOCKSIZE/3,pos[1]-BLOCKSIZE/3)
      self.rect=Rect(pos[0]-BLOCKSIZE/3,pos[1]-BLOCKSIZE/3,BLOCKSIZE/1.5,BLOCKSIZE/1.5)
      self.vel=(random.random()*0.5-0.25,random.random()-2)
      self.age=0
      self.amnt=amnt
      worldItems.append(self)
   def update(self):
      global worldItems
      if self.age>10000:
          worldItems.remove(self)
      else:
          self.age+=1
      if p.alive:
          if distance(self.pos,p.pos)<BLOCKSIZE*3:
             self.vel=((p.pos[0]-self.pos[0])/15,(p.pos[1]-self.pos[1])/15)
      self.vel=(self.vel[0],self.vel[1]+0.2)
      self.vel=(self.vel[0]*0.99,self.vel[1]*0.99+0.05)
      if self.vel[1]>5:
         self.vel=(self.vel[0],5)
      self.pos=(self.pos[0]+self.vel[0],self.pos[1]+self.vel[1])
      self.rect.left=self.pos[0]-BLOCKSIZE/3
      self.rect.top=self.pos[1]-BLOCKSIZE/3
      blockpos=(math.floor(self.rect.centerx//BLOCKSIZE),math.floor(self.rect.centery//BLOCKSIZE))
      for i in range(3):
         for j in range(3):
            val=mapData[blockpos[1]+j-1-CHUNKSIZE][blockpos[0]+i-1-CHUNKSIZE][0]
            if val not in uncollidableBlocks:
               blockrect=Rect(BLOCKSIZE*(blockpos[0]+i-1),BLOCKSIZE*(blockpos[1]+j-1),BLOCKSIZE,BLOCKSIZE)
               if blockrect.colliderect(self.rect):
                  deltaX = self.rect.centerx-blockrect.centerx
                  deltaY = self.rect.centery-blockrect.centery
                  if abs(deltaX) > abs(deltaY):
                      if deltaX > 0:
                          self.pos=(blockrect.right+BLOCKSIZE/3,self.pos[1])
                          self.vel=(0,self.vel[1])
                      else:
                          self.pos=(blockrect.left-BLOCKSIZE/3,self.pos[1])
                          self.vel=(0,self.vel[1])
                  else:
                      if deltaY > 0:
                          self.pos=(self.pos[0],blockrect.bottom+BLOCKSIZE/3)
                          if self.vel[1]<0:
                             self.vel=(self.vel[0],0)
                      else:
                         self.pos=(self.pos[0],blockrect.top-BLOCKSIZE/3)
                         if self.vel[1]>0:
                            self.vel=(self.vel[0]*0.5,0)
      if p.alive:
          if p.rect.colliderect(self.rect):
             p.changeItem(self.name,self.amnt)
             worldItems.remove(self)
   def draw(self):
      screen.blit(itemImages[self.imgIndex],(int(self.rect.left-CAM.pos[0]),int(self.rect.top-CAM.pos[1])))
class Item():
   def __init__(self,name,amnt):
      self.name=name
      self.tags=getTagsFromName(name)
      self.amnt=amnt
      self.imgIndex=getItemImgIndex(name)
class Projectile():
    def __init__(self,pos,vel,ammoinfo,stats,rectsize,imgIndex):#pos = tuple, vel=tuple, stats=dict
        self.pos=pos
        self.vel=vel
        self.ammoinfo=ammoinfo
        self.imgIndex=imgIndex
        self.stats=stats
        self.rect=Rect(self.pos[0]-rectsize/2,self.pos[1]-rectsize/2,rectsize,rectsize)
        self.originialsize=self.rect.height
        self.angle=random.randint(0,360)
        projectiles.append(self)
    def update(self):
        if "arrow" in self.ammoinfo[1]:
            self.angle=math.atan2(self.vel[1],-self.vel[0])*180/math.pi
        elif "grenade" in self.ammoinfo[1]:
           speed =math.sqrt(self.vel[0]**2+self.vel[1]**2)
           self.angle+=speed
        else:
            self.angle+=10
        self.vel=(self.vel[0]*self.stats["air resistance"],self.vel[1]*self.stats["air resistance"]+self.stats["gravity"])
        self.pos=(self.pos[0]+self.vel[0],self.pos[1]+self.vel[1])
        self.rect.left=self.pos[0]
        self.rect.top=self.pos[1]
        blockpos=(math.floor(self.rect.centerx//BLOCKSIZE),math.floor(self.rect.centery//BLOCKSIZE))
        destroy=False
        try:
            for i in range(3):
                for j in range(3):
                    val=mapData[blockpos[1]+j-1-CHUNKSIZE][blockpos[0]+i-1-CHUNKSIZE][0]
                    if val not in uncollidableBlocks:
                       blockrect=Rect(BLOCKSIZE*(blockpos[0]+i-1),BLOCKSIZE*(blockpos[1]+j-1),BLOCKSIZE,BLOCKSIZE)
                       if blockrect.colliderect(self.rect):
                          deltaX = self.rect.centerx-blockrect.centerx
                          deltaY = self.rect.centery-blockrect.centery
                          if abs(deltaX) > abs(deltaY):
                              if deltaX > 0:
                                  if self.stats["bounce"]==True:
                                      if self.stats["bounceNum"]>0:
                                          self.stats["bounceNum"]-=1
                                          self.pos=(blockrect.right,self.pos[1])
                                          self.vel=(-self.vel[0]*0.9,self.vel[1])
                                      else:
                                          destroy=True
                                  else:
                                      destroy=True
                              else:
                                  if self.stats["bounce"]==True:
                                      if self.stats["bounceNum"]>0:
                                          self.stats["bounceNum"]-=1
                                          self.pos=(blockrect.left-self.rect.width,self.pos[1])
                                          self.vel=(-self.vel[0]*0.9,self.vel[1])
                                      else:
                                          destroy=True
                                  else:
                                      destroy=True
                          else:
                              if deltaY > 0:
                                  if self.stats["bounce"]==True:
                                      if self.stats["bounceNum"]>0:
                                          self.stats["bounceNum"]-=1
                                          self.pos=(self.pos[0],blockrect.bottom)
                                          if self.vel[1]<0:
                                             self.vel=(self.vel[0],-self.vel[1]*0.9)
                                      else:
                                          destroy=True
                                  else:
                                      destroy=True
                              else:
                                 if self.stats["bounce"]==True:
                                     if self.stats["bounceNum"]>0:
                                         self.stats["bounceNum"]-=1
                                         self.pos=(self.pos[0],blockrect.top-self.rect.height)
                                         if self.vel[1]>0:
                                             self.vel=(self.vel[0]*0.5,-self.vel[1]*0.9)
                                     else:
                                          destroy=True
                                 else:
                                     destroy=True
        except:None
        if self.stats["age"]==True:
            self.stats["life"]-=1
            if self.stats["life"]<=0:
                destroy=True
        if destroy:
            if "grenade" in self.ammoinfo[1]:
                for NPC in NPCS:
                    if distance(NPC.pos,self.pos)<BLOCKSIZE*2.5:
                        NPC.damage(self.stats["damage"],self.stats["crit"])
                if distance(p.pos,self.pos)<BLOCKSIZE*4:
                    p.damage(self.stats["damage"],self.stats["crit"])
            projectiles.remove(self)
            if self.stats["dropammo"]==True:
                if random.randint(0,2)==2:
                    WorldItem(self.ammoinfo[0],1,self.pos)
        for NPC in NPCS:
            if self.stats["damaging"]==True:
                if NPC.rect.colliderect(self.rect):
                    NPC.damage(self.stats["damage"],self.stats["crit"])
    def draw(self):
        self.surf=pygame.Surface((int(BLOCKSIZE/1.5),int(BLOCKSIZE/1.5)))
        self.surf.fill((255,0,255))
        self.surf.blit(itemImages[self.imgIndex],(0,0))
        self.surf.set_colorkey((255,0,255))
        self.surf=rot_center(self.surf,self.angle-90)
        screen.blit(self.surf,(self.pos[0]-self.rect.width/2-CAM.pos[0],self.pos[1]-self.rect.height/2-CAM.pos[1]))
        if showHitBoxes:
            pygame.draw.rect(screen,(255,0,0),Rect(self.rect.left-CAM.pos[0],self.rect.top-CAM.pos[1],self.rect.width,self.rect.height),2)
class Map():
   def __init__(self,xchunks,ychunks,CHUNKSIZE,BLOCKSIZE):
      self.CHUNKSIZE=CHUNKSIZE
      self.BLOCKSIZE=BLOCKSIZE
      self.xchunks=xchunks
      self.ychunks=ychunks
      self.chunks=[]
      self.focusChunks=[]
      self.createChunks()
      self.lightUpdateDelay=10
      self.lightUpdateTick=0
   def createChunks(self):
      self.chunks=[]
      for i in range(self.ychunks):
         self.chunks.append([])
         for j in range(self.xchunks):
            self.chunks[i].append(Chunk(self.CHUNKSIZE,self.BLOCKSIZE,(j*self.CHUNKSIZE*self.BLOCKSIZE,i*self.CHUNKSIZE*self.BLOCKSIZE)))
   def generateTerrain(self,num):
      global mapData
      mapData=[]
      for j in range(self.CHUNKSIZE*self.ychunks):
         mapData.append([])
         for i in range(self.CHUNKSIZE*self.xchunks):
            val=400-noise.noise((i*500)/10000,0.0001,0.235)*15+noise.noise((i*100)/10000,0.0001,0.235)*15
            if j<val:
               val=0
               backval=0
            else:
               if j<500:
                  val=2
                  backval=2
               else:
                  val=1
                  backval=1
               if j>400 and j<=450  and val==2: 
                  backval=2
               if j>0:
                  if mapData[j-1][i][0]==0 and val==2:
                     val=3
                     backval=3
                  if mapData[j-2][i][0]==0 and val==2:
                     backval=3
               
            mapData[j].append([val,backval])
      print("Spawning stone...")
      for i in range(int(CHUNKNUMX*CHUNKNUMY/6)):#surface stone
         ore(1,6,None,(300,425),(6,CHUNKNUMX*CHUNKSIZE-6))
      for i in range(int(CHUNKNUMX*CHUNKNUMY/4)):#lower stone
         ore(1,6,None,(425,500),(6,CHUNKNUMX*CHUNKSIZE-6),1)
      for i in range(int(CHUNKNUMX*CHUNKNUMY/4)):#boarder stone
         ore(1,6,None,(500,500),(6,CHUNKNUMX*CHUNKSIZE-6),1)
      val=random.randint(50,CHUNKSIZE*CHUNKNUMX-50)
      print("Spawning sand...")
      #for i in range(1):#add desert
      #   ore(18,15,None,(300,500),(val-50,val+50),18)
      print("Spawning Ores...")
      for i in range(int(CHUNKNUMX*CHUNKNUMY/3)):#coal
         ore(34,4,None,None,(4,CHUNKNUMX*CHUNKSIZE-4))
      for i in range(int(CHUNKNUMX*CHUNKNUMY/7)):#iron,copper,lead
         ore(33,3,None,None,(4,CHUNKNUMX*CHUNKSIZE-4))
         ore(51,3,None,None,(4,CHUNKNUMX*CHUNKSIZE-4))
         ore(52,3,None,None,(4,CHUNKNUMX*CHUNKSIZE-4))
      for i in range(int(CHUNKNUMX*CHUNKNUMY/8)):#silver
         ore(35,3,None,(450,CHUNKNUMY*CHUNKSIZE-4),(4,CHUNKNUMX*CHUNKSIZE-4))
      for i in range(int(CHUNKNUMX*CHUNKNUMY/12)):#gold
         ore(32,3,None,(550,CHUNKNUMY*CHUNKSIZE-4),(4,CHUNKNUMX*CHUNKSIZE-4))
      print("Growing Gemstones...")
      for i in range(int(CHUNKNUMX*CHUNKNUMY/100)):#gems
         ore(64,3,None,(450,CHUNKNUMY*CHUNKSIZE-4),(4,CHUNKNUMX*CHUNKSIZE-4))
         ore(65,3,None,(450,CHUNKNUMY*CHUNKSIZE-4),(4,CHUNKNUMX*CHUNKSIZE-4))
         ore(66,3,None,(450,CHUNKNUMY*CHUNKSIZE-4),(4,CHUNKNUMX*CHUNKSIZE-4))
         ore(67,3,None,(450,CHUNKNUMY*CHUNKSIZE-4),(4,CHUNKNUMX*CHUNKSIZE-4))
         ore(50,3,None,(450,CHUNKNUMY*CHUNKSIZE-4),(4,CHUNKNUMX*CHUNKSIZE-4))
      print("Making Caves...")
      for i in range(int(CHUNKNUMX*CHUNKNUMY/12)):#simple caves
         ore(0,10,None,None,(10,CHUNKNUMX*CHUNKSIZE-10))
      for i in range(int(CHUNKNUMX*CHUNKNUMY/12)):#bigger lower caves
         ore(0,17,None,(550,CHUNKSIZE*CHUNKNUMY-17),(17,CHUNKNUMX*CHUNKSIZE-17))
      print("Adding Loot... (",int(CHUNKNUMX*CHUNKNUMY/200),")")
      for i in range(int(CHUNKNUMX*CHUNKNUMY/200)):#Chest rooms
         chestRoom((random.randint(4,CHUNKNUMX*CHUNKSIZE-4),random.randint(500,CHUNKNUMY*CHUNKSIZE-4)))
      for i in range(int(CHUNKNUMX*CHUNKNUMY/3)):
          pot((random.randint(0,CHUNKNUMX*CHUNKSIZE-1),random.randint(420,CHUNKNUMY*CHUNKSIZE-12)))
      print("Growing Trees...")
      for i in range(int(CHUNKNUMX*CHUNKSIZE/3.5)):
         tree((random.randint(0,CHUNKNUMX*CHUNKSIZE),200))
##      data=open("maps\mapData"+str(num),"w")
##      for j in range(len(genData)):
##         string=""
##         for i in range(len(genData[i])):
##            string+=str(genData[i][j][0]).zfill(3)+str(genData[i][j][1]).zfill(3)
##         print(str(j/(self.CHUNKSIZE*self.ychunks)*100)+"%")
##         data.write(string+"\n")
##      data.close()
   def loadTerrain(self,num):
      global mapData
      data=open("maps\mapData"+str(num),"r")
      tData=data.readlines()
      mapData=[]
      for i in range(len(tData)):
         mapData.append([])
         for j in range(int(len(tData[0])/6)):
            mapData[i].append([int(tData[i][j*6:j*6+3]),int(tData[i][j*6+3:j*6+6])])
         print(str(i/(len(tData))*100)+"%")
      data.close()
   def loadChunks(self,pos):
      camj=int((pos[0]+screenW/2)//(BLOCKSIZE*CHUNKSIZE))
      cami=int((pos[1]+screenH/2)//(BLOCKSIZE*CHUNKSIZE))
      for chunk in self.focusChunks:
         if chunk[0]<cami-2 or chunk[0]>cami+2:
            self.chunks[chunk[0]][chunk[1]].loaded=False
            self.chunks[chunk[0]][chunk[1]].surface=None
            self.chunks[chunk[0]][chunk[1]].blocks=None
         if chunk[1]<camj-2 or chunk[1]>camj+2:
            self.chunks[chunk[0]][chunk[1]].loaded=False
            self.chunks[chunk[0]][chunk[1]].surface=None
            self.chunks[chunk[0]][chunk[1]].blocks=None
            
      self.focusChunks=[]
      for i in range(5):
         for j in range(5):
            cpos=(cami+i-2,camj+j-2)
            if cpos[0]>0 and cpos[0]<CHUNKNUMY and cpos[1]>0 and cpos[1]<CHUNKNUMX:
               self.focusChunks.append((cami+i-2,camj+j-2))
               if not self.chunks[cpos[0]][cpos[1]].loaded:
                  self.chunks[cpos[0]][cpos[1]].loaded=True
                  self.chunks[cpos[0]][cpos[1]].loadBlocks()
                  self.chunks[cpos[0]][cpos[1]].surface=pygame.Surface((CHUNKSIZE*BLOCKSIZE,CHUNKSIZE*BLOCKSIZE))
                  self.chunks[cpos[0]][cpos[1]].surface.set_colorkey((255,0,255))
                  self.chunks[cpos[0]][cpos[1]].updateSurface()
   def draw(self,offset):
      for chunk in self.focusChunks:
         self.chunks[chunk[0]][chunk[1]].draw(offset)
def ore(val,size,pos,brangey,brangex,back=None):
   global mapData
   if pos==None:
      if brangey !=None:
         if brangex !=None:
            pos=(random.randint(brangex[0],brangex[1]),random.randint(brangey[0],brangey[1]))
         else:
            pos=(random.randint(size,CHUNKNUMX*CHUNKSIZE-size-1),random.randint(brangey[0],brangey[1]))
      else:
         pos=(random.randint(size,CHUNKNUMX*CHUNKSIZE-size-1),random.randint(300,CHUNKNUMY*CHUNKSIZE-size-1))
   if mapData[pos[1]][pos[0]][0]>0:
      mapData[pos[1]][pos[0]][0]=val
      if back!=None:
         mapData[pos[1]][pos[0]][1]=back
      if random.randint(0,10)<=size:
         ore(val,size-1,(pos[0]-1,pos[1]),None,None,back)
      if random.randint(0,10)<=size:
         ore(val,size-1,(pos[0]+1,pos[1]),None,None,back)
      if random.randint(0,10)<=size:
         ore(val,size-1,(pos[0],pos[1]-1),None,None,back)
      if random.randint(0,10)<=size:
         ore(val,size-1,(pos[0],pos[1]+1),None,None,back)
class Chunk():
   def __init__(self,CHUNKSIZE,BLOCKSIZE,POS):
      self.CHUNKSIZE=CHUNKSIZE
      self.BLOCKSIZE=BLOCKSIZE
      self.POS=POS
      self.blocks=[]
      self.loaded=False
   def createRandomBlocks(self):
      self.blocks=[]
      for i in range(self.CHUNKSIZE):
         self.blocks.append([])
         for j in range(self.CHUNKSIZE):
            self.blocks[i].append(Block(random.randint(0,20),0))
   def loadBlocks(self):
      self.blocks=[]
      datai=int(self.POS[0]/(self.CHUNKSIZE*self.BLOCKSIZE))-1
      dataj=int(self.POS[1]/(self.CHUNKSIZE*self.BLOCKSIZE))-1
      for i in range(self.CHUNKSIZE):
         self.blocks.append([])
         for j in range(self.CHUNKSIZE):
            dat=mapData[dataj*self.CHUNKSIZE+j][datai*self.CHUNKSIZE+i]
            self.blocks[i].append(Block(dat[0],dat[1]))
      #self.sources=[(random.randint(0,CHUNKSIZE-1),random.randint(0,CHUNKSIZE-1)) for i in range(5)]
      #self.updateLight()
   def draw(self,offset):
      if self.loaded:
         screen.blit(self.surface,(self.POS[0]-offset[0],self.POS[1]-offset[1]))
   def updateLight(self):
      for source in self.sources:
         self.blocks[source[0]][source[1]].light=1
         self.traversed=[]
         self.fillLight(source,1,4)
   def fillLight(self,pos,val,size):
      if pos not in self.traversed:
         self.blocks[pos[0]][pos[1]].light=val
      else:
         return
      self.traversed.append(pos)
      if size<=0:
         return
      if pos[0]>0:
         if self.blocks[pos[0]-1][pos[1]].val>0:
            self.fillLight((pos[0]-1,pos[1]),val*0.6,size-1)
         else:
            self.fillLight((pos[0]-1,pos[1]),val*0.8,size-1)
      if pos[0]<CHUNKSIZE-1:
         if self.blocks[pos[0]+1][pos[1]].val>0:
            self.fillLight((pos[0]+1,pos[1]),val*0.6,size-1)
         else:
            self.fillLight((pos[0]+1,pos[1]),val*0.8,size-1)
      if pos[1]>0:
         if self.blocks[pos[0]][pos[1]-1].val>0:
            self.fillLight((pos[0],pos[1]-1),val*0.6,size-1)
         else:
            self.fillLight((pos[0],pos[1]-1),val*0.8,size-1)
      if pos[1]<CHUNKSIZE-1:
         if self.blocks[pos[0]][pos[1]+1].val>0:
            self.fillLight((pos[0],pos[1]+1),val*0.6,size-1)
         else:
            self.fillLight((pos[0],pos[1]+1),val*0.8,size-1)
   def updateSurface(self):
      self.surface.fill((255,0,255))
      self.surface.set_colorkey((255,0,255))
      for i in range(len(self.blocks)):
         for j in range(len(self.blocks[i])):
            if self.blocks[i][j].val in transparentBlocks:
               if self.blocks[i][j].backval>0:
                  self.surface.blit(backImages[self.blocks[i][j].backval],(self.BLOCKSIZE*i,self.BLOCKSIZE*j))
                  if self.blocks[i][j].backintegrity!=self.blocks[i][j].maxbackintegrity:
                     if self.blocks[i][j].backval==19 or self.blocks[i][j].backval==20:img=images[240+math.floor((self.blocks[i][j].maxbackintegrity-self.blocks[i][j].backintegrity)/self.blocks[i][j].maxbackintegrity*3)]
                     else:img=images[240+math.floor((self.blocks[i][j].maxbackintegrity-self.blocks[i][j].backintegrity)/self.blocks[i][j].maxbackintegrity*9)]
                     img.set_alpha(200)
                     self.surface.blit(img,(self.BLOCKSIZE*i,self.BLOCKSIZE*j))
            if self.blocks[i][j].val>0:
               self.surface.blit(images[self.blocks[i][j].val],(self.BLOCKSIZE*i,self.BLOCKSIZE*j))
               if self.blocks[i][j].integrity!=self.blocks[i][j].maxintegrity:
                  img=images[240+math.floor((self.blocks[i][j].maxintegrity-self.blocks[i][j].integrity)/self.blocks[i][j].maxintegrity*9)]
                  img.set_alpha(200)
                  self.surface.blit(img,(self.BLOCKSIZE*i,self.BLOCKSIZE*j))
            elif self.blocks[i][j].backval>0:
               self.surface.blit(backImages[self.blocks[i][j].backval],(self.BLOCKSIZE*i,self.BLOCKSIZE*j))
               if self.blocks[i][j].backintegrity!=self.blocks[i][j].maxbackintegrity:
                  if self.blocks[i][j].backval==19 or self.blocks[i][j].backval==20:img=images[240+math.floor((self.blocks[i][j].maxbackintegrity-self.blocks[i][j].backintegrity)/self.blocks[i][j].maxbackintegrity*3)]
                  else:img=images[240+math.floor((self.blocks[i][j].maxbackintegrity-self.blocks[i][j].backintegrity)/self.blocks[i][j].maxbackintegrity*9)]
                  img.set_alpha(200)
                  self.surface.blit(img,(self.BLOCKSIZE*i,self.BLOCKSIZE*j))
            if self.blocks[i][j].light!=1 and self.blocks[i][j].backval!=0:
               if self.blocks[i][j].backval==19:
                  lightimg=specialLightingImages[0]
               elif self.blocks[i][j].backval==20:
                  lightimg=specialLightingImages[1]
               elif self.blocks[i][j].backval==21:
                  lightimg=specialLightingImages[2]
               else:
                  lightimg=pygame.Surface((self.BLOCKSIZE,self.BLOCKSIZE))
               lightimg.set_alpha((1-self.blocks[i][j].light)*255)
               self.surface.blit(lightimg,(self.BLOCKSIZE*i,self.BLOCKSIZE*j))
class Block():
   def __init__(self,val,backval):
      self.val=val
      self.backval=backval
      integ=getIntegFromVal(val)
      self.integrity=integ
      self.maxintegrity=integ
      if backval>0:
         integ=getIntegFromVal(backval)
         self.backintegrity=integ
         self.maxbackintegrity=integ
      self.light=1
class Cam():
   def __init__(self,Map,pos):
      self.pos=pos
      self.oldpos=(-1000,-1000)
      self.Map=Map
      self.updateDelay=10
      self.updateTick=0
   def update(self):
      if self.pos!=self.oldpos:
         if self.updateTick>self.updateDelay:
            self.updateTick-=self.updateDelay
            self.Map.loadChunks(self.pos)
            self.oldpos=self.pos
         else:
            self.updateTick+=1
   def damageBlock(self,val,screenPos,tags):
     global mapData
      #try:
     actualPos=(screenPos[0]+int(self.pos[0]),screenPos[1]+int(self.pos[1]))
     chunkPos=(actualPos[0]//(CHUNKSIZE*BLOCKSIZE),actualPos[1]//(CHUNKSIZE*BLOCKSIZE))
     inChunkPos=((actualPos[0]-chunkPos[0]*CHUNKSIZE*BLOCKSIZE)//BLOCKSIZE,(actualPos[1]-chunkPos[1]*CHUNKSIZE*BLOCKSIZE)//BLOCKSIZE)
     if "pickaxe" in tags:
        bval =CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].val
        if bval>0:
           if bval==54 or bval==55:
               potLoot(actualPos)
               mapData[(actualPos[1]//BLOCKSIZE)-CHUNKSIZE][(actualPos[0]//BLOCKSIZE)-CHUNKSIZE][0]=0
               CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].val=0
               CAM.Map.chunks[chunkPos[1]][chunkPos[0]].updateSurface()
               return
           if CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].integrity>0:
              CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].integrity-=val
              CAM.Map.chunks[chunkPos[1]][chunkPos[0]].updateSurface()
              if CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].integrity<=0:
                 info = getInfoFromVal(bval)
                 CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].val=0
                 CAM.Map.chunks[chunkPos[1]][chunkPos[0]].updateSurface()
                 WorldItem(info[0],1,(chunkPos[0]*CHUNKSIZE*BLOCKSIZE+inChunkPos[0]*BLOCKSIZE+2/3*BLOCKSIZE,chunkPos[1]*CHUNKSIZE*BLOCKSIZE+inChunkPos[1]*BLOCKSIZE+2/3*BLOCKSIZE))
                 mapData[(actualPos[1]//BLOCKSIZE)-CHUNKSIZE][(actualPos[0]//BLOCKSIZE)-CHUNKSIZE][0]=0
     if "axe" in tags:
        backval=CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].backval
        if backval==19 or backval==20:
           CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].backintegrity-=val
           CAM.Map.chunks[chunkPos[1]][chunkPos[0]].updateSurface()
           if CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].backintegrity<=0:
              CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].backval=0
              CAM.Map.chunks[chunkPos[1]][chunkPos[0]].updateSurface()
              pos=((actualPos[0]//BLOCKSIZE)-CHUNKSIZE,(actualPos[1]//BLOCKSIZE)-CHUNKSIZE)
              mapData[pos[1]][pos[0]][1]=0
              chunksVisited=[]
              for i in range(20):
                 pos=(pos[0],pos[1]-1)
                 if mapData[pos[1]][pos[0]][1]==20 or mapData[pos[1]][pos[0]][1]==21:
                    mapData[pos[1]][pos[0]][1]=0
                    bchunkPos=(pos[0]//CHUNKSIZE+1,pos[1]//CHUNKSIZE+1)
                    if bchunkPos not in chunksVisited:
                       chunksVisited.append(bchunkPos)
                    binChunkPos=(pos[0]-bchunkPos[0]*CHUNKSIZE,pos[1]-bchunkPos[1]*CHUNKSIZE)
                    CAM.Map.chunks[bchunkPos[1]][bchunkPos[0]].blocks[binChunkPos[0]][binChunkPos[1]].backval=0
                    WorldItem("wood",random.randint(2,3),((pos[0]+CHUNKSIZE)*BLOCKSIZE+BLOCKSIZE,(pos[1]+CHUNKSIZE)*BLOCKSIZE+BLOCKSIZE))
                    if random.randint(0,7)==0:
                       WorldItem("acorn",1,((pos[0]+CHUNKSIZE)*BLOCKSIZE+BLOCKSIZE,(pos[1]+CHUNKSIZE)*BLOCKSIZE+BLOCKSIZE))
                 else:
                    for i in range(len(chunksVisited)):
                       CAM.Map.chunks[chunksVisited[i][1]][chunksVisited[i][0]].updateSurface()
     if "hammer" in tags:
        backval=CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].backval
        if backval!=0 and backval!=19 and backval!=20 and backval!=21:
           CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].backintegrity-=val
           CAM.Map.chunks[chunkPos[1]][chunkPos[0]].updateSurface()
           if CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].backintegrity<=0:
              CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].backval=0
              mapData[(actualPos[1]//BLOCKSIZE)-CHUNKSIZE][(actualPos[0]//BLOCKSIZE)-CHUNKSIZE][1]=0
              CAM.Map.chunks[chunkPos[1]][chunkPos[0]].updateSurface()
      #except:print("mouse off screen")
   def placeBlock(self,name,tags,screenPos):
      global mapData, chestData,tpressed
      actualPos=(screenPos[0]+int(self.pos[0]),screenPos[1]+int(self.pos[1]))
      blockpos=(actualPos[0]//BLOCKSIZE,actualPos[1]//BLOCKSIZE)
      if not tpressed:
         if "backwall" not in tags:
            if not Rect(p.pos[0]-CAM.pos[0]-BLOCKSIZE/2,p.pos[1]-CAM.pos[1]-BLOCKSIZE,BLOCKSIZE,BLOCKSIZE*2).colliderect(Rect(blockpos[0]*BLOCKSIZE-CAM.pos[0],blockpos[1]*BLOCKSIZE-CAM.pos[1],BLOCKSIZE,BLOCKSIZE)):
               if name=="acorn":
                  if tree((blockpos[0]-CHUNKSIZE,blockpos[1]-CHUNKSIZE)):
                     CAM.Map.chunks[blockpos[1]//CHUNKSIZE][blockpos[0]//CHUNKSIZE].loadBlocks()
                     CAM.Map.chunks[blockpos[1]//CHUNKSIZE-1][blockpos[0]//CHUNKSIZE].loadBlocks()
                     CAM.Map.chunks[blockpos[1]//CHUNKSIZE+1][blockpos[0]//CHUNKSIZE].loadBlocks()
                     CAM.Map.chunks[blockpos[1]//CHUNKSIZE][blockpos[0]//CHUNKSIZE].updateSurface()
                     CAM.Map.chunks[blockpos[1]//CHUNKSIZE-1][blockpos[0]//CHUNKSIZE].updateSurface()
                     CAM.Map.chunks[blockpos[1]//CHUNKSIZE+1][blockpos[0]//CHUNKSIZE].updateSurface()
                     tpressed=True
                     return True
                  else:
                     return False
                     
               val=getValFromName(name)
               chunkPos=(actualPos[0]//(CHUNKSIZE*BLOCKSIZE),actualPos[1]//(CHUNKSIZE*BLOCKSIZE))
               inChunkPos=((actualPos[0]-chunkPos[0]*CHUNKSIZE*BLOCKSIZE)//BLOCKSIZE,(actualPos[1]-chunkPos[1]*CHUNKSIZE*BLOCKSIZE)//BLOCKSIZE)
               if mapData[(actualPos[1]//BLOCKSIZE)-CHUNKSIZE][(actualPos[0]//BLOCKSIZE)-CHUNKSIZE][0]==0:
                  canPlace=False
                  if mapData[(actualPos[1]//BLOCKSIZE)-CHUNKSIZE][(actualPos[0]//BLOCKSIZE)-CHUNKSIZE][1]!=0:canPlace=True
                  elif mapData[(actualPos[1]//BLOCKSIZE)-CHUNKSIZE-1][(actualPos[0]//BLOCKSIZE)-CHUNKSIZE][0]!=0:canPlace=True
                  elif mapData[(actualPos[1]//BLOCKSIZE)-CHUNKSIZE+1][(actualPos[0]//BLOCKSIZE)-CHUNKSIZE][0]!=0:canPlace=True
                  elif mapData[(actualPos[1]//BLOCKSIZE)-CHUNKSIZE][(actualPos[0]//BLOCKSIZE)-CHUNKSIZE-1][0]!=0:canPlace=True
                  elif mapData[(actualPos[1]//BLOCKSIZE)-CHUNKSIZE][(actualPos[0]//BLOCKSIZE)-CHUNKSIZE+1][0]!=0:canPlace=True
                  if canPlace:
                      if val in chestBlocks:
                         chestData.append([((actualPos[0]//BLOCKSIZE)-CHUNKSIZE,(actualPos[1]//BLOCKSIZE)-CHUNKSIZE),[[None for i in range(4)] for i in range(7)]])
                      CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].val=val
                      integ=getIntegFromVal(val)
                      CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].integrity=integ
                      CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].maxintegrity=integ
                      CAM.Map.chunks[chunkPos[1]][chunkPos[0]].updateSurface()
                      mapData[(actualPos[1]//BLOCKSIZE)-CHUNKSIZE][(actualPos[0]//BLOCKSIZE)-CHUNKSIZE][0]=val
                      return True
         else:
            val=getValFromName(name)
            chunkPos=(actualPos[0]//(CHUNKSIZE*BLOCKSIZE),actualPos[1]//(CHUNKSIZE*BLOCKSIZE))
            inChunkPos=((actualPos[0]-chunkPos[0]*CHUNKSIZE*BLOCKSIZE)//BLOCKSIZE,(actualPos[1]-chunkPos[1]*CHUNKSIZE*BLOCKSIZE)//BLOCKSIZE)
            if mapData[(actualPos[1]//BLOCKSIZE)-CHUNKSIZE][(actualPos[0]//BLOCKSIZE)-CHUNKSIZE][1]==0:
               canPlace=False
               if mapData[(actualPos[1]//BLOCKSIZE)-CHUNKSIZE-1][(actualPos[0]//BLOCKSIZE)-CHUNKSIZE][1]!=0:canPlace=True
               elif mapData[(actualPos[1]//BLOCKSIZE)-CHUNKSIZE+1][(actualPos[0]//BLOCKSIZE)-CHUNKSIZE][1]!=0:canPlace=True
               elif mapData[(actualPos[1]//BLOCKSIZE)-CHUNKSIZE][(actualPos[0]//BLOCKSIZE)-CHUNKSIZE-1][1]!=0:canPlace=True
               elif mapData[(actualPos[1]//BLOCKSIZE)-CHUNKSIZE][(actualPos[0]//BLOCKSIZE)-CHUNKSIZE+1][1]!=0:canPlace=True 
               if canPlace:
                  CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].backval=val
                  integ=getIntegFromVal(val)
                  CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].backintegrity=integ
                  CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].maxbackintegrity=integ
                  CAM.Map.chunks[chunkPos[1]][chunkPos[0]].updateSurface()
                  mapData[(actualPos[1]//BLOCKSIZE)-CHUNKSIZE][(actualPos[0]//BLOCKSIZE)-CHUNKSIZE][1]=val
                  return True
         return False
   def altclickBlock(self,screenPos,tags):
      actualPos=(screenPos[0]+int(self.pos[0]),screenPos[1]+int(self.pos[1]))
      pos=((actualPos[0]//BLOCKSIZE)-CHUNKSIZE,(actualPos[1]//BLOCKSIZE)-CHUNKSIZE)
      if mapData[pos[1]][pos[0]][0] in chestBlocks:
         for i in range(len(chestData)):
            if chestData[i][0]==pos:
               items=chestData[i][1]
               p.openChest(pos,items)
   def render(self):
      self.Map.draw((self.pos[0],self.pos[1]))
def drawHoldingItem():
   m=pygame.mouse.get_pos()
   screen.blit(hotbarItemImages[itemHolding.imgIndex],(m[0]-BLOCKSIZE/3,m[1]-BLOCKSIZE/3))
   if "tool" not in itemHolding.tags:
      text=font.render(str(itemHolding.amnt),True,(255,255,255))
      screen.blit(text,(m[0]-text.get_width()/2+15,m[1]+5))
class Player():
   def __init__(self,pos,maxhp,movespeed):
      self.pos=pos
      self.vel=(0,0)
      self.maxhp=maxhp
      self.hp=maxhp
      self.hpsurf=pygame.Surface((428,50))
      self.hpsurf.set_colorkey((255,0,255))
      self.movespeed=movespeed
      self.rect=Rect(pos[0]-(BLOCKSIZE/2)*playerscale,pos[1]-BLOCKSIZE*playerscale,BLOCKSIZE*playerscale,BLOCKSIZE*2*playerscale)
      self.animationFrame=0
      self.direction=0
      self.animationTick=0
      self.groundedTick=0
      self.grounded=False
      self.hotbar=[None for i in range(10)]
      self.inventory=[[None for i in range(4)]for i in range(10)]
      self.coinSlots=[None for i in range(4)]
      self.ammoSlots=[None for i in range(4)]
      self.showInventory=False
      self.selectedItem=0
      self.craftableItems=[]
      self.itemList=[]
      self.craftingMenuVel=0
      self.craftingMenuPos=600
      self.craftingSlotDelay=0
      self.craftingTableInRange=False
      self.furnaceInRange=False
      self.anvilInRange=False
      self.chestOpen=False
      self.chestItems=None
      self.alive=True
      self.craftItemName=""
      self.craftItemComponents=[]
      self.respawnTick=0
   def drawHotbar(self):
      screen.blit(hotbarback,(10,10))
      for i in range(10):
         if self.hotbar[i]!=None:
            screen.blit(hotbarItemImages[self.hotbar[i].imgIndex],(22+i*61,20))
            if "tool" not in self.hotbar[i].tags:
                text=font.render(str(self.hotbar[i].amnt),True,(255,255,255))
                screen.blit(text,(50+i*61-text.get_width()/2,40))
      pygame.draw.rect(screen,(255,255,0),Rect(10+self.selectedItem*61,10,60,60),5)
   def updateCraftableItems(self,findItem=None):
       self.itemList=[]
       for i in range(10):
           if self.hotbar[i]!=None:
               found=False
               for k in range(len(self.itemList)):
                   if self.hotbar[i].name==self.itemList[k].name:
                       self.itemList[k].amnt+=self.hotbar[i].amnt
                       found=True
                       break
               if not found:
                   self.itemList.append(Item(self.hotbar[i].name,self.hotbar[i].amnt))
       for i in range(10):
           for j in range(4):
               if self.inventory[i][j]!=None:
                   found=False
                   for k in range(len(self.itemList)):
                       if self.inventory[i][j].name==self.itemList[k].name:
                           self.itemList[k].amnt+=self.inventory[i][j].amnt
                           found=True
                           break
                   if not found:
                       self.itemList.append(Item(self.inventory[i][j].name,self.inventory[i][j].amnt))
       self.craftableItems=[]
       for i in range(len(basicRecipies)):
          partscomplete=0
          for k in range(len(basicRecipies[i][2])):
             for g in range(len(self.itemList)):
                if basicRecipies[i][2][k][0] == self.itemList[g].name:
                   if self.itemList[g].amnt>=basicRecipies[i][2][k][1]:
                      partscomplete+=1
             if partscomplete>=len(basicRecipies[i][2]):
                self.craftableItems.append([Item(basicRecipies[i][0],basicRecipies[i][1]),basicRecipies[i][2]])
       if self.anvilInRange:
           for i in range(len(anvilRecipies)):
               partscomplete=0
               for k in range(len(anvilRecipies[i][2])):
                  for g in range(len(self.itemList)):  
                       if anvilRecipies[i][2][k][0] == self.itemList[g].name:
                           if self.itemList[g].amnt>=anvilRecipies[i][2][k][1]:
                               partscomplete+=1
                  if partscomplete>=len(anvilRecipies[i][2]):
                     self.craftableItems.append([Item(anvilRecipies[i][0],anvilRecipies[i][1]),anvilRecipies[i][2]])
       if self.craftingTableInRange:
           for i in range(len(tableRecipies)):
               partscomplete=0
               for k in range(len(tableRecipies[i][2])):
                  for g in range(len(self.itemList)):  
                       if tableRecipies[i][2][k][0] == self.itemList[g].name:
                           if self.itemList[g].amnt>=tableRecipies[i][2][k][1]:
                               partscomplete+=1
                  if partscomplete>=len(tableRecipies[i][2]):
                     self.craftableItems.append([Item(tableRecipies[i][0],tableRecipies[i][1]),tableRecipies[i][2]])
       if self.furnaceInRange:
           for i in range(len(furnaceRecipies)):
               partscomplete=0
               for k in range(len(furnaceRecipies[i][2])):
                  for g in range(len(self.itemList)):  
                       if furnaceRecipies[i][2][k][0] == self.itemList[g].name:
                           if self.itemList[g].amnt>=furnaceRecipies[i][2][k][1]:
                               partscomplete+=1
                  if partscomplete>=len(furnaceRecipies[i][2]):
                     self.craftableItems.append([Item(furnaceRecipies[i][0],furnaceRecipies[i][1]),furnaceRecipies[i][2]])
       found=False
       if findItem!=None:
          for i in range(len(self.craftableItems)):
             if self.craftableItems[i][0].name==findItem.name:
                found=True
                self.craftingMenuPos=600-i*60
       if not found:
          self.craftingMenuPos=600
           
   def drawCraftableItems(self):
       screen.blit(craftingBack,(10,360))
       craftsurf=pygame.Surface((55,506))
       craftsurf.fill((255,0,255))
       craftsurf.set_colorkey((255,0,255))
       for i in range(len(self.craftableItems)):
           craftsurf.blit(itemImages[self.craftableItems[i][0].imgIndex],(10,self.craftingMenuPos-355+i*60))
           text=font.render(str(self.craftableItems[i][0].amnt),True,(255,255,255))
           craftsurf.blit(text,(35,30+self.craftingMenuPos-360+i*60))
       screen.blit(craftsurf,(10,362))
       pygame.draw.rect(screen,(200,200,200),Rect(10,600,55,55),3)
       text=font.render(self.craftItemName,True,(255,255,255))
       screen.blit(text,(75,590))
       for i in range(len(self.craftItemComponents)):
          screen.blit(itemImages[self.craftItemComponents[i][2]],(80+i*60,610))
          text=font.render(str(self.craftItemComponents[i][1]),True,(255,255,255))
          screen.blit(text,(100+i*60,630))
   def drawInventory(self):
      screen.blit(inventoryback,(10,80))
      screen.blit(ammunitionBack,(700,80))
      screen.blit(ammunitionBack,(640,80))
      m=pygame.mouse.get_pos()
      for i in range(10):
          if self.hotbar[i]!=None:
              if Rect(10+i*61,10,61,61).collidepoint(m):
                  text=font.render(str(self.hotbar[i].name),True,(255,255,255))
                  screen.blit(text,(m[0]-text.get_width()/2,m[1]-20))
      for i in range(10):
          for j in range(4):
              if self.inventory[i][j]!=None:
                  screen.blit(hotbarItemImages[self.inventory[i][j].imgIndex],(22+i*61,90+j*61))
                  if "tool" not in self.inventory[i][j].tags:
                      text=font.render(str(self.inventory[i][j].amnt),True,(255,255,255))
                      screen.blit(text,(50+i*61-text.get_width()/2,110+j*61))
                  if Rect(10+i*61,70+j*61,61,61).collidepoint(m):
                      text=font.render(str(self.inventory[i][j].name),True,(255,255,255))
                      screen.blit(text,(m[0]-text.get_width()/2,m[1]-20))
      for i in range(4):
         if self.coinSlots[i]!=None:
             screen.blit(hotbarItemImages[self.coinSlots[i].imgIndex],(655,90+i*61))
             if "tool" not in self.coinSlots[i].tags:
                 text=font.render(str(self.coinSlots[i].amnt),True,(255,255,255))
                 screen.blit(text,(680-text.get_width()/2,110+i*61))
             if Rect(640,80+i*61,61,61).collidepoint(m):
                 text=font.render(str(self.coinSlots[i].name),True,(255,255,255))
                 screen.blit(text,(m[0]-text.get_width()/2,m[1]-20))
      for i in range(4):
         if self.ammoSlots[i]!=None:
             screen.blit(hotbarItemImages[self.ammoSlots[i].imgIndex],(712,90+i*61))
             if "tool" not in self.ammoSlots[i].tags:
                 text=font.render(str(self.ammoSlots[i].amnt),True,(255,255,255))
                 screen.blit(text,(740-text.get_width()/2,110+i*61))
             if Rect(700,80+i*61,61,61).collidepoint(m):
                 text=font.render(str(self.ammoSlots[i].name),True,(255,255,255))
                 screen.blit(text,(m[0]-text.get_width()/2,m[1]-20))
      if self.chestOpen:
         screen.blit(chestBack,(130,330))
         for i in range(7):
            for j in range(4):
               if self.chestItems[i][j]!=None:
                  screen.blit(hotbarItemImages[self.chestItems[i][j].imgIndex],(140+i*61,340+j*61))
                  if "tool" not in self.chestItems[i][j].tags:
                      text=font.render(str(self.chestItems[i][j].amnt),True,(255,255,255))
                      screen.blit(text,(170+i*61-text.get_width()/2,360+j*61))
                  if Rect(130+i*61,330+j*61,61,61).collidepoint(m):
                     text=font.render(str(self.chestItems[i][j].name),True,(255,255,255))
                     screen.blit(text,(m[0]-text.get_width()/2,m[1]-20))
      if pressed:
         drawHoldingItem()
   def updateInventory(self):
      global itemHolding, pressed, itemPos
      if pygame.mouse.get_pressed()[0]:
         if not pressed:
             if Rect(10,10,610,313).collidepoint(pygame.mouse.get_pos()):
               for i in range(10):
                  if Rect(10+i*61,10,61,61).collidepoint(pygame.mouse.get_pos()):
                     if self.hotbar[i]!=None:
                        itemHolding=self.hotbar[i]
                        itemPos=["hotbar",i]
                        self.hotbar[i]=None
                        pressed=True
               for i in range(10):
                  for j in range(4):
                     if Rect(10+i*61,70+j*61,61,61).collidepoint(pygame.mouse.get_pos()):
                        if self.inventory[i][j]!=None:
                           itemPos=["inventory",(i,j)]
                           itemHolding=self.inventory[i][j]
                           self.inventory[i][j]=None
                           pressed=True
             if Rect(640,80,120,240).collidepoint(pygame.mouse.get_pos()):
                 for i in range(4):
                     if Rect(640,80+i*61,61,61).collidepoint(pygame.mouse.get_pos()):
                        if self.coinSlots[i]!=None:
                            itemHolding=self.coinSlots[i]
                            itemPos=["coins",i]
                            self.coinSlots[i]=None
                            pressed=True
                 for i in range(4):
                     if Rect(700,80+i*61,61,61).collidepoint(pygame.mouse.get_pos()):
                        if self.ammoSlots[i]!=None:
                            itemHolding=self.ammoSlots[i]
                            itemPos=["ammo",i]
                            self.ammoSlots[i]=None
                            pressed=True
             if self.chestOpen:
                if Rect(130,330,420,240).collidepoint(pygame.mouse.get_pos()):
                  for i in range(10):
                     for j in range(4):
                        if Rect(130+i*61,330+j*61,61,61).collidepoint(m):
                           if self.chestItems[i][j]!=None:
                              itemPos=["chest",(i,j)]
                              itemHolding=self.chestItems[i][j]
                              self.chestItems[i][j]=None
                              pressed=True
      else:
         if pressed:
            pressed=False
            found=False
            for i in range(10):
               if Rect(10+i*61,10,61,61).collidepoint(pygame.mouse.get_pos()):
                  if self.hotbar[i]==None:
                     self.hotbar[i]=itemHolding
                  else:
                     if self.hotbar[i].name==itemHolding.name:
                        if "tool" not in self.hotbar[i].tags:
                           self.hotbar[i].amnt+=itemHolding.amnt
                           if self.hotbar[i].amnt>999:
                              self.changeItem(self.hotbar[i].name,self.hotbar[i].tags,self.hotbar[i].amnt-999)
                              self.hotbar[i].amnt=999
                     else:
                        putItemBack(self.hotbar[i])
                        self.hotbar[i]=itemHolding
                  found=True
                  self.updateCraftableItems()
                  break
            if not found:
               for i in range(10):
                  for j in range(4):
                     if Rect(10+i*61,70+j*61,61,61).collidepoint(pygame.mouse.get_pos()):
                        if self.inventory[i][j]==None:
                           self.inventory[i][j]=itemHolding
                        else:
                           if self.inventory[i][j].name==itemHolding.name:
                              if "tool" not in self.inventory[i][j].tags:
                                 self.inventory[i][j].amnt+=itemHolding.amnt
                                 if self.inventory[i][j].amnt>999:
                                    self.changeItem(self.inventory[i][j].name,self.inventory[i][j].tags,self.inventory[i][j].amnt-999)
                                    self.inventory[i][j].amnt=999
                           else:
                              putItemBack(self.inventory[i][j])
                              self.inventory[i][j]=itemHolding
                        found=True
                        self.updateCraftableItems()
                        break
            if not found:
                for i in range(4):
                    if Rect(640,60+i*61,61,61).collidepoint(pygame.mouse.get_pos()):
                        if self.coinSlots[i]==None:
                            self.coinSlots[i]=itemHolding
                        else:
                            if self.coinSlots[i].name==itemHolding.name:
                              if "tool" not in self.coinSlots[i].tags:
                                 self.coinSlots[i].amnt+=itemHolding.amnt
                                 if self.coinSlots[i].amnt>999:
                                    self.changeItem(self.coinSlots[i].name,self.coinSlots[i].tags,self.coinSlots[i].amnt-999)
                                    self.coinSlots[i].amnt=999
                            else:
                              putItemBack(self.coinSlots[i])
                              self.coinSlots[i]=itemHolding
                        found=True
                        self.updateCraftableItems()
                        break
            if not found:
                for i in range(4):
                    if Rect(700,60+i*61,61,61).collidepoint(pygame.mouse.get_pos()):
                        if self.ammoSlots[i]==None:
                            self.ammoSlots[i]=itemHolding
                        else:
                            if self.ammoSlots[i].name==itemHolding.name:
                              if "tool" not in self.ammoSlots[i].tags:
                                 self.ammoSlots[i].amnt+=itemHolding.amnt
                                 if self.ammoSlots[i].amnt>999:
                                    self.changeItem(self.ammoSlots[i].name,self.ammoSlots[i].tags,self.ammoSlots[i].amnt-999)
                                    self.ammoSlots[i].amnt=999
                            else:
                              putItemBack(self.coinSlots[i])
                              self.ammoSlots[i]=itemHolding
                        found=True
                        self.updateCraftableItems()
                        break
            if not found:
               if self.chestOpen:
                  for i in range(7):
                     for j in range(4):
                        if Rect(130+i*61,330+j*61,61,61).collidepoint(pygame.mouse.get_pos()):
                           if self.chestItems[i][j]==None:
                              self.chestItems[i][j]=itemHolding
                           else:
                              if self.chestItems[i][j].name==itemHolding.name:
                                 if "tool" not in self.chestItems[i][j].tags:
                                    self.chestItems[i][j].amnt+=itemHolding.amnt
                                    if self.chestItems[i][j].amnt>999:
                                       self.changeItem(self.chestItems[i][j].name,self.chestItems[i][j].tags,self.chestItems[i][j].amnt-999)
                                       self.chestItems[i][j].amnt=999
                              else:
                                 putItemBack(self.chestItems[i][j])
                                 self.chestItems[i][j]=itemHolding
                           found=True
                           self.updateCraftableItems()
                           break
            if not found:
               putItemBack(itemHolding)
   def updateAnimationFrame(self):
      if self.animationTick<0:
         self.animationTick+=7
         if self.animationFrame<3:
            self.animationFrame+=1
         else:
            self.animationFrame=0
      else:
         self.animationTick-=1
   def damage(self,val,crit):
       global damagePopUps
       if self.alive:
           if crit:col=(255,0,0)
           else:col=(200,100,0)
           damagePopUps.append([val,col,100,(p.pos[0]+random.randint(-20,20),p.pos[1]-80+random.randint(-20,20))])
           self.hp-=val
           if self.hp<=0:
               self.kill()
   def kill(self):
       self.alive=False
       self.respawnTick=500
       copper=math.floor(self.getItemAmnt("copper coin")/2)
       silver=math.floor(self.getItemAmnt("silver coin")/2)
       gold=math.floor(self.getItemAmnt("gold coin")/2)
       print(gold,silver,copper)
       if copper>0:
           self.changeItem("copper coin",["coin"],-copper)
           WorldItem("copper coin",copper,self.pos)
       if silver>0:
           self.changeItem("silver coin",-silver)
           WorldItem("silver coin",copper,self.pos)
       if gold>0:
           self.changeItem("gold coin",-gold)
           WorldItem("gold coin",copper,self.pos)
       
   def getItemAmnt(self,itemName):
       amnt=0
       for i in range(10):
           if self.hotbar[i]!=None:
               if self.hotbar[i].name==itemName:
                   amnt+=self.hotbar[i].amnt
       for i in range(10):
           for j in range(4):
               if self.inventory[i][j]!=None:
                   if self.inventory[i][j].name==itemName:
                       amnt+=self.inventory[i][j].amnt
       for i in range(4):
           if self.ammoSlots[i]!=None:
               if self.ammoSlots[i].name==itemName:
                   amnt+=self.ammoSlots[i].amnt
       for i in range(4):
           if self.coinSlots[i]!=None:
               if self.coinSlots[i].name==itemName:
                   amnt+=self.coinSlots[i].amnt
       return amnt
        
   def changeItem(self,name,amnt):#check hotbar and inventory for item, then use empty spaces
      if amnt>0:
          if name=="gold coin":
             addRecentPickup(name,amnt,(255,255,0))
          elif name=="silver coin":
             addRecentPickup(name,amnt,(176,176,176))
          elif name=="copper coin":
             addRecentPickup(name,amnt,(151,118,55))
          else:
             addRecentPickup(name,amnt)
      for i in range(10):
         if self.hotbar[i]!=None:
            if self.hotbar[i].name==name:
               if self.hotbar[i].amnt<999:
                  self.hotbar[i].amnt+=amnt
                  if self.hotbar[i].amnt>999:
                     amnt=p.hotbar[i].amnt-999
                     self.hotbar[i].amnt=999
                  elif self.hotbar[i].amnt<=0:
                      self.hotbar[i]=None
                      return
                  else:
                     return
      for i in range(10):
         for j in range(4):
            if self.inventory[i][j]!=None:
               if self.inventory[i][j].name==name:
                  if self.inventory[i][j].amnt<999:
                     self.inventory[i][j].amnt+=amnt
                     if self.inventory[i][j].amnt>999:
                        amnt=self.inventory[i][j].amnt-999
                        self.inventory[i][j].amnt=999
                     elif self.inventory[i][j].amnt<=0:
                         self.inventory[i][j]=None
                         return
                     else:
                        return
      for i in range(10):
         if self.hotbar[i]==None:
            self.hotbar[i]=Item(name,amnt)
            return
      for i in range(10):
         for j in range(4):
            if self.inventory[i][j]==None:
               self.inventory[i][j]=Item(name,amnt)
               return
   def update(self):
      global stopRight, stopLeft, pressed, itemHolding, itemPos
      if not self.alive:
          if self.respawnTick>0:
              self.respawnTick-=1
          else:
              self.pos=spawnPoint
              self.alive=True
              self.hp=self.maxhp
      if self.showInventory:
          if self.craftingSlotDelay<=0:
              if self.craftingMenuPos%60<29.8:
                  self.craftingMenuPos-=self.craftingMenuPos%60/2
              elif self.craftingMenuPos%60>30.2:
                  self.craftingMenuPos+=(60-self.craftingMenuPos%60)/2
              if len(self.craftableItems)>0 and not pressed:
                 itemIndex=int(round(abs(self.craftingMenuPos-600)/60))
                 self.craftItemName=self.craftableItems[itemIndex][0].name
                 self.craftItemComponents=self.craftableItems[itemIndex][1]
                 for i in range(len(self.craftItemComponents)):
                    self.craftItemComponents[i].append(getItemImgIndex(self.craftableItems[itemIndex][1][i][0]))
                 if pygame.mouse.get_pressed()[0]:
                    if Rect(10,600,55,55).collidepoint(pygame.mouse.get_pos()):
                       pressed=True
                       item=self.craftableItems[itemIndex][0]
                       itemHolding=Item(item.name,item.amnt)
                       for i in range(len(self.craftableItems[itemIndex][1])):
                           item=self.craftableItems[itemIndex][1][i]
                           p.changeItem(item[0],-item[1])
                       p.updateCraftableItems(itemHolding)
              else:
                 self.craftItemName=""
          else:
              self.craftingSlotDelay-=1
          self.craftingMenuVel*=0.9
          self.craftingMenuPos+=self.craftingMenuVel
          if self.craftingMenuPos>600:
              self.craftingMenuPos=600
          elif self.craftingMenuPos<655-len(self.craftableItems)*60:
              self.craftingMenuPos=655-len(self.craftableItems)*60
              
      if self.grounded:
         if self.groundedTick<=0:
            self.groundedTick+=7
            self.grounded=False
            #stopRight=False
            #stopLeft=False
         else:
            self.groundedTick-=1
      if self.alive:
          if movingRight:
             if not stopRight:
                self.direction=0
                self.updateAnimationFrame()
                self.vel=(self.vel[0]+1,self.vel[1])
                self.chestOpen=False
                self.showInventory=False
                itemPos=None
          if movingLeft:
             if not stopLeft:
                self.direction=1
                self.updateAnimationFrame()
                self.vel=(self.vel[0]-1,self.vel[1])
                self.chestOpen=False
                self.showInventory=False
                itemPos=None
      if not movingLeft and not movingRight:
         self.animationFrame=0
      if self.vel[0]<-self.movespeed:
         self.vel=(-self.movespeed,self.vel[1])
      if self.vel[0]>self.movespeed:
         self.vel=(self.movespeed,self.vel[1])
      if self.alive:
          self.vel=(self.vel[0]*0.95,self.vel[1]*0.99+0.3)
          self.pos=(self.pos[0]+self.vel[0],self.pos[1]+self.vel[1])
      self.blockpos=(math.floor(self.pos[0]//BLOCKSIZE),math.floor(self.pos[1]//BLOCKSIZE))
      self.craftingTableInRange=False
      self.furnaceInRange=False
      self.anvilInRange=False
      for i in range(3):
         for j in range(3):
            val=mapData[self.blockpos[1]+j-1-CHUNKSIZE][self.blockpos[0]+i-1-CHUNKSIZE][0]
            if val==84:
                self.craftingTableInRange=True
            if val==61:
               self.furnaceInRange=True
            if val==100:
               self.anvilInRange=True
            try:
               if val not in uncollidableBlocks:
                  blockrect=Rect(BLOCKSIZE*(self.blockpos[0]+i-1),BLOCKSIZE*(self.blockpos[1]+j-1),BLOCKSIZE,BLOCKSIZE)
                  if blockrect.colliderect(self.rect):
                     deltaX = self.pos[0]-blockrect.centerx
                     deltaY = self.pos[1]-blockrect.centery
                     if abs(deltaX) > abs(deltaY):
                         if deltaX > 0:
                            if val != 5:
                                self.pos=(blockrect.right+(BLOCKSIZE/2)*playerscale,self.pos[1])
                                self.vel=(0,self.vel[1])
                                stopLeft=True
                         else:
                            if val != 5:
                               self.pos=(blockrect.left-(BLOCKSIZE/2)*playerscale,self.pos[1])
                               self.vel=(0,self.vel[1])
                               stopRight=True
                     else:
                         if deltaY > 0:
                            if val != 5:
                               self.pos=(self.pos[0],blockrect.bottom+BLOCKSIZE*playerscale)
                               if self.vel[1]<0:
                                  self.vel=(self.vel[0],0)
                         else:
                            if val == 5:#platform code
                               if self.vel[1]>=0:
                                  if self.rect.bottom<=blockrect.top+10:
                                      if not movingDown:
                                         self.pos=(self.pos[0],blockrect.top-BLOCKSIZE*playerscale)
                                         if self.vel[1]>0:
                                            self.vel=(self.vel[0]*0.5,0)
                                         self.grounded=True
                            else:
                               self.pos=(self.pos[0],blockrect.top-BLOCKSIZE*playerscale)
                               if self.vel[1]>0:
                                  self.vel=(self.vel[0]*0.5,0)
                               self.grounded=True
            except:print("player out of map")
      self.rect.left=self.pos[0]-BLOCKSIZE/2*playerscale
      self.rect.top=self.pos[1]-BLOCKSIZE*playerscale
   def openChest(self,pos,items):
      self.chestOpen=True
      self.chestItems=items
      self.showInventory=True
      self.updateCraftableItems()
   def drawHP(self):
      heartNum=math.ceil(self.hp/10)
      for i in range(heartNum):
          surf=pygame.Surface((50,50))
          surf.set_colorkey((255,0,255))
          surf.blit(miscIcons[0],(0,0))
          if i==heartNum-1:
              surf.set_alpha(25.5*(self.hp%10))
          screen.blit(surf,(screenW-60-i*42,15))
      font=pygame.font.SysFont("Fixedsys",25)
      text=font.render("Life: "+str(self.hp)+"/"+str(self.maxhp),True,(255,255,255))
      screen.blit(text,(screenW-350,3))
   def draw(self):
      screen.blit(characterFrames[self.animationFrame+self.direction*4],(int(self.rect.left-CAM.pos[0]),int(self.rect.top-CAM.pos[1])))
      if showHitBoxes:
          pygame.draw.rect(screen,(255,0,0),Rect(self.rect.left-CAM.pos[0],self.rect.top-CAM.pos[1],self.rect.width,self.rect.height),2)
def distance(p1,p2):
   return math.sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)
def putItemBack(item):
    global itemPos
    if itemPos!=None:
       if itemPos[0]=="inventory":
          p.inventory[itemPos[1][0]][itemPos[1][1]]=item
       elif itemPos[0]=="hotbar":
          p.hotbar[itemPos[1]]=item
       elif itemPos[0]=="coins":
          p.coinSlots[itemPos[1]]=item
       elif itemPos[0]=="ammo":
          p.ammoSlots[itemPos[1]]=item
       else:
          p.chestItems[itemPos[1][0]][itemPos[1][1]]=item
    else:
        p.changeItem(item.name,item.amnt)
    itemPos=None
def tree(pos):
   global mapData
   planted=False
   for i in range(1000):
      try:
         if mapData[pos[1]-1][pos[0]][1]==20:
            return False
         if mapData[pos[1]+1][pos[0]][0]==3:
            planted=True
            if mapData[pos[1]][pos[0]][1]!=19:
               mapData[pos[1]][pos[0]][1]=19
               for i in range(12):
                  pos=(pos[0],pos[1]-1)
                  mapData[pos[1]][pos[0]][1]=20
                  if random.randint(0,15)==15 or i==11:
                     mapData[pos[1]][pos[0]][1]=21
                     break
               break
      except:None
      pos=(pos[0],pos[1]+1)
   if planted:
      return True
   else:
      return False
def chestRoom(pos):
   global chestData
   num=random.randint(0,5)
   if num==5:
      tier=2
   elif num>2:
      tier=1
   else:
      tier=0
   for i in range(9):
      for j in range(7):
         mapData[pos[1]-j-3][pos[0]-i-4][1]=16
         mapData[pos[1]-j-3][pos[0]-i-4][0]=0
         if i==0 or i==8 or j==0 or j==6:
            mapData[pos[1]-j-3][pos[0]-i-4][0]=16
   if tier==2:
      mapData[pos[1]-CHUNKSIZE+6][pos[0]-CHUNKSIZE+2][0]=86
   else:
      mapData[pos[1]-CHUNKSIZE+6][pos[0]-CHUNKSIZE+2][0]=85
   chest=[(pos[0]-CHUNKSIZE+2,pos[1]-CHUNKSIZE+6),lootChestItems(tier)]
   chestData.append(chest)
def lootChestItems(tier):
   itemArr=[[None for i in range(4)] for j in range(7)]
   rowsreq=len(chestLoot[tier])//7+1
   for j in range(rowsreq):
      for i in range(len(chestLoot[tier])-7*(rowsreq-1)):
         itemDat=chestLoot[tier][i%7+j*7][random.randint(0,len(chestLoot[tier][i])-1)]
         name=itemDat[0]
         amnt=random.randint(itemDat[1][0],itemDat[1][1])
         itemArr[i][j]=Item(name,amnt)
   return itemArr
def pot(pos):
    for i in range(10):
        if mapData[pos[1]][pos[0]][0]==0 and mapData[pos[1]+1][pos[0]][0] >0 and mapData[pos[1]+1][pos[0]][0] not in uncollidableBlocks:
            mapData[pos[1]][pos[0]][0] = random.randint(54,55)
            return True
        pos=(pos[0],pos[1]+1)
    return False
def potLoot(pos):
    rnum=random.randint(0,len(potLootItems)-1)
    WorldItem(potLootItems[rnum][0],random.randint(potLootItems[rnum][1][0],potLootItems[rnum][1][1]),pos)
def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
def updateWorldItems():
   global worldItems
   for item in worldItems:
      item.update()
def drawWorldItems():
   for item in worldItems:
      item.draw()
def getItemImgIndex(name):
   if name=="wood":return 4
   if name=="dirt":return 2
   if name=="stone":return 1
   if name=="copper":return 226
   if name=="iron":return 210
   if name=="coal":return 194
   if name=="silver":return 178
   if name=="gold":return 162
   if name=="copper bar":return 227
   if name=="iron bar":return 211
   if name=="silver bar":return 179
   if name=="gold bar":return 163
   if name=="copper pickaxe":return 106
   if name=="copper axe":return 107
   if name=="copper hammer":return 108
   if name=="copper sword":return 109
   if name=="iron pickaxe":return 122
   if name=="iron axe":return 123
   if name=="iron hammer":return 124
   if name=="iron sword":return 125
   if name=="lead pickaxe":return 90
   if name=="lead axe":return 91
   if name=="lead hammer":return 92
   if name=="lead sword":return 93
   if name=="silver pickaxe":return 138
   if name=="silver axe":return 139
   if name=="silver hammer":return 140
   if name=="silver sword":return 141
   if name=="gold pickaxe":return 154
   if name=="gold axe":return 155
   if name=="gold hammer":return 156
   if name=="gold sword":return 157
   if name=="cobble":return 16
   if name=="crafting table":return 84
   if name=="wood platform":return 5
   if name=="wood backwall":return 20
   if name=="cobble backwall":return 17
   if name=="cobble furnace":return 61
   if name=="wooden chest":return 85
   if name=="gold chest":return 86
   if name=="gold coin":return 54
   if name=="silver coin":return 55
   if name=="copper coin":return 56
   if name=="acorn":return 39
   if name=="greater healing potion":return 71
   if name=="lesser healing potion":return 72
   if name=="throwing knife":return 121
   if name=="shuriken":return 137
   if name=="sponge":return 48
   if name=="wooden bow":return 136
   if name=="wooden arrow":return 153
   if name=="grenade":return 152
   if name=="amethyst":return 161
   if name=="ruby":return 193
   if name=="topaz":return 177
   if name=="diamond":return 209
   if name=="sapphire":return 225
   if name=="iron anvil":return 100
   if name=="lead":return 146
   if name=="lead bar":return 147
   if name=="copper bow": return 110
   if name=="iron bow": return 126
   if name=="lead bow": return 94
   if name=="silver bow": return 142
   if name=="gold bow": return 158
   if name=="ruby staff": return 95
   if name=="amethyst staff": return 111
   if name=="sapphire staff": return 143
   if name=="topaz staff": return 127
   if name=="diamond staff": return 159
def getTagsFromName(name):
   if name=="wood":return ["block","material"]
   if name=="dirt":return ["block"]
   if name=="stone":return ["block","material"]
   if name=="copper":return ["ore"]
   if name=="iron":return ["ore"]
   if name=="coal":return ["ore"]
   if name=="silver":return ["ore"]
   if name=="gold":return ["ore"]
   if name=="lead": return ["ore"]
   if name=="copper bar":return ["material"]
   if name=="iron bar":return ["material"]
   if name=="silver bar":return ["material"]
   if name=="gold bar":return ["material"]
   if name=="lead bar": return ["material"]
   if name=="copper pickaxe":return ["tool","pickaxe"]
   if name=="copper axe":return ["tool","axe"]
   if name=="copper hammer":return ["tool","hammer"]
   if name=="copper sword":return ["tool","sword"]
   if name=="iron pickaxe":return ["tool","pickaxe"]
   if name=="iron axe":return ["tool","axe"]
   if name=="iron hammer":return ["tool","hammer"]
   if name=="iron sword":return ["tool","sword"]
   if name=="lead pickaxe":return ["tool","pickaxe"]
   if name=="lead axe":return ["tool","axe"]
   if name=="lead hammer":return ["tool","hammer"]
   if name=="lead sword":return ["tool","sword"]
   if name=="silver pickaxe":return ["tool","pickaxe"]
   if name=="silver axe":return ["tool","axe"]
   if name=="silver hammer":return ["tool","hammer"]
   if name=="silver sword":return ["tool","sword"]
   if name=="gold pickaxe":return ["tool","pickaxe"]
   if name=="gold axe":return ["tool","axe"]
   if name=="gold hammer":return ["tool","hammer"]
   if name=="gold sword":return ["tool","sword"]
   if name=="cobble":return ["block","material"]
   if name=="crafting table":return ["block"]
   if name=="wood platform":return ["block"]
   if name=="wood backwall":return ["block","backwall"]
   if name=="cobble backwall":return ["block","backwall"]
   if name=="cobble furnace":return ["block","furnace"]
   if name=="wooden chest":return ["block","chest"]
   if name=="gold chest":return ["block","chest"]
   if name=="gold coin":return ["coin"]
   if name=="silver coin":return ["coin"]
   if name=="copper coin":return ["coin"]
   if name=="acorn":return ["block"]
   if name=="greater healing potion":return ["potion","healing"]
   if name=="lesser healing potion":return ["potion","healing"]
   if name=="throwing knife":return ["throwable"]
   if name=="shuriken":return ["throwable"]
   if name=="sponge":return ["block"]
   if name=="wooden bow":return ["weapon","bow"]
   if name=="wooden arrow":return ["ammunition","arrow"]
   if name=="grenade":return ["throwable","grenade"]
   if name=="amethyst":return ["gem","material"]
   if name=="ruby":return ["gem","material"]
   if name=="topaz":return ["gem","material"]
   if name=="diamond":return ["gem","material"]
   if name=="sapphire":return ["gem","material"]
   if name=="iron anvil": return ["block","anvil"]
   if name=="ruby staff": return ["weapon","magic","staff"]
   if name=="amethyst staff": return ["weapon","magic","staff"]
   if name=="sapphire staff": return ["weapon","magic","staff"]
   if name=="topaz staff": return ["weapon","magic","staff"]
   if name=="diamond staff": return ["weapon","magic","staff"]
   if name=="copper bow": return ["weapon","bow"]
   if name=="iron bow": return ["weapon","bow"]
   if name=="lead bow": return ["weapon","bow"]
   if name=="silver bow": return ["weapon","bow"]
   if name=="gold bow": return ["weapon","bow"]
def getInfoFromVal(val):
   if val==1:return ["cobble",["material","block"]]
   if val==4:return ["wood",["material","block"]]
   if val==2 or val==3:return ["dirt",["material","block"]]
   if val==5:return ["wood platform",["block"]]
   if val==32:return ["gold",["ore"]]
   if val==33:return ["iron",["ore"]]
   if val==34:return ["coal",["ore","material"]]
   if val==16:return ["cobble",["block"]]
   if val==35:return ["silver",["ore"]]
   if val==51:return ["copper",["ore"]]
   if val==84:return ["crafting table",["block"]]
   if val==61:return ["cobble furnace",["block"]]
   if val==85:return ["wooden chest",["block","chest"]]
   if val==86:return ["gold chest",["block","chest"]]
   if val==48:return ["sponge",["block"]]
   if val==50:return ["topaz",["gem","material"]]
   if val==66:return ["ruby",["gem","material"]]
   if val==67:return ["sapphire",["gem","material"]]
   if val==65:return ["amethyst",["gem","material"]]
   if val==64:return ["diamond",["gem","material"]]
   if val==100:return ["iron anvil",["gem","material"]]
   if val==52:return ["lead",["ore"]]
def getValFromName(name):
   if name=="stone":return 1
   if name=="dirt":return 2
   if name=="cobble":return 16
   if name=="wood":return 4
   if name=="crafting table":return 84
   if name=="wood platform":return 5
   if name=="wood backwall":return 4
   if name=="cobble backwall":return 16
   if name=="cobble furnace":return 61
   if name=="wooden chest":return 85
   if name=="gold chest":return 86
   if name=="sponge":return 48
   if name=="iron anvil": return 100
def getIntegFromVal(val):
   if val==1:return 100
   if val==2 or val==3:return 75
   if val==32:return 200
   if val==33:return 175
   if val==34:return 150
   if val==35:return 150
   if val==51:return 120
   if val==16:return 100
   if val==19:return 500
   if val==20:return 500
   if val==4:return 150
   if val==84:return 200
   if val==5:return 80
   if val==61:return 200
   if val==85:return 200
   if val==86:return 200
   if val==48:return 2000
   if val==54 or val==55:return 5
   if val==50:return 150
   if val==66:return 150
   if val==67:return 150
   if val==65:return 150
   if val==64:return 250
   if val==100:return 350
   if val==52: return 200
def updateRecentPickups():
   global recentPickups
   for pickup in recentPickups:
      pickup[2]-=1
      if pickup[2]<0:
         recentPickups.remove(pickup)
   recentPickups=sorted(recentPickups,key= lambda x:x[2],reverse=True)
def drawRecentPickups():
   for i in range(len(recentPickups)):
      if recentPickups[i][2]>90:
         font=pygame.font.SysFont("Fixedsys",int((100-recentPickups[i][2])*2.8))
      else:
         font=pygame.font.SysFont("Fixedsys",28)
      if recentPickups[i][1]>1:
         text=font.render(recentPickups[i][0]+" ("+str(recentPickups[i][1])+")",False,recentPickups[i][4])
      else:
         text=font.render(recentPickups[i][0],False,recentPickups[i][4])
      if recentPickups[i][2]<=25:
         text.set_alpha(recentPickups[i][2]/25*255)
      screen.blit(text,(recentPickups[i][3][0]-CAM.pos[0]-text.get_width()/2,recentPickups[i][3][1]-CAM.pos[1]-75-i*30))
def updateDamagePopUps():
   global damagePopUps
   for popup in damagePopUps:
      popup[2]-=1
      if popup[2]<0:
         damagePopUps.remove(popup)
def drawDamagePopUps():
   for i in range(len(damagePopUps)):
      if damagePopUps[i][2]>90:
         font=pygame.font.SysFont("Fixedsys",int((100-damagePopUps[i][2])*4))
      else:
         font=pygame.font.SysFont("Fixedsys",40)
      text=font.render(str(damagePopUps[i][0]),False,damagePopUps[i][1])
      if damagePopUps[i][2]<=25:
         text.set_alpha(damagePopUps[i][2]/25*255)
      screen.blit(text,(damagePopUps[i][3][0]-CAM.pos[0]-text.get_width()/2,damagePopUps[i][3][1]-CAM.pos[1]))
def addRecentPickup(name,amnt,colour=(255,255,255)):
   global recentPickups
   for i in range(len(recentPickups)):
      if recentPickups[i][0]==name.title():
         recentPickups[i][1]+=amnt
         recentPickups[i][2]=100
         recentPickups[i][3]=p.pos
         recentPickups[i][4]=colour
         return
   recentPickups.append([name.title(),amnt,100,p.pos,colour])
def updateNPCS():
   global NPCS
   for NPC in NPCS:
      NPC.update()
def drawNPCS():
   for NPC in NPCS:
      NPC.draw()
def updateProjectiles():
   global projectiles
   for projectile in projectiles:
      projectile.update()
def drawProjectiles():
   for projectile in projectiles:
      projectile.draw()
transparentBlocks=[84,5,85,86,54,55,100]
uncollidableBlocks=[0,84,61,85,86,54,55,100]
chestBlocks=[85,86]

NPCS=[]
projectiles=[]

birdNum=0

if platform.system() == "Darwin": #Resolves Font Errors on OSX : User is required to Install
  font=pygame.font.SysFont("Fonts/ARCADECLASSIC.TFF",20)
else:
  font=pygame.font.Font("Fonts/ARCADECLASSIC.TTF",20)
clock=pygame.time.Clock()

basicRecipies=[#[out item name,out item tags,out item quantity,out item imgIndex,[in items, in item quianties]]
   ["wood",1,[["wood backwall",4]]],
   ["wood",1,[["wood platform",2]]],
   ["cobble",1,[["cobble backwall",4]]],
   ["wood platform",2,[["wood",1]]],
   ["crafting table",1,[["wood",10]]],
   ]
tableRecipies=[
   ["wood backwall",4,[["wood",1]]],
   ["cobble backwall",4,[["cobble",1]]],
   ["iron anvil",1,[["iron bar",5]]],
   ["cobble furnace",1,[["coal",4],["cobble",10]]],
   ["wooden chest",1,[["wood",20],["iron bar",2]]],
   ["sponge",1,[["stone",100]]],
   ["wooden bow",1,[["wood",10]]],
   ["wooden arrow",25,[["wood",1],["cobble",1]]],
   ]
anvilRecipies=[
    ["copper pickaxe",1,[["wood",10],["copper bar",10]]],
    ["copper hammer",1,[["wood",10],["copper bar",5]]],
    ["copper axe",1,[["wood",10],["copper bar",5]]],
    ["copper sword",1,[["wood",10],["copper bar",5]]],
    ["copper bow",1,[["copper bar",7]]],
    ["iron pickaxe",1,[["wood",10],["iron bar",10]]],
    ["iron axe",1,[["wood",10],["iron bar",5]]],
    ["iron hammer",1,[["wood",10],["iron bar",5]]],
    ["iron sword",1,[["wood",10],["iron bar",5]]],
    ["iron bow",1,[["iron bar",7]]],
    ["lead pickaxe",1,[["wood",10],["lead bar",10]]],
    ["lead axe",1,[["wood",10],["lead bar",5]]],
    ["lead hammer",1,[["wood",10],["lead bar",5]]],
    ["lead sword",1,[["wood",10],["lead bar",5]]],
    ["lead bow",1,[["lead bar",7]]],
    ["silver pickaxe",1,[["wood",10],["silver bar",10]]],
    ["silver axe",1,[["wood",10],["silver bar",5]]],
    ["silver hammer",1,[["wood",10],["silver bar",5]]],
    ["silver sword",1,[["wood",10],["silver bar",5]]],
    ["silver bow",1,[["silver bar",7]]],
    ["gold pickaxe",1,[["wood",10],["gold bar",10]]],
    ["gold axe",1,[["wood",10],["gold bar",5]]],
    ["gold hammer",1,[["wood",10],["gold bar",5]]],
    ["gold sword",1,[["wood",10],["gold bar",5]]],
    ["gold bow",1,[["gold bar",7]]],
    ["diamond staff",1,[["diamond",5],["gold bar",5]]],
    ["sapphire staff",1,[["sapphire",5],["silver bar",7]]],
    ["ruby staff",1,[["ruby",5],["lead bar",9]]],
    ["topaz staff",1,[["topaz",5],["iron bar",12]]],
    ["amethyst staff",1,[["amethyst",5],["copper bar",15]]],
    ]
furnaceRecipies=[
   ["iron bar",1,[["iron",3]]],
   ["copper bar",1,[["copper",3]]],
   ["silver bar",1,[["silver",3]]],
   ["gold bar",1,[["gold",3]]],
   ["lead bar",1,[["lead",3]]],
   ["stone",1,[["cobble",1]]],
   ]

toolspeeds={"copper":4,
            "iron":6,
            "lead":8,
            "silver":10,
            "gold":12,
            }
bowBaseDamages={
    "wooden":(8,11),
    "copper":(11,13),
    "iron":(13,15),
    "lead":(15,18),
    "silver":(18,21),
    "gold":(21,23),
    }
chestLoot = [[
   [["copper bar",(4,15)],["iron bar",(4,15)],["silver bar",(4,10)]],
   [["lesser healing potion",(2,7)]],
   [["silver coin",(20,69)]],
   [["shuriken",(10,30)],["throwing knife",(10,30)]],
   ],

[
   [["gold coin",(1,1)],["copper bar",(8,20)],["iron bar",(8,20)],["silver bar",(8,15)]],
   [["copper bar",(8,20)],["iron bar",(8,20)],["silver bar",(8,15)]],
   [["lesser healing potion",(3,9)],["greater healing potion",(1,3)]],
   [["silver coin",(20,69)]],
   [["shuriken",(20,40)],["throwing knife",(20,40)]],
   [["grenade",(10,20)]],
   [["ruby",(1,2)],["sapphire",(1,2)],["diamond",(1,2)],["topaz",(1,3)],["amethyst",(1,2)]]
   ],

[
   [["gold bar",(3,9)]],#slot2
   [["gold coin",(1,2)]],#slot2
   [["silver coin",(50,99)]],#slot3
   [["shuriken",(30,70)]],#slot4
   [["throwing knife",(30,70)]],#slot5
   [["greater healing potion",(2,7)],["lesser healing potion",(5,15)]],#etc.
   [["grenade",(10,30)]],#slot4
   [["ruby",(2,5)],["sapphire",(2,5)],["diamond",(2,5)],["topaz",(2,5)],["amethyst",(2,5)]]
   ]]
potLootItems=[
    ["shuriken",(20,40)],
    ["throwing knife",(20,40)],
    ["lesser healing potion",(1,3)],
    ["wooden arrow",(20,40)],
    ["silver coin",(5,15)],
    ["grenade",(5,15)],
    ]

baseItemDamages={
    "throwing knife":(7,13),
    "grenade":(20,30),
    "shuriken":(5,10),
    "wooden arrow":(3,4)
    }
baseItemCritChance={
    "throwing knife":0.1,
    "shuriken":0.15,
    "wooden arrow":0.1,
    "grenade":0.05,
    }
worldSize="tiny"

worldSizes={
   "tiny":[20,70],#3 seconds to gen
   "small":[100,80],#16 seconds to gen
   "medium":[200,120],#50 seconds to gen
   "large":[400,180],#146 seconds to gen
   "massive":[800,240],#>146 seconds
   }

CHUNKSIZE=10
BLOCKSIZE=48

CHUNKNUMX=worldSizes[worldSize][0]
CHUNKNUMY=worldSizes[worldSize][1]

print("Worldsize: "+worldSize+" ("+str(CHUNKSIZE*CHUNKNUMX)+"x"+str(CHUNKSIZE*CHUNKNUMY)+" blocks)")
PLAYERREACH=BLOCKSIZE*5

LEFTBOARDER=CHUNKSIZE*BLOCKSIZE+BLOCKSIZE/2
RIGHTBOARDER=CHUNKSIZE*BLOCKSIZE*CHUNKNUMX-BLOCKSIZE/2
BOTBOARDER=CHUNKSIZE*BLOCKSIZE*CHUNKNUMY-BLOCKSIZE/2
TOPBOARDER=CHUNKSIZE*BLOCKSIZE+BLOCKSIZE/2

globalLighting=1

worldItems=[]
recentPickups=[]#name,amnt,life,pos
damagePopUps=[]#amnt,colour,life,pos
chestData=[]

stopRight=False
stopLeft=False
movingRight=False
movingLeft=False
movingDown=False
movingDownTimer=0
pressed=False
altpressed=False
tpressed=False
t2pressed=False
itemHolding=None
itemPos=None

print("Loading images...")

loadTileImages()
loadBackTileImages()
loadCharacterAnimation()
loadHotbarImages()
assembleHotbarBack()
assembleInventoryBack()
assembleCraftingBack()
assembleChestBack()
assembleAmmunitionBack()
loadItemImages()
loadLightingImages()
loadBirdImages()
loadMiscIcons()


print("Initailizing Objects...")
spawnPoint=(BLOCKSIZE*CHUNKNUMX*CHUNKSIZE/2,BLOCKSIZE*395)
CAM=Cam(Map(CHUNKNUMX,CHUNKNUMY,CHUNKSIZE,BLOCKSIZE),(spawnPoint[0]-screenW/2,spawnPoint[1]))
p=Player(spawnPoint,100,4)
print("Generating terrain...")
CAM.Map.generateTerrain(0)
#CAM.Map.loadTerrain(0)

print("Giving tools...")

p.hotbar[0]=Item("copper pickaxe",1)
p.hotbar[1]=Item("copper axe",1)
p.hotbar[2]=Item("copper hammer",1)
p.hotbar[3]=Item("copper sword",1)
ie=lootChestItems(2)
print("Done! (In",pygame.time.get_ticks()/1000,"seconds!)")
p.hp=25
while 1:
   if p.pos[1]/BLOCKSIZE<430:
      if birdNum<3 and random.randint(0,100)==100:
         if random.randint(0,1)==1:
            bird((CAM.pos[0]-20,random.randint(int(CAM.pos[1]),int(CAM.pos[1]+4*BLOCKSIZE))),(1,0))
         else:
            bird((CAM.pos[0]+screenW,random.randint(int(CAM.pos[1]),int(CAM.pos[1]+4*BLOCKSIZE))),(-1,0))
   gameTick=pygame.time.get_ticks()
   if movingDown:
      if movingDownTimer>0:
         movingDownTimer-=1
         if movingDownTimer<=0:
            movingDown=False
      movingDownTimer
   CAM.pos=(CAM.pos[0]+(p.pos[0]-screenW/2-CAM.pos[0])*0.05,CAM.pos[1]+(p.pos[1]-screenH/2-CAM.pos[1])*0.05)
   rel=pygame.mouse.get_rel()
   m=pygame.mouse.get_pos()
##   if pygame.mouse.get_pressed()[2]:    
##      CAM.pos=(CAM.pos[0]-rel[0],CAM.pos[1]-rel[1])
   if p.pos[0]<LEFTBOARDER:
      p.pos=(LEFTBOARDER,p.pos[1])
   elif p.pos[0]>RIGHTBOARDER:
      p.pos=(RIGHTBOARDER,p.pos[1])
   if p.pos[1]<TOPBOARDER:
      p.pos=(p.pos[0],TOPBOARDER)
   elif p.pos[1]>BOTBOARDER:
      p.pos=(p.pos[0],BOTBOARDER)
   if CAM.pos[0]<LEFTBOARDER-BLOCKSIZE/2:
      CAM.pos=(LEFTBOARDER-BLOCKSIZE/2,CAM.pos[1])
   elif CAM.pos[0]>RIGHTBOARDER+BLOCKSIZE/2-screenW:
      CAM.pos=(RIGHTBOARDER+BLOCKSIZE/2-screenW,CAM.pos[1])
   if CAM.pos[1]<TOPBOARDER-BLOCKSIZE/2:
      CAM.pos=(CAM.pos[0],TOPBOARDER-BLOCKSIZE/2)
   elif CAM.pos[1]>BOTBOARDER+BLOCKSIZE/2-screenH:
      CAM.pos=(CAM.pos[0],BOTBOARDER+BLOCKSIZE/2-screenH)
   if pygame.mouse.get_pressed()[0] and p.alive:
      if p.hotbar[p.selectedItem]!=None:
          tags=p.hotbar[p.selectedItem].tags
          if distance((p.pos[0]-CAM.pos[0],p.pos[1]-CAM.pos[1]),m)<PLAYERREACH:
             if "tool" in tags:
                for i in range(len(p.hotbar[p.selectedItem].name)):
                   if p.hotbar[p.selectedItem].name[i]==" ":
                      toolset=p.hotbar[p.selectedItem].name[:i]
                      break
                damage=toolspeeds[toolset]
                CAM.damageBlock(damage,m,tags)
             if "block" in tags:
                if CAM.placeBlock(p.hotbar[p.selectedItem].name,p.hotbar[p.selectedItem].tags,m):
                   p.hotbar[p.selectedItem].amnt-=1
                   if p.hotbar[p.selectedItem].amnt<=0:
                      p.hotbar[p.selectedItem]=None
          if not t2pressed:
              t2pressed=True
              stats={"bounce":False,"life":300,"damaging":False,"crit":False,"gravity":0.2,"age":False,"dropammo":False,"air resistance":0.99}
              if "throwable" in tags: 
                  angle=math.atan2(p.pos[1]-CAM.pos[1]-m[1],p.pos[0]-CAM.pos[0]-m[0])
                  vel=(-math.cos(angle)*15,-math.sin(angle)*15)
                  damages=baseItemDamages[p.hotbar[p.selectedItem].name]
                  damage=random.randint(damages[0],damages[1])
                  stats["damage"]=damage
                  if random.randint(0,100)<100*baseItemCritChance[p.hotbar[p.selectedItem].name]:
                       stats["damage"]*=2
                       stats["crit"]=True
                  if "grenade" in tags:
                      stats["age"]=True
                      stats["life"]=300
                      stats["bounce"]=True
                      stats["bounceNum"]=10
                      Projectile(p.pos,vel,[p.hotbar[p.selectedItem].name,p.hotbar[p.selectedItem].tags],stats,20,p.hotbar[p.selectedItem].imgIndex)
                  else:
                      stats["damaging"]=True
                      stats["dropammo"]=True
                      Projectile(p.pos,vel,[p.hotbar[p.selectedItem].name,p.hotbar[p.selectedItem].tags],stats,20,p.hotbar[p.selectedItem].imgIndex) 
                  p.hotbar[p.selectedItem].amnt-=1
                  if p.hotbar[p.selectedItem].amnt==0:
                      p.hotbar[p.selectedItem]=None
              if "potion" in tags:
                  if p.hotbar[p.selectedItem].name=="greater healing potion":
                      p.hp+=100
                      damagePopUps.append([100,(0,230,0),100,(p.pos[0],p.pos[1]-80)])
                  if p.hotbar[p.selectedItem].name=="lesser healing potion":
                      p.hp+=50
                      damagePopUps.append([50,(0,230,0),100,(p.pos[0],p.pos[1]-80)])
                  if p.hp>p.maxhp:
                      p.hp=p.maxhp
                  p.hotbar[p.selectedItem].amnt-=1
                  if p.hotbar[p.selectedItem].amnt==0:
                      p.hotbar[p.selectedItem]=None
              if "bow" in tags:
                  for i in range(len(p.hotbar[p.selectedItem].name)):
                   if p.hotbar[p.selectedItem].name[i]==" ":
                      toolset=p.hotbar[p.selectedItem].name[:i]
                      break
                  baseDmg=random.randint(bowBaseDamages[toolset][0],bowBaseDamages[toolset][1])
                  if p.getItemAmnt("wooden arrow")>0:
                      p.changeItem("wooden arrow",-1)
                      angle=math.atan2(p.pos[1]-CAM.pos[1]-m[1],p.pos[0]-CAM.pos[0]-m[0])
                      vel=(-math.cos(angle)*20,-math.sin(angle)*20)
                      damages=baseItemDamages["wooden arrow"]
                      damage=random.randint(damages[0],damages[1])+baseDmg
                      stats["damage"]=damage
                      stats["dropammo"]=True
                      stats["damaging"]=True
                      if random.randint(0,100)<100*baseItemCritChance["wooden arrow"]:
                          stats["damage"]*=2
                          stats["crit"]=True
                      Projectile(p.pos,vel,["wooden arrow",["arrow","projectile"]],stats,20,153)
              if "staff" in tags:
                  stats["age"]=True
                  stats["life"]=200
                  stats["damaging"]=True
                  stats["air resistance"]=1
                  angle=math.atan2(p.pos[1]-CAM.pos[1]-m[1],p.pos[0]-CAM.pos[0]-m[0])
                  vel=(-math.cos(angle)*6,-math.sin(angle)*6)
                  stats["gravity"]=0
                  if random.randint(0,100)<10:
                      damageMult=2
                      stats["crit"]=True
                  else:
                      damageMult=1
                  if p.hotbar[p.selectedItem].name=="ruby staff":
                      stats["damage"]=random.randint(14,17)*damageMult
                      Projectile(p.pos,vel,["bolt",[]],stats,20,74)
                  elif p.hotbar[p.selectedItem].name=="amethyst staff":
                      stats["damage"]=random.randint(8,11)*damageMult
                      Projectile(p.pos,vel,["bolt",[]],stats,20,75)
                  elif p.hotbar[p.selectedItem].name=="topaz staff":
                      stats["damage"]=random.randint(10,14)*damageMult
                      Projectile(p.pos,vel,["bolt",[]],stats,20,76)
                  elif p.hotbar[p.selectedItem].name=="sapphire staff":
                      stats["damage"]=random.randint(17,20)*damageMult
                      Projectile(p.pos,vel,["bolt",[]],stats,20,77)
                  elif p.hotbar[p.selectedItem].name=="diamond staff":
                      stats["damage"]=random.randint(20,23)*damageMult
                      Projectile(p.pos,vel,["bolt",[]],stats,20,78)
                      
                  
              
   else:
      tpressed=False
      t2pressed=False
   if pygame.mouse.get_pressed()[2]:
      if not altpressed:
         altpressed=True
         if p.hotbar[p.selectedItem]!=None:
            tags=p.hotbar[p.selectedItem].tags
         else:tags=[]
         CAM.altclickBlock(m,tags)
   else:
      altpressed=False
   CAM.update()
   p.update()
   updateNPCS()
   updateProjectiles()
   updateWorldItems()
   updateDamagePopUps()
   updateRecentPickups()
   screen.fill((135*globalLighting,206*globalLighting,235*globalLighting))
   #screen.blit(overworldbkg,(0,0))
   CAM.render()
   drawRecentPickups()
   drawDamagePopUps()
   drawProjectiles()
   if p.alive:
       p.draw()
   drawWorldItems()
   drawNPCS()
   if p.alive:
       p.drawHotbar()
       p.drawHP()
       if p.showInventory:
          p.updateInventory()
          p.drawCraftableItems()
          p.drawInventory()
   fps=clock.get_fps()
   text=font.render(str(int(fps))+"fps  "+str(int(p.pos[0]//BLOCKSIZE))+"x "+str(int(p.pos[1]//BLOCKSIZE))+"y",True,(255,255,255))
   screen.blit(text,(screenW-180,0))
   #screen.blit(surf,(300,300))
   #img=pygame.transform.rotate(itemImages[109],gameTick)
   #screen.blit(img,(300,300))
   #globalLighting=math.sin(gameTick/100)/2.5+0.5
   for event in pygame.event.get():
       if event.type==QUIT:
          pygame.quit()
          sys.exit()
       if event.type==KEYDOWN:
          if event.key==K_ESCAPE:
             if p.showInventory:
                p.showInventory=False
                p.chestItems=None
                p.chestOpen=False
                itemPos=None
             else:
                p.showInventory=True
                p.craftingMenuPos=600
                p.updateCraftableItems()
          if event.key==K_a:
             movingLeft=True
             stopLeft=False
          if event.key==K_d:
             movingRight=True
             stopRight=False
          if event.key==K_s:
             movingDown=True
          if event.key==K_j:
             p.pos=spawnPoint
             print("respawning...")
          if event.key==K_h:
              if showHitBoxes:
                  showHitBoxes=False
              else:
                  showHitBoxes=True
          if event.key==K_u:
              p.kill()
          if event.key==K_o:
             num=random.randint(0,4)
             if num==0:
                WorldItem("gold",random.randint(10,20),(p.pos[0],p.pos[1]-200))
             elif num==1:
                WorldItem("silver",random.randint(10,20),(p.pos[0],p.pos[1]-200))
             elif num==2:
                WorldItem("iron",random.randint(10,20),(p.pos[0],p.pos[1]-200))
             elif num==3:
                WorldItem("lead",random.randint(10,20),(p.pos[0],p.pos[1]-200))
             else:
                WorldItem("copper",random.randint(10,20),(p.pos[0],p.pos[1]-200))
          if event.key==K_i:
             num=random.randint(0,4)
             if num==0:
                WorldItem("ruby",random.randint(3,10),(p.pos[0],p.pos[1]-200))
             elif num==1:
                WorldItem("diamond",random.randint(3,10),(p.pos[0],p.pos[1]-200))
             elif num==2:
                WorldItem("sapphire",random.randint(3,10),(p.pos[0],p.pos[1]-200))
             elif num==3:
                WorldItem("topaz",random.randint(3,10),(p.pos[0],p.pos[1]-200))
             else:
                WorldItem("amethyst",random.randint(3,10),(p.pos[0],p.pos[1]-200))
          if event.key==K_f:
             WorldItem("cobble furnace",1,(p.pos[0],p.pos[1]-200))
          if event.key==K_k:
             WorldItem("gold chest",1,(p.pos[0],p.pos[1]-200))
          if event.key==K_l:
             WorldItem("diamond staff",1,(p.pos[0],p.pos[1]-200))
          if event.key==K_m:
             num=random.randint(0,2)
             if num==0:
                WorldItem("gold coin",1,(p.pos[0],p.pos[1]-200))
             elif num==1:
                WorldItem("silver coin",1,(p.pos[0],p.pos[1]-200))
             elif num==2:
                WorldItem("copper coin",1,(p.pos[0],p.pos[1]-200))
          if event.key==K_p:
             WorldItem("gold pickaxe",1,(p.pos[0],p.pos[1]-200))
          if event.key==K_w or event.key==K_SPACE:
             if p.grounded:
                p.vel=(p.vel[0],-BLOCKSIZE/3.4)
          if event.key==K_1:p.selectedItem=0
          if event.key==K_2:p.selectedItem=1
          if event.key==K_3:p.selectedItem=2
          if event.key==K_4:p.selectedItem=3
          if event.key==K_5:p.selectedItem=4
          if event.key==K_6:p.selectedItem=5
          if event.key==K_7:p.selectedItem=6
          if event.key==K_8:p.selectedItem=7
          if event.key==K_9:p.selectedItem=8
          if event.key==K_0:p.selectedItem=9
       if event.type==KEYUP:
          if event.key==K_a:
             movingLeft=False
          if event.key==K_d:
             movingRight=False
          if event.key==K_s:
             movingDownTimer=10
       if event.type==MOUSEBUTTONDOWN:
          if event.button==4:
             if p.showInventory:
                 p.craftingMenuVel+=5
                 p.craftingSlotDelay=15
             else:
                 if p.selectedItem>0:
                    p.selectedItem-=1
                 else:
                    p.selectedItem=9
          if event.button==5: 
             if p.showInventory:
                 p.craftingMenuVel-=5
                 p.craftingSlotDelay=15
             else:
                 if p.selectedItem<9:
                    p.selectedItem+=1
                 else:
                    p.selectedItem=0
   clock.tick(60)
   #pygame.display.update()
   pygame.display.flip()
