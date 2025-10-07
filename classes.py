import pygame
from textures import *

pygame.init()
compass = {"north":0,"south":180,"east":270,"west":90,"up":0,"down":0}

def updateTorchTexture():
  global on_torch_surface, off_torch_surface
  on_torch_surface = pygame.Surface((100,100), pygame.SRCALPHA)
  pygame.draw.rect(on_torch_surface,(220,0,0),(37.5,37.5,25,25))
  pygame.draw.rect(on_torch_surface,(255,190,0),(42.5,42.5,15,15))
  off_torch_surface = pygame.Surface((100,100), pygame.SRCALPHA)
  off_torch_surface.blit(on_torch_surface,(0,0))
  pygame.draw.rect(off_torch_surface,(145,0,0),(42.5,42.5,15,15))

class Block:
  def __init__(self, pos):
    self.pos = pos
  def updateTexture(self):
    pass
    
class Shadow(Block):
  def __init__(self, pos):
    super().__init__(pos)
    self.type = "shadow"
    self.texture = shadow

class Air(Block):
  def __init__(self, pos):
    super().__init__(pos)
    self.texture = None
    self.type = "air"
    self.canfloat = True
    self.solid = False
    self.orientation = None
    
class Wool(Block):
  def __init__(self, pos, colour):
    super().__init__(pos)
    self.colour = colour
    self.texture = wool_colour_to_texture[self.colour]
    self.type = "wool"
    self.canfloat = True
    self.solid = True
    self.orientation = None
    
class Dust(Block):
  def __init__(self, pos):
    self.pos = pos
    self.type = "dust"
    self.canfloat = False
    self.solid = False
    self.orientation = "north"
    self.onDelay = 0 #Delay in redstone ticks (10 ticks = 1 second)
    self.offDelay = 0
    self.powered = False
    self.strength = 0
    self.state = "cross"#Can be line, cross, T, L 
    self.updateTexture()
  
  def updateTexture(self):
    font = pygame.font.Font(None, 25)
    self.colour = (145+(self.strength*5),0,0)
    red_mid = pygame.Rect(35,35,30,30)
    text = font.render(str(self.strength),True,(0,0,0))
    text_rect = text.get_rect(center=red_mid.center)

    cross_surface = pygame.Surface((100,100), pygame.SRCALPHA)
    pygame.draw.rect(cross_surface,self.colour,(40,0,20,100))
    pygame.draw.rect(cross_surface,self.colour,(0,40,100,20))
    pygame.draw.rect(cross_surface,self.colour,red_mid)
    cross_surface.blit(text,text_rect)

    line_surface = pygame.Surface((100,100), pygame.SRCALPHA)
    pygame.draw.rect(line_surface,self.colour,(40,0,20,100))
    pygame.draw.rect(line_surface,self.colour,red_mid)
    line_surface.blit(text,text_rect)

    T_surface = pygame.Surface((100,100), pygame.SRCALPHA)
    pygame.draw.rect(T_surface,self.colour,(40,0,20,50))
    pygame.draw.rect(T_surface,self.colour,(0,40,100,20))
    pygame.draw.rect(T_surface,self.colour,red_mid)
    T_surface.blit(text,text_rect)

    L_surface = pygame.Surface((100,100), pygame.SRCALPHA)
    pygame.draw.rect(L_surface,self.colour,(40,0,20,50))
    pygame.draw.rect(L_surface,self.colour,(0,40,50,20))
    pygame.draw.rect(L_surface,self.colour,red_mid)
    L_surface.blit(text,text_rect)

    texture_dict = {"cross":cross_surface,"line":line_surface,"T":T_surface,"L":L_surface}
    self.texture = texture_dict[self.state]
    self.texture = pygame.transform.rotate(self.texture,compass[self.orientation])

class Torch(Block):
  def __init__(self, pos, orientation="up"):#Can be up,N,S,E,W
    super().__init__(pos)
    self.type = "torch"
    self.canfloat = False
    self.solid = False
    self.orientation = orientation
    self.on = True
    self.onDelay = 1
    self.offDelay = 1
    self.updateTexture()
  def updateTexture(self):
    updateTorchTexture()
    if self.on:
      self.texture = on_torch_surface
    else:
      self.texture = off_torch_surface
    if self.orientation in ["north","south","east","west"]:
      pygame.draw.rect(self.texture,(139,69,19),(42.5,62.5,15,37.5))
    self.texture = pygame.transform.rotate(self.texture,compass[self.orientation])
    
class Repeater(Block):
  def __init__(self, pos, orientation="north"):
    super().__init__(pos)
    self.type = "repeater"
    self.canfloat = False
    self.solid = False
    self.orientation = orientation
    self.locked = False
    self.powered = False
    self.delay = 1
    self.onDelay = self.delay
    self.offDelay = self.delay
    self.updateTexture()
  def updateTexture(self):
    updateTorchTexture()
    repeater_surface = pygame.Surface((100,100), pygame.SRCALPHA)
    repeater_surface.blit(repeater_texture,(0,0))
    if self.powered:
      repeater_surface.blit(on_torch_surface,(0,-30))
      if self.locked:
        pygame.draw.rect(repeater_surface,(0,0,0),(12.5,5+10*(self.delay+3),75,100/8))
      else:
        repeater_surface.blit(on_torch_surface,(0,10*(self.delay-1)))
    else:
      repeater_surface.blit(off_torch_surface,(0,-30))
      if self.locked:
        pygame.draw.rect(repeater_surface,(0,0,0),(12.5,5+10*(self.delay+3),75,100/8))
      else:
        repeater_surface.blit(off_torch_surface,(0,10*(self.delay-1)))
    self.texture = repeater_surface
    self.texture = pygame.transform.rotate(self.texture,compass[self.orientation])
    
