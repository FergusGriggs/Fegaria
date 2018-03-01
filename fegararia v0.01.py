import pygame, sys, math, time, os, random, noise
from pygame.locals import *
pygame.init()
VERSION=0.01
screenObj=pygame.display.Info()
screenW=screenObj.current_w
screenH=screenObj.current_h
screenW,screenH=1200,1000
screen=pygame.display.set_mode((screenW,screenH))#,FULLSCREEN)
pygame.display.set_caption('fegararia'+" v"+str(VERSION))

overworldbkg=pygame.transform.scale(pygame.image.load("Textures/overworldbkg.png"),(screenW,screenH))

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
def assembleInventoryBack():
   global inventoryback
   inventoryback=pygame.Surface((610,243))
   pygame.draw.rect(inventoryback,(150,150,150),Rect(0,0,610,243),0)
   for i in range(10):
      for j in range(4):
         pygame.draw.rect(inventoryback,(200,200,200),Rect(i*61,j*61,60,60),5)
   inventoryback.set_alpha(200)
def loadCharacterAnimation():
   global characterFrames
   characterimages=pygame.transform.scale(pygame.image.load("Textures/player tilesheet.png"),(BLOCKSIZE*4,BLOCKSIZE*4))
   characterimages.set_colorkey((255,0,255))
   characterFrames=[]
   for i in range(2):
      for j in range(4):
         surf=pygame.Surface((BLOCKSIZE,BLOCKSIZE*2))
         surf.set_colorkey((255,0,255))
         surf.blit(characterimages,(-j*BLOCKSIZE,-i*BLOCKSIZE*2))
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
class WorldItem():
   def __init__(self,name,tags,amnt,pos):
      global worldItems
      self.name=name
      self.tags=tags
      self.imgIndex=getItemImgIndex(name)
      self.pos=(pos[0]-BLOCKSIZE/3,pos[1]-BLOCKSIZE/3)
      self.rect=Rect(pos[0]-BLOCKSIZE/3,pos[1]-BLOCKSIZE/3,BLOCKSIZE/1.5,BLOCKSIZE/1.5)
      self.vel=(random.random()*0.5-0.25,random.random()-2)
      self.age=0
      self.amnt=amnt
      worldItems.append(self)
   def update(self):
      global worldItems
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
            if mapData[blockpos[1]+j-1-CHUNKSIZE][blockpos[0]+i-1-CHUNKSIZE][0]>0:
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
      if p.rect.colliderect(self.rect):
         p.addItem(self.name,self.tags,self.amnt,self.imgIndex)
         worldItems.remove(self)
   def draw(self):
      screen.blit(itemImages[self.imgIndex],(int(self.rect.left-CAM.pos[0]),int(self.rect.top-CAM.pos[1])))
class Item():
   def __init__(self,name,tags,amnt,imgIndex):
      self.name=name
      self.tags=tags
      self.amnt=amnt
      self.imgIndex=imgIndex
      
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
         ore(1,6,None,(300,425),None)
      for i in range(int(CHUNKNUMX*CHUNKNUMY/4)):#lower stone
         ore(1,6,None,(425,500),None,1)
      for i in range(int(CHUNKNUMX*CHUNKNUMY/4)):#boarder stone
         ore(1,6,None,(500,500),None,1)
      val=random.randint(50,CHUNKSIZE*CHUNKNUMX-50)
      print("Spawning sand...")
