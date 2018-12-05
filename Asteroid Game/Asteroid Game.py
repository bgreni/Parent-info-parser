import pygame  
from pygame import *
import random

# Asteroid game version 1.0

def main():
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()
    
class Game:
    # Game object represents an instance of this game
    def __init__(self):
        # create screen and set font
        self.continue_game = True
        (width,height) = (700,500)
        self.screen = pygame.display.set_mode((width,height))
        self.ast_list = []
        self.score = 0
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS',30)
        
    def run(self):
       # loop while game continuation is true
        ship = Ship(self.screen)
        while self.continue_game:
            # start with a 2% chance to spawn an asteroid each tick, spawn chance
            # increases as score increases
            if 1000-self.score > 100:
                ast_spawn = random.randint(0,1000-int(self.score))
            else:
                ast_spawn = random.randint(0,100)
            if ast_spawn <= 20 :
                aster = Asteroid(self.screen)
                self.ast_list.append(aster)
            # check for ship control input
            self.handle_key(ship)
            self.draw_screen(ship,self.ast_list)
            self.continue_game = self.should_continue(ship)
            pygame.display.flip()
            pygame.time.wait(5)                
            
        
    def handle_key(self,ship):
        # check for control input
        key = pygame.key.get_pressed()
        if key[K_w]:
            ship.move_up()
        if key[K_s]:
            ship.move_down()
        if key[K_a]:
            ship.move_left()
        if key[K_d]:
            ship.move_right()        
        
    def should_continue(self,ship):
        # check if quit box has been pressed or player has run out of health
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False 
        if ship.get_health() <= 0:
            return False
        return True
    
    
    def draw_screen(self,ship,ast_list):
        # overwrite old screen contents
        self.screen.fill((0,0,0))
        # loop through all live asteroids and draw and move them one tick
        for rock in ast_list:
            rock.draw()
            rock.move()
            # check if rock has gone off screen
            if rock.is_dead():
                self.ast_list.remove(rock)
                self.score += 1
            # check if rock has hit the player
            if rock.get_hit_box().colliderect(ship.get_hit_box()):
                ship.is_hit(rock.get_damage())
                self.ast_list.remove(rock)
        # draw the ship and write game text
        ship.draw()
        self.write_text(ship)
    
    def write_text(self,ship):
        # write score and health totals to the screen
        text = self.font.render("SCORE: "+str(self.score),False,pygame.Color('WHITE'))
        self.screen.blit(text,(0,0))
        text = self.font.render("HEALTH: "+str(ship.get_health()),False,pygame.Color('WHITE'))
        self.screen.blit(text,(self.screen.get_width()-text.get_width(),0))
    

class Ship:
    # Ship object represents the players controllable ship
    def __init__(self,screen):
        # initialize needed instance attributes
        self.screen = screen
        self.dims = screen.get_size()
        # ship starts near the bottom of the screen
        self.ship_x = self.dims[0]/2
        self.ship_y = self.dims[1]-100
        self.ship_width = 30
        self.ship_height = 30
        self.ship = Rect(self.ship_x,self.ship_y,self.ship_width,self.ship_height)
        self.health = 100
        self.move_speed = 2
        # apply spaceship picture
        self.image = pygame.image.load('ship.jpg').convert()
        self.image = pygame.transform.scale(self.image,(self.ship_width,self.ship_height))
    
    # draw ship to the screen
    def draw(self):
        self.screen.blit(self.image,self.ship)
    # movement functions, ship is bound to the edges of the screen
    def move_up(self):
        if self.ship.top != 0:
            self.ship.move_ip(0,-self.move_speed)
    def move_down(self):
        if self.ship.bottom != self.dims[1]:
            self.ship.move_ip(0,self.move_speed)
    def move_left(self):
        if self.ship.left != 0:
            self.ship.move_ip(-self.move_speed,0)
    def move_right(self):
        if self.ship.right != self.dims[0]:
            self.ship.move_ip(self.move_speed,0)
    
    def get_health(self):
        return self.health
    
    # damage is determined by the type of asteroid has hit the ship
    def is_hit(self,damage):
        self.health -= damage
        
    def get_hit_box(self):
        return self.ship
    
    
class Asteroid:
    # Asteroid object represents the asteroids the player is avoiding
    def __init__(self,screen):
        # initialize instance attributes
        screen_width = screen.get_width()
        self.screen = screen
        # horizontal starting position is random
        self.x = random.randint(0,screen_width)
        self.y = 0
        # value decides the size and damage values of the asteroid
        size_decider = random.randint(0,100)
        if size_decider <= 40:
            dimensions = 10
            self.damage = 5
        elif size_decider <= 70:
            dimensions = 20
            self.damage = 10
        elif size_decider <= 90:
            dimensions = 30
            self.damage = 15
        elif size_decider <= 99:
            dimensions = 40
            self.damage = 25
        else:
            dimensions = 70
            self.damage = 35
            
        self.width = dimensions
        self.height = dimensions
        # horizontal velocity is a random float -2<=x<=2
        self.x_vel = random.uniform(-2,2)
        self.rock = Rect(self.x,self.y,self.width,self.height)
        # apply asteroid image
        self.image = pygame.image.load('asteroid.png').convert()
        self.image = pygame.transform.scale(self.image,(self.width+10,self.height+10))
        
    # draw asteroid to screen
    def draw(self):
        self.screen.blit(self.image,self.rock)
    
    def move(self):
        self.rock.move_ip(self.x_vel,2)
    
    # check if asteroid has gone off the screen
    def is_dead(self):
        return self.rock.top == self.screen.get_height() or self.rock.left == self.screen.get_width() or self.rock.right == 0
    
    def get_hit_box(self):
        return self.rock
    
    def get_damage(self):
        return self.damage
        
        
    
main()