class Comparator(Block):
  def __init__(self, pos, orientation="north"):#Can be N,S,E,W
    super().__init__(pos)
    self.type = "comparator"
    self.canfloat = False
    self.solid = False
    self.orientation = orientation
    self.powered = False
    self.onDelay = 1
    self.offDelay = 1
    self.mode = "compare"
    self.updateTexture()
  def updateTexture(self):
    updateTorchTexture()
    comparator_surface = pygame.Surface((100,100), pygame.SRCALPHA)
    comparator_surface.blit(comparator_texture,(0,0))
    if self.mode == "compare":
      comparator_surface.blit(off_torch_surface,(0,-30))
    elif self.mode == "subtract":
      comparator_surface.blit(on_torch_surface,(0,-30))
    if self.powered:
      comparator_surface.blit(on_torch_surface,(-25,25))
      comparator_surface.blit(on_torch_surface,(25,25))
    else:
      comparator_surface.blit(off_torch_surface,(-25,25))
      comparator_surface.blit(off_torch_surface,(25,25))
    self.texture = comparator_surface
    self.texture = pygame.transform.rotate(self.texture,compass[self.orientation])

class Lever(Block):
  def __init__(self, pos, orientation="up"):#Can be up,N,S,E,W
    super().__init__(pos)
    self.type = "lever"
    self.canfloat = False
    self.solid = False
    self.orientation = orientation
    self.on = False
    self.updateTexture()
  def updateTexture(self):
    lever_surface = pygame.Surface((100,100), pygame.SRCALPHA)
    lever_base = pygame.Rect(25,31.25,50,37.5)
    lever_stick = pygame.Rect(12.5,43.75,25,12.5)
    lever_mid = pygame.Rect(37.5,43.75,25,12.5)
    if self.orientation in ["north","south","east","west"]:
      lever_base = lever_base.move(0,-30)
      lever_stick = lever_stick.move(0,-30)
      lever_mid = lever_mid.move(0,-30)
    pygame.draw.rect(lever_surface,(145,145,145),lever_base)
    if self.on:
      pygame.draw.rect(lever_surface,(220,0,0),lever_mid)
      pygame.draw.rect(lever_surface,(139,69,19),lever_stick.move(50,0))
    else:
      pygame.draw.rect(lever_surface,(75,75,75),lever_mid)
      pygame.draw.rect(lever_surface,(139,69,19),lever_stick)
    self.texture = lever_surface
    self.texture = pygame.transform.rotate(self.texture,compass[self.orientation])

class Button(Block):#Stone button
  def __init__(self, pos, orientation="up"):#Can be up,down,N,S,E,W
    super().__init__(pos)
    self.type = "button"
    self.canfloat = False
    self.solid = False
    self.orientation = orientation
    self.on = False
    self.duration = 10
    self.updateTexture()
  def updateTexture(self):
    button_surface = pygame.Surface((100,100), pygame.SRCALPHA)
    button = pygame.Rect(30,37.5,40,25)
    if self.orientation in ["north","south","east","west"]:
      button = button.move(0,-37.5)
    if self.on:
      pygame.draw.rect(button_surface,(220,0,0),button)
    else:
      pygame.draw.rect(button_surface,(145,145,145),button)
    self.texture = button_surface
    self.texture = pygame.transform.rotate(self.texture,compass[self.orientation])

class Lamp(Block):
  def __init__(self, pos):
    super().__init__(pos)
    self.type = "lamp"
    self.canfloat = True
    self.solid = True
    self.orientation = None
    self.powered = False
    self.onDelay = 0
    self.offDelay = 2
    self.updateTexture()
  def updateTexture(self):
    lamp_surface = pygame.Surface((100,100), pygame.SRCALPHA)
    if self.powered:
      lamp_surface.blit(on_lamp,(0,0))
    else:
      lamp_surface.blit(off_lamp,(0,0))
    self.texture = lamp_surface

class World:
  def __init__(self, xSize, ySize, zSize):
    self.xSize = xSize
    self.ySize = ySize
    self.zSize = zSize
    self.layout = []

  def createLayout(self):
    for y in range(self.ySize):#Creates y axis (up and down)
      self.layout.append([])
      for x in range(self.xSize):#Creates x axis (left and right)
        self.layout[y].append([])
        for z in range(self.zSize):#Creates z axis (forward and backward)
          self.layout[y][x].append(Air((x,y,z)))

  def setBlock(self, block):
    self.layout[block.pos[1]][block.pos[0]][block.pos[2]] = block