##      for i in range(1):#add desert
##         ore(18,15,None,(300,500),(val-50,val+50),18)
      print("Spawning Ores...")
      for i in range(int(CHUNKNUMX*CHUNKNUMY/3)):#coal
         ore(34,4,None,None,None)
      for i in range(int(CHUNKNUMX*CHUNKNUMY/6)):#iron
         ore(33,3,None,None,None)
      for i in range(int(CHUNKNUMX*CHUNKNUMY/8)):#silver
         ore(35,3,None,(450,CHUNKNUMY*CHUNKSIZE-4),None)
      for i in range(int(CHUNKNUMX*CHUNKNUMY/12)):#gold
         ore(32,3,None,(550,CHUNKNUMY*CHUNKSIZE-4),None)
      print("Making Caves...")
      for i in range(int(CHUNKNUMX*CHUNKNUMY/12)):#simple caves
         ore(0,10,None,None,None)
      for i in range(int(CHUNKNUMX*CHUNKNUMY/12)):#bigger lower caves
         ore(0,17,None,(550,CHUNKSIZE*CHUNKNUMY-17),None)
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
         #print(cami,chunk)
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
   def draw(self,offset):
      if self.loaded:
         screen.blit(self.surface,(self.POS[0]-offset[0],self.POS[1]-offset[1]))
   def updateSurface(self):
      self.surface.fill((255,0,255))
      self.surface.set_colorkey((255,0,255))
      for i in range(len(self.blocks)):
         for j in range(len(self.blocks[i])):
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
   def updateLighting(self):
      for i in range(len(self.blocks)):
         for j in range(len(self.blocks[i])):
            self.blocks[i][j].light=globalLighting
      self.updateSurface()
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
      self.light=globalLighting
class Cam():
   def __init__(self,Map,pos):
      self.pos=pos
      self.oldpos=(-1000,-1000)
      self.Map=Map
      self.updateDelay=10
      self.updateTick=0
   def update(self):
