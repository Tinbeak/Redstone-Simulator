import pygame

pygame.init()
screen = pygame.display.set_mode((700, 600))
pygame.display.set_caption("Redstone Simulator")

hotbar_hand = pygame.image.load("Hotbar Square.png")
hotbar_hand = pygame.transform.scale(hotbar_hand,(70,70))
hotbar_hand.set_colorkey((255,255,255))

grid_square = pygame.image.load("Grid Square.png")
grid_square = pygame.transform.scale(grid_square,(100,100))
grid_square.set_colorkey((255,255,255))

shadow = pygame.image.load("Shadow.png").convert_alpha()
shadow.set_alpha(100)
shadow = pygame.transform.scale(shadow,(100,100))
shadow.set_colorkey((255,255,255))

repeater_texture = pygame.image.load("Repeater.png")
repeater_texture = pygame.transform.scale(repeater_texture,(100,100))

comparator_texture = pygame.image.load("Comparator.png")
comparator_texture = pygame.transform.scale(comparator_texture,(100,100))

on_lamp = pygame.image.load("On Lamp.png")
on_lamp = pygame.transform.scale(on_lamp,(100,100))
off_lamp = pygame.image.load("Off Lamp.png")
off_lamp = pygame.transform.scale(off_lamp,(100,100))

red_wool_texture = pygame.image.load("Red Wool.png")
red_wool_texture = pygame.transform.scale(red_wool_texture,(100,100))

light_blue_wool_texture = pygame.image.load("Light Blue Wool.png")
light_blue_wool_texture = pygame.transform.scale(light_blue_wool_texture,(100,100))

orange_wool_texture = pygame.image.load("Orange Wool.png")
orange_wool_texture = pygame.transform.scale(orange_wool_texture,(100,100))

wool_colour_to_texture = {"red":red_wool_texture,"light blue":light_blue_wool_texture,"orange":orange_wool_texture}
