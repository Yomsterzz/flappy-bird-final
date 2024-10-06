import pygame
import random
from pygame.locals import *
from pygame.sprite import Group
pygame.init()

WIDTH = 864
HEIGHT = 936

clock = pygame.time.Clock()
fps = 60
# title_font = pygame.font.SysFont("helvicta", 14)
ground_x = 0
scroll_speed = 4
running = True
game_over = False
flying = False
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks()-1500
pipe_gap = 150

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird") 

bg = pygame.image.load("./images/bg.png")
ground = pygame.image.load("./images/ground.png")

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        
        for i in range(1,4):
            bird = pygame.image.load(f"./images/bird{i}.png")
            self.images.append(bird)
        
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.velocity = 0    
        self.clicked = False
        
    def update(self):
        if flying == True:
            # Gravity
            self.velocity += 0.5
            if self.velocity > 8:
                self.velocity = 8
            
            if self.rect.bottom < 768:
                self.rect.y += int(self.velocity)
            
        if game_over == False:
            # Clicking effect
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.velocity = -10
            
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            
            self.counter += 1
            flap_cooldown = 2
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
        
            self.image = self.images[self.index]
            self.image = pygame.transform.rotate(self.images[self.index], self.velocity * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)
            

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, pos):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("./images/pipe.png")
        self.rect = self.image.get_rect()
        #if pos = 1, pipe is at the top. if pos = -1, pipe is at the bottom.
        if pos == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x,y-int(pipe_gap/2)]
        
        if pos == -1:
            self.rect.topleft = [x,y+int(pipe_gap/2)]
        
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


pipe_group = pygame.sprite.Group()
   
bird_group = pygame.sprite.Group()
bird1 = Bird(int(WIDTH/4), int(HEIGHT/2))     
bird_group.add(bird1)
        
while running:
    clock.tick(fps)

    screen.blit(bg, (0,0))
    
    bird_group.draw(screen)
    bird_group.update()
    
    pipe_group.draw(screen)
    # checking for collison between bird and pipe
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or bird1.rect.top < 0 or bird1.rect.bottom >= 768:
        game_over = True
        flying = False
    
    if flying == True and game_over == False:
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100,100)
            bottom_pipe = Pipe(WIDTH, HEIGHT//2 + pipe_height, -1)
            top_pipe = Pipe(WIDTH, HEIGHT//2 + pipe_height, 1)
            
            pipe_group.add(bottom_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now
            
        # drawing and scrolling the ground
        ground_x -= scroll_speed
        if abs(ground_x) > 35:
            ground_x = 0
        
        pipe_group.update()
    
    screen.blit(ground, (ground_x, 768))
          
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
    pygame.display.update()

pygame.quit()