##      if self.Map.lightUpdateTick<0:
##         self.Map.lightUpdateTick+=self.Map.lightUpdateDelay
##         for chunk in self.Map.focusChunks:
##            self.Map.chunks[chunk[0]][chunk[1]].updateLighting()
##      else:
##         self.Map.lightUpdateTick-=1
      if self.pos!=self.oldpos:
         if self.updateTick>self.updateDelay:
            self.updateTick-=self.updateDelay
            self.Map.loadChunks(self.pos)
            self.oldpos=self.pos
         else:
            self.updateTick+=1
   def damageBlock(self,val,screenPos,tags):
      global mapData
      try:
         actualPos=(screenPos[0]+int(self.pos[0]),screenPos[1]+int(self.pos[1]))
         chunkPos=(actualPos[0]//(CHUNKSIZE*BLOCKSIZE),actualPos[1]//(CHUNKSIZE*BLOCKSIZE))
         inChunkPos=((actualPos[0]-chunkPos[0]*CHUNKSIZE*BLOCKSIZE)//BLOCKSIZE,(actualPos[1]-chunkPos[1]*CHUNKSIZE*BLOCKSIZE)//BLOCKSIZE)
         if "pickaxe" in tags:
            if CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].val>0:
               if CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].integrity>0:
                  CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].integrity-=val
                  CAM.Map.chunks[chunkPos[1]][chunkPos[0]].updateSurface()
                  if CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].integrity<=0:
                     info = getInfoFromVal(CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].val)
                     CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].val=0
                     CAM.Map.chunks[chunkPos[1]][chunkPos[0]].updateSurface()
                     WorldItem(info[0],info[1],1,(chunkPos[0]*CHUNKSIZE*BLOCKSIZE+inChunkPos[0]*BLOCKSIZE+2/3*BLOCKSIZE,chunkPos[1]*CHUNKSIZE*BLOCKSIZE+inChunkPos[1]*BLOCKSIZE+2/3*BLOCKSIZE))
                     mapData[(actualPos[1]//BLOCKSIZE)-CHUNKSIZE][(actualPos[0]//BLOCKSIZE)-CHUNKSIZE][0]=0
         if "axe" in tags:
            backval=CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].backval
            if backval==19 or backval==20:
               CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].backintegrity-=val
               CAM.Map.chunks[chunkPos[1]][chunkPos[0]].updateSurface()
               if CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].backintegrity<=0:
                  CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].backval=0
                  WorldItem("wood",["material","block"],random.randint(2,3),(chunkPos[0]*CHUNKSIZE*BLOCKSIZE+inChunkPos[0]*BLOCKSIZE+2/3*BLOCKSIZE,chunkPos[1]*CHUNKSIZE*BLOCKSIZE+inChunkPos[1]*BLOCKSIZE+2/3*BLOCKSIZE))
                  CAM.Map.chunks[chunkPos[1]][chunkPos[0]].updateSurface()
                  pos=((actualPos[0]//BLOCKSIZE)-CHUNKSIZE,(actualPos[1]//BLOCKSIZE)-CHUNKSIZE-1)
                  chunksVisited=[]
                  for i in range(20):
                     if mapData[pos[1]][pos[0]][1]==20 or mapData[pos[1]][pos[0]][1]==21:
                        mapData[pos[1]][pos[0]][1]=0
                        bchunkPos=(pos[0]//CHUNKSIZE+1,pos[1]//CHUNKSIZE+1)
                        if bchunkPos not in chunksVisited:
                           chunksVisited.append(bchunkPos)
                        binChunkPos=(pos[0]-bchunkPos[0]*CHUNKSIZE,pos[1]-bchunkPos[1]*CHUNKSIZE)
                        CAM.Map.chunks[bchunkPos[1]][bchunkPos[0]].blocks[binChunkPos[0]][binChunkPos[1]].backval=0
                        WorldItem("wood",["material","block"],random.randint(2,3),((pos[0]+CHUNKSIZE)*BLOCKSIZE+BLOCKSIZE,(pos[1]+CHUNKSIZE)*BLOCKSIZE+BLOCKSIZE))
                        pos=(pos[0],pos[1]-1)
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
      except:print("mouse off screen")
   def placeBlock(self,name,screenPos):
      global mapData
      actualPos=(screenPos[0]+int(self.pos[0]),screenPos[1]+int(self.pos[1]))
      blockpos=(actualPos[0]//BLOCKSIZE,actualPos[1]//BLOCKSIZE)
      if not Rect(p.pos[0]-CAM.pos[0]-BLOCKSIZE/2,p.pos[1]-CAM.pos[1]-BLOCKSIZE,BLOCKSIZE,BLOCKSIZE*2).colliderect(Rect(blockpos[0]*BLOCKSIZE-CAM.pos[0],blockpos[1]*BLOCKSIZE-CAM.pos[1],BLOCKSIZE,BLOCKSIZE)):
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
                CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].val=val
                integ=getIntegFromVal(val)
                CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].integrity=integ
                CAM.Map.chunks[chunkPos[1]][chunkPos[0]].blocks[inChunkPos[0]][inChunkPos[1]].maxintegrity=integ
                CAM.Map.chunks[chunkPos[1]][chunkPos[0]].updateSurface()
                mapData[(actualPos[1]//BLOCKSIZE)-CHUNKSIZE][(actualPos[0]//BLOCKSIZE)-CHUNKSIZE][0]=val
                return True
      return False
      
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
      self.movespeed=movespeed
      self.rect=Rect(pos[0]-BLOCKSIZE/2,pos[1]-BLOCKSIZE,BLOCKSIZE,BLOCKSIZE*2)
      self.animationFrame=0
      self.direction=0
      self.animationTick=0
      self.groundedTick=0
      self.grounded=False
      self.hotbar=[None for i in range(10)]
      self.inventory=[[None for i in range(4)]for i in range(10)]
      self.showInventory=False
      self.selectedItem=0
   def drawHotbar(self):
      screen.blit(hotbarback,(10,10))
      for i in range(10):
         if self.hotbar[i]!=None:
            screen.blit(hotbarItemImages[self.hotbar[i].imgIndex],(22+i*61,20))
            if "tool" not in self.hotbar[i].tags:
                text=font.render(str(self.hotbar[i].amnt),True,(255,255,255))
                screen.blit(text,(50+i*61-text.get_width()/2,40))
      pygame.draw.rect(screen,(255,255,0),Rect(10+self.selectedItem*61,10,60,60),5)
   def drawInventory(self):
      screen.blit(inventoryback,(10,80))
      for i in range(10):
         for j in range(4):
            if self.inventory[i][j]!=None:
               screen.blit(hotbarItemImages[self.inventory[i][j].imgIndex],(22+i*61,90+j*61))
               if "tool" not in self.inventory[i][j].tags:
                   text=font.render(str(self.inventory[i][j].amnt),True,(255,255,255))
                   screen.blit(text,(50+i*61-text.get_width()/2,110+j*61))
      if pressed:
         drawHoldingItem()
   def updateInventory(self):
      global itemHolding, pressed, itemPos
      if pygame.mouse.get_pressed()[0]:
         if Rect(10,10,610,313).collidepoint(pygame.mouse.get_pos()):
            if not pressed:
               for i in range(10):
                  if Rect(10+i*61,10,61,61).collidepoint(pygame.mouse.get_pos()):
                     itemHolding=self.hotbar[i]
                     itemPos=["h",i]
                     self.hotbar[i]=None
                     pressed=True
               for i in range(10):
                  for j in range(4):
                     if Rect(10+i*61,70+j*61,61,61).collidepoint(pygame.mouse.get_pos()):
                        itemPos=["i",(i,j)]
                        itemHolding=self.inventory[i][j]
                        self.inventory[i][j]=None
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
                              self.addItem(self.hotbar[i].name,self.hotbar[i].tags,self.hotbar[i].amnt-999,self.hotbar[i].imgIndex)
                              self.hotbar[i].amnt=999
                     else:
                        putItemBack(self.hotbar[i])
                        self.hotbar[i]=itemHolding
                  found=True
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
                                    self.addItem(self.inventory[i][j].name,self.inventory[i][j].tags,self.inventory[i][j].amnt-999,self.inventory[i][j].imgIndex)
                                    self.inventory[i][j].amnt=999
                           else:
                              putItemBack(self.inventory[i][j])
                              self.inventory[i][j]=itemHolding
                        found=True
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
   def addItem(self,name,tags,amnt,imgIndex):#check hotbar and inventory for item, then use empty spaces
      for i in range(10):
         if self.hotbar[i]!=None:
            if self.hotbar[i].name==name:
               if p.hotbar[i].amnt<999:
                  p.hotbar[i].amnt+=amnt
                  if p.hotbar[i].amnt>999:
                     amnt=p.hotbar[i].amnt-999
                     p.hotbar[i].amnt=999
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
                     else:
                        return
      for i in range(10):
         if self.hotbar[i]==None:
            self.hotbar[i]=Item(name,tags,amnt,imgIndex)
            return
      for i in range(10):
         for j in range(4):
            if self.inventory[i][j]==None:
               self.inventory[i][j]=Item(name,tags,amnt,imgIndex)
               return
   def update(self):
      global stopRight, stopLeft
      if self.grounded:
         if self.groundedTick<0:
            self.groundedTick+=7
            self.grounded=False
            stopRight=False
            stopLeft=False
         else:
            self.groundedTick-=1
            
      if movingRight:
         if not stopRight:
            self.direction=0
            self.updateAnimationFrame()
            self.vel=(self.vel[0]+1,self.vel[1])
      if movingLeft:
         if not stopLeft:
            self.direction=1
            self.updateAnimationFrame()
            self.vel=(self.vel[0]-1,self.vel[1])
      if not movingLeft and not movingRight:
         self.animationFrame=0
      if self.vel[0]<-self.movespeed:
         self.vel=(-self.movespeed,self.vel[1])
      if self.vel[0]>self.movespeed:
         self.vel=(self.movespeed,self.vel[1])
      self.vel=(self.vel[0]*0.95,self.vel[1]*0.99+0.2)
      self.pos=(self.pos[0]+self.vel[0],self.pos[1]+self.vel[1])
      self.blockpos=(math.floor(self.pos[0]//BLOCKSIZE),math.floor(self.pos[1]//BLOCKSIZE))
      for i in range(3):
         for j in range(3):
            try:
               if mapData[self.blockpos[1]+j-1-CHUNKSIZE][self.blockpos[0]+i-1-CHUNKSIZE][0]>0:
                  blockrect=Rect(BLOCKSIZE*(self.blockpos[0]+i-1),BLOCKSIZE*(self.blockpos[1]+j-1),BLOCKSIZE,BLOCKSIZE)
                  if blockrect.colliderect(self.rect):
                     deltaX = self.pos[0]-blockrect.centerx
                     deltaY = self.pos[1]-blockrect.centery
                     if abs(deltaX) > abs(deltaY):
                         if deltaX > 0:
                             self.pos=(blockrect.right+BLOCKSIZE/2,self.pos[1])
                             self.vel=(0,self.vel[1])
                             stopLeft=True
                         else:
                             self.pos=(blockrect.left-BLOCKSIZE/2,self.pos[1])
                             self.vel=(0,self.vel[1])
                             stopRight=True
                     else:
                         if deltaY > 0:
                             self.pos=(self.pos[0],blockrect.bottom+BLOCKSIZE)
                             if self.vel[1]<0:
                                self.vel=(self.vel[0],0)
                         else:
                            self.pos=(self.pos[0],blockrect.top-BLOCKSIZE)
                            if self.vel[1]>0:
                               self.vel=(self.vel[0]*0.5,0)
                            self.grounded=True
            except:print("player out of map")
      self.rect.left=self.pos[0]-BLOCKSIZE/2
      self.rect.top=self.pos[1]-BLOCKSIZE
   def draw(self):
      screen.blit(characterFrames[self.animationFrame+self.direction*4],(int(self.rect.left-CAM.pos[0]),int(self.rect.top-CAM.pos[1])))
def distance(p1,p2):
   return math.sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)
def putItemBack(item):
   if itemPos[0]=="i":
      p.inventory[itemPos[1][0]][itemPos[1][1]]=item
   else:
      p.hotbar[itemPos[1]]=item
def tree(pos):
   global mapData
   for i in range(1000):
      pos=(pos[0],pos[1]+1)
      try:
         if mapData[pos[1]+1][pos[0]][0]==3:
            if mapData[pos[1]][pos[0]][1]!=19:
               mapData[pos[1]][pos[0]][1]=19
               exitloop=False
               for i in range(12):
                  pos=(pos[0],pos[1]-1)
                  mapData[pos[1]][pos[0]][1]=20
                  if random.randint(0,15)==15 or i==11:
                     mapData[pos[1]][pos[0]][1]=21
                     break
               break
      except:None
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
   if name=="stone":return 16
   if name=="iron":return 210
   if name=="coal":return 194
   if name=="silver":return 178
   if name=="gold":return 162
   if name=="copperPickaxe":return 106
   if name=="copperAxe":return 107
   if name=="copperHammer":return 108
   if name=="cobble":return 16
def getInfoFromVal(val):
   if val==1:return ["cobble",["material","block"]]
   if val==4:return ["wood",["material","block"]]
   if val==2 or val==3:return ["dirt",["material","block"]]
   if val==32:return ["gold",["ore"]]
   if val==33:return ["iron",["ore"]]
   if val==34:return ["coal",["material"]]
   if val==16:return ["cobble",["block"]]
   if val==35:return ["silver",["ore"]]
def getValFromName(name):
   if name=="stone":return 1
   if name=="dirt":return 2
   if name=="cobble":return 16
   if name=="wood":return 4
def getIntegFromVal(val):
   if val==1:return 100
   if val==2 or val==3:return 75
   if val==32:return 200
   if val==33:return 175
   if val==34:return 150
   if val==35:return 150
   if val==16:return 100
   if val==19:return 500
   if val==20:return 500
   if val==4:return 150

font=pygame.font.Font("Fonts\ARCADECLASSIC.TTF",20)
clock=pygame.time.Clock()
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

globalLighting=1

worldItems=[]

stopRight=False
stopLeft=False
movingRight=False
movingLeft=False

pressed=False
itemHolding=None
itemPos=[]

print("Loading images...")

loadTileImages()
loadBackTileImages()
loadCharacterAnimation()
loadHotbarImages()
assembleHotbarBack()
assembleInventoryBack()
loadItemImages()
loadLightingImages()

print("Initailizing Objects...")
spawnPoint=(BLOCKSIZE*CHUNKNUMX*CHUNKSIZE/2,BLOCKSIZE*395)
CAM=Cam(Map(CHUNKNUMX,CHUNKNUMY,CHUNKSIZE,BLOCKSIZE),(spawnPoint[0]-screenW/2,spawnPoint[1]))
p=Player(spawnPoint,100,4)
print("Generating terrain...")
CAM.Map.generateTerrain(0)
#CAM.Map.loadTerrain(0)

print("Giving tools...")

p.hotbar[0]=Item("copperPickaxe",["pickaxe","tool"],1,106)
p.hotbar[1]=Item("copperAxe",["axe","tool"],1,107)
p.hotbar[2]=Item("copperHammer",["hammer","tool"],1,108)


print("Done! (In",pygame.time.get_ticks()/1000,"seconds!)")
while 1:
   gameTick=pygame.time.get_ticks()
   CAM.pos=(CAM.pos[0]+(p.pos[0]-screenW/2-CAM.pos[0])*0.05,CAM.pos[1]+(p.pos[1]-screenH/2-CAM.pos[1])*0.05)
   rel=pygame.mouse.get_rel()
   m=pygame.mouse.get_pos()
   if pygame.mouse.get_pressed()[2]:    
      CAM.pos=(CAM.pos[0]-rel[0],CAM.pos[1]-rel[1])
   if p.pos[0]<LEFTBOARDER:
      p.pos=(LEFTBOARDER,p.pos[1])
   elif p.pos[0]>RIGHTBOARDER:
      p.pos=(RIGHTBOARDER,p.pos[1])
   if CAM.pos[0]<LEFTBOARDER-BLOCKSIZE/2:
      CAM.pos=(LEFTBOARDER-BLOCKSIZE/2,CAM.pos[1])
   elif CAM.pos[0]>RIGHTBOARDER+BLOCKSIZE/2-screenW:
      CAM.pos=(RIGHTBOARDER+BLOCKSIZE/2-screenW,CAM.pos[1])
   if pygame.mouse.get_pressed()[0]:
      if distance((p.pos[0]-CAM.pos[0],p.pos[1]-CAM.pos[1]),m)<PLAYERREACH:
          if p.hotbar[p.selectedItem]!=None:
             tags=p.hotbar[p.selectedItem].tags
             CAM.damageBlock(5,m,tags)
             if "block" in tags:
                if CAM.placeBlock(p.hotbar[p.selectedItem].name,m):
                   p.hotbar[p.selectedItem].amnt-=1
                   if p.hotbar[p.selectedItem].amnt<=0:
                      p.hotbar[p.selectedItem]=None
   CAM.update()
   p.update()
   updateWorldItems()
   screen.fill((135*globalLighting,206*globalLighting,235*globalLighting))
   #screen.blit(overworldbkg,(0,0))
   CAM.render()
   p.draw()
   drawWorldItems()
   p.drawHotbar()
   if p.showInventory:
      p.drawInventory()
      p.updateInventory()
   fps=clock.get_fps()
   text=font.render(str(int(fps))+"fps  "+str(int(p.pos[0]//BLOCKSIZE))+"x "+str(int(p.pos[1]//BLOCKSIZE))+"y",True,(255,255,255))
   screen.blit(text,(1000,10))
   #globalLighting=math.sin(gameTick/1000)/2.5+0.5
   for event in pygame.event.get():
       if event.type==QUIT:
          pygame.quit()
          sys.exit()
       if event.type==KEYDOWN:
          if event.key==K_ESCAPE:
             if p.showInventory:
                p.showInventory=False
             else:
                p.showInventory=True
          if event.key==K_a:
             movingLeft=True
             stopLeft=False
          if event.key==K_d:
             movingRight=True
             stopRight=False
          if event.key==K_f:
             for i in range(19):
                WorldItem("cobble",["material","block"],5,(p.pos[0],p.pos[1]-200))
          if event.key==K_h:
             p.pos=spawnPoint
          if event.key==K_w or event.key==K_SPACE:
             if p.grounded:
                p.vel=(p.vel[0],-BLOCKSIZE/4)
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
       if event.type==MOUSEBUTTONDOWN:
          if event.button==4:
             if p.selectedItem>0:
                p.selectedItem-=1
             else:
                p.selectedItem=9
          if event.button==5: 
             if p.selectedItem<9:
                p.selectedItem+=1
             else:
                p.selectedItem=0
   clock.tick(60)
   #pygame.display.update()
   pygame.display.flip()
