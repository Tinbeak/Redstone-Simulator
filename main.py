import pygame
from classes import *
from textures import *

pygame.init()
clock = pygame.time.Clock()

world = World(5,5,5)#x,y,z size
world.createLayout()

#Fills the bottom layer with light blue wool
x = 0
for row in world.layout[0]:
  z = 0
  for block in row:
    world.setBlock(Wool((x,0,z),"light blue"))
    z += 1
  x += 1
  
def gamePos_to_screenPos(block):#In game position to screen position
  return (50+block.pos[0]*100,50+block.pos[2]*100)

def renderLayer(layer):#Blits a layer to the screen
  for row in layer:
    for block in row:
      if block.texture != None:
        block.updateTexture()
        screen.blit(block.texture,gamePos_to_screenPos(block))
      else:
        screen.blit(grid_square,gamePos_to_screenPos(block))

def renderShadow(layer):#Blits a shadow layer to the screen
  for row in layer:
    for block in row:
      if block.texture != None:
        screen.blit(shadow,gamePos_to_screenPos(block))

def renderHotbar(hand):
  hotbar = {
    1:Wool((0,0,0),"orange").texture,
    2:Dust((0,0,0)).texture,
    3:Repeater((0,0,0)).texture,
    4:Comparator((0,0,0)).texture,
    5:Torch((0,0,0)).texture,
    6:Lever((0,0,0)).texture,
    7:Button((0,0,0)).texture,
    8:Lamp((0,0,0)).texture,
    9:Air((0,0,0)).texture
  }
  hotbar_grid = grid_square
  hotbar_grid = pygame.transform.scale(hotbar_grid,(55,55))
  hotbar_grid.set_colorkey((255,255,255))
  for i in range(1,10):
    screen.blit(hotbar_grid,(600,50+(i-1)*55))
    if i == hand:
      screen.blit(hotbar_hand,(600-10,45+(i-1)*55))
    if hotbar[i] != None:
      item = pygame.transform.scale(hotbar[i],(50,50))
      screen.blit(item,(600,55+(i-1)*55))
  
hotbar_controls = {
  1:pygame.K_1,
  2:pygame.K_2,
  3:pygame.K_3,
  4:pygame.K_4,
  5:pygame.K_5,
  6:pygame.K_6,
  7:pygame.K_7,
  8:pygame.K_8,
  9:pygame.K_9
}
font = pygame.font.Font(None, 36)
# pygame setup
running = True
current_layer = 0
hand = 1
while running:
  screen.fill("grey")
  # poll for events
  # pygame.QUIT event means the user clicked X to close your window
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_UP and current_layer < world.ySize-1:
        current_layer += 1
      elif event.key == pygame.K_DOWN and current_layer > 0:
        current_layer -= 1
      for control in hotbar_controls:
        if event.key == hotbar_controls[control]:
          hand = control
      
  
  # RENDER YOUR GAME HERE
  if current_layer > 0:
    renderLayer(world.layout[current_layer-1])
    renderShadow(world.layout[current_layer-1])
  renderLayer(world.layout[current_layer])
  renderHotbar(hand)

  #Show mouse co-ords
  mouse_pos = pygame.mouse.get_pos()
  mouse_pos = ((mouse_pos[0]-50)//100,current_layer,(mouse_pos[1]-50)//100)
  if mouse_pos[0] not in range(0,world.xSize) or mouse_pos[1] not in range(0,world.zSize):
    mouse_pos = (0,current_layer,0)
  text = font.render(str(mouse_pos), True, (0, 0, 0))
  text_rect = text.get_rect(topleft=(0, 0))

  screen.blit(text, text_rect)# Draw mouse co-ords
  pygame.display.flip()

  clock.tick(20)

pygame.quit()
