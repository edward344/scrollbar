#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

SCREEN_WIDTH = 660
SCREEN_HEIGHT = 480

GRAY = (197,194,197)
BLUE = (0,0,255)
WHITE = (255,255,255)

class ScrollBar(object):
    def __init__(self,image_height):
        self.y_axis = 0
        self.image_height = image_height
        self.change_y = 0
        
        bar_height = int((SCREEN_HEIGHT - 40) / (image_height / (SCREEN_HEIGHT * 1.0)))
        self.bar_rect = pygame.Rect(SCREEN_WIDTH - 20,20,20,bar_height)
        self.bar_up = pygame.Rect(SCREEN_WIDTH - 20,0,20,20)
        self.bar_down = pygame.Rect(SCREEN_WIDTH - 20,SCREEN_HEIGHT - 20,20,20)
        
        self.bar_up_image = pygame.image.load("up.png").convert()
        self.bar_down_image = pygame.image.load("down.png").convert()
        
        self.on_bar = False
        self.mouse_diff = 0
        
    def update(self):
        self.y_axis += self.change_y
        
        if self.y_axis > 0:
            self.y_axis = 0
        elif (self.y_axis + self.image_height) < SCREEN_HEIGHT:
            self.y_axis = SCREEN_HEIGHT - self.image_height
            
        height_diff = self.image_height - SCREEN_HEIGHT
        
        scroll_length = SCREEN_HEIGHT - self.bar_rect.height - 40
        bar_half_lenght = self.bar_rect.height / 2 + 20
        
        if self.on_bar:
            pos = pygame.mouse.get_pos()
            self.bar_rect.y = pos[1] - self.mouse_diff
            if self.bar_rect.top < 20:
                self.bar_rect.top = 20
            elif self.bar_rect.bottom > (SCREEN_HEIGHT - 20):
                self.bar_rect.bottom = SCREEN_HEIGHT - 20
            
            self.y_axis = int(height_diff / (scroll_length * 1.0) * (self.bar_rect.centery - bar_half_lenght) * -1)
        else:
            self.bar_rect.centery =  scroll_length / (height_diff * 1.0) * (self.y_axis * -1) + bar_half_lenght
             
        
    def event_handler(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.bar_rect.collidepoint(pos):
                self.mouse_diff = pos[1] - self.bar_rect.y
                self.on_bar = True
            elif self.bar_up.collidepoint(pos):
                self.change_y = 5
            elif self.bar_down.collidepoint(pos):
                self.change_y = -5
                
        if event.type == pygame.MOUSEBUTTONUP:
            self.change_y = 0
            self.on_bar = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.change_y = 5
            elif event.key == pygame.K_DOWN:
                self.change_y = -5
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.change_y = 0
            elif event.key == pygame.K_DOWN:
                self.change_y = 0
                
    def draw(self,screen):
        pygame.draw.rect(screen,GRAY,self.bar_rect)
        
        screen.blit(self.bar_up_image,(SCREEN_WIDTH - 20,0))
        screen.blit(self.bar_down_image,(SCREEN_WIDTH - 20,SCREEN_HEIGHT - 20))
            
        

def main():
    # Initialize all imported pygame modules
    pygame.init()
    # Set the width and height of the screen [width, height]
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    # Set the current window caption
    pygame.display.set_caption("ScrollBar")
    #Loop until the user clicks the close button.
    done = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    # Load Image:
    image = pygame.image.load("instruments.png").convert()
    # Create scrollbar object 
    scrollbar = ScrollBar(image.get_height())
    # -------- Main Program Loop -----------
    while not done:
        # --- Main event loop
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop
            
            scrollbar.event_handler(event)
            
        # --- Game logic should go here
        scrollbar.update()
        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        screen.fill((255,255,255))

        # --- Drawing code should go here
        screen.blit(image,(0,scrollbar.y_axis))
        scrollbar.draw(screen)
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 30 frames per second
        clock.tick(30)

    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()

if __name__ == '__main__':
    main()