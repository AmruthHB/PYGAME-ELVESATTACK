# Amruth Baskar
# 19/1/2018
# ICS3U-Pygame- CPT
# Creates a shooter game in which the player has to try to score as many points as possible by surviving waves of enslaved elves

import pygame
import random

# colours
RED = ( 255, 0, 0)
WHITE = ( 255, 255, 255)
BLACK = ( 0, 0, 0)
BLUE = ( 0, 0, 255)
GREEN = ( 0, 255, 0)
YELLOW = ( 247, 202, 24)
CANDY_RED = ( 215, 0, 12)
STAR_YELLOW = ( 244, 208, 63)
GLACIAL_WHITE = ( 227, 227, 227)

# creates variables to set dimenisons of the screen
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600


# creates a class for the background and associated background effects such as snow and stars
class Background:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.snow_list = []
        self.snow_y = 0
        self.move_y = 3

    # creates background 
    def draw_background(self):
        pygame.draw.rect(screen,BLACK,[0,0,1000,600])
        for i in range (20):
            pygame.draw.ellipse(screen,GLACIAL_WHITE,[(i*60),555,80,20])
        pygame.draw.rect(screen,GLACIAL_WHITE,[0,570,1000,50])

    # generates stars through use of lists and repetition. Repetiotion and lists are used to create many sets of random values and store them.
    def create_stars(self,amount):
      x_values = []
      y_values = []
      for i in range (amount):
        x = random.randint(10,1000)
        y = random.randint(40,450)
        x_values.append(x)
        y_values.append(y)
        # because unit testing could not be done using the unittest module, testing was done manually
        #print(len (x_values))
      return x_values,y_values,amount

    # draws the randomly generated star coordinates through repetition by iterating through each stored coordinate in the list and drawing each element.
    def draw_stars(self,x_values,y_values,amount):
      for i in range(amount):
        x_coord = x_values[i]
        y_coord = y_values[i]
        pygame.draw.ellipse(screen,STAR_YELLOW,[x_coord,y_coord,10,10])

    # through use of repetition and lists random snow coordinates are generated and stored. In two parts, repetition creates these coordinates, and the list stores them.
    def create_snow(self,amount):
        xy_snow_values = []
        for i in range (amount):
            coordinate_temp_storage = [random.randint(30,1000),random.randint(0,450)]
            xy_snow_values.append(coordinate_temp_storage)
        return amount,xy_snow_values

    # using the stored coordinates of snow, repetition is used to iterate through each element of the list and draws it
    def draw_and_animate_snow(self,amount,xy_snow_values):
        for i in range (amount):
            pygame.draw.ellipse(screen,WHITE,[xy_snow_values[i][0],xy_snow_values[i][1],5,5])

            # makes snow fall after drawing
            xy_snow_values[i][1] += 0.65

            #if snow reaches certain coordinate resets position so that it falls from the top to bottom again, also made sure that the snow does not cover the player stats and score
            if xy_snow_values[i][1] > 550:
                xy_snow_values[i][0] = random.randint(30,1000)
                xy_snow_values[i][1] = random.randint(0,450)
    
            
            
            
# creates player as santa
# Jump and gravity code referenced from: http://programarcadegames.com/index.php?chapter=introduction_to_sprites&lang=en
class Santa(pygame.sprite.Sprite):
    def __init__(self):

        # initializes attributes of player
        super().__init__()
        self.image = pygame.image.load("Santa.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.move_x = 0
        self.move_y = 3
        self.hitpoints = 100
        self.dead = False
        
   
    #   inherited from sprites, updates through every iteration of the loop to calculate gravity and update player position. Also takes platfroms as a paramter to detect player collisons.
    def update(self,platform_list):
        
        self.platform_list = platform_list
        self.calc_gravity()
        self.rect.x += self.move_x
       
        # if player is gone beyond a certain point on the screen, prevents them from moving any further, sleection used to account for the player going beyond the higest and lowes x values
        if player.rect.x <= 10:
            self.rect.x -= self.move_x
        elif player.rect.x >= 930:
            self.rect.x -= self.move_x

        #creates a list that checks if the player has collided with any of the platforms. Uses repetition to iterate through each created platform
        #and sets player position acordingly
        platform_list = pygame.sprite.spritecollide(self, self.platform_list, False)
        for block in platform_list:

            # uses selection to see if player contacts the block by travelling right or left and sets their position on the block accordingly
            if self.move_x > 0:
                self.rect.right = block.rect.left
            elif self.move_x < 0:
                self.rect.left = block.rect.right
        
        # increses or decreases the height of the player movement vector relative to the ground
        self.rect.y += self.move_y

        # creates a list that checks if the player has collided with any of the platforms. Uses repetition to iterate through each created platform
        # and sets player position acordingly
        platform_list = pygame.sprite.spritecollide(self, self.platform_list, False)
        for block in platform_list:
 
            # uses selection to see if player, came in contact with the top of or bottom of the platfrom and sets a new position accordingly
            if self.move_y > 0:
                self.rect.bottom = block.rect.top
            elif self.move_y < 0:
                self.rect.top = block.rect.bottom
             
            self.move_y = 0

    
    # calculates gravity for jumping
    def calc_gravity(self):
        # adds gravity so that player drops by 0.35 pixels in each frame in the update
        self.move_y += .35
 
        # checks to see if player is on ground, if the are sets they movement vector to 0 to make sure they dont fall out of screen 
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.move_y >= 0:
            self.move_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    # param given as platform list to detect collision with all platforms in the game
    def jump(self,platform_list):
        self.platform_list = platform_list
        # moves down to check if there is a platfrom, if there is a platform, moves back to original position before being moved. Ensures that mid-air jumping cannot be achieved
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.platform_list, False)
        self.rect.y -= 2
 
        # uses selection check if the player has collided with the platform or if they are on the ground, then allow player to jump 
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.move_y = -10
    # moves player to the right by changing x speed vector
    def move_right(self):
        self.move_x = 4

    # moves player left by changing the x speed vector
    def move_left(self):
        self.move_x = -4

    # resets move ment vector to zero if no buttons are being pressed
    def reset_movement(self):
        self.move_x = 0

    # reduces the player's hitpounts based on the damage of the enemy object
    def reduce_hitpoints(self, item_damage):
        self.hitpoints -= item_damage

    # uses sleection to check if player is dead, result is returned as a boolean
    def is_dead(self):
        if self.hitpoints <= 0:
            self.dead = True
        else:
            self.dead = False
        return self.dead

    # destroys the player character by removing the object, used if player dies
    def destroy(self):
        self.kill()
        

# construct bplatform based on x, y, width and height values
class Platform(pygame.sprite.Sprite):
   def __init__(self,x,y,width, height):

        # initialize attributes
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(CANDY_RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# class for enemies
class Elf(pygame.sprite.Sprite):
    def __init__(self):

        # initializes attributes
        super().__init__()
        self.image = pygame.image.load("IncomingElf.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.move_x = -1*random.randint(5,8)
        self.move_y = 0
        self.hitpoints = 60
        self.dead = False
        self.damage = 0.25
        
    def update(self):

        # checks to see if elves are at a certain point, if they are, the movement vector is changed so that they turn and go the otehr way
        if self.rect.x <=  0:
            self.move_x = self.move_x *-1
        elif self.rect.x >= 990:
            self.move_x = self.move_x *-1
        self.rect.x +=  self.move_x
        
    # reduces enemy hitpoints based on the damage of the weapon
    def reduce_hitpoints(self, item_damage):
        self.hitpoints -= item_damage

    # uses selection to check player's hitpoints, if lower than or equal to zero, returns boolean as true, or else returns it as false
    def is_dead(self):
        if self.hitpoints <= 0:
            self.dead = True
        else:
            self.dead = False
        return self.dead

    # return teh value of samage done by the elf
    def get_damage(self):
        return self.damage

    # used to destroy object if enemy is dead
    def destroy(self):
        self.kill()



# wave class is used to spawn waves after a group of elves are killed, increases spawns by 3 new enemies each round
class Wave:
    def __init__(self,rounds,enemy_list,all_sprites):
        
        spawn_val = rounds*2
        
        # iteraties relative to the length of enemies to be spawned, creates the enemies and stores them in two lists; all enemies and sprites
        for i in range (spawn_val):
            enemy = Elf()
            enemy.rect.x = random.randint(650,700)
            enemy.rect.y = 500
            all_enemies.add(enemy)
            all_sprites.add(enemy)

            
# bullet class used to proect bullets from the gun
class Bullet(pygame.sprite.Sprite):
    
    def __init__(self):

        # initializes bullet attributes
        super().__init__()
        self.image = pygame.image.load("Bullet.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.damage = 4
        self.rate_of_fire = 4

    # moves bullet for each frame and destroys the object once it goes past a certain x value  
    def update(self):
       self.rect.x += self.rate_of_fire
       if self.rect.x > 990:
            self.kill()

    # returns the damage done by the bullet
    def get_damage(self):
        return self.damage


# class for player's weapon, a pistol
class Pistol(pygame.sprite.Sprite):
    
    def __init__(self):

        # initializes attributes of the object
        super().__init__()
        self.image = pygame.image.load("pistol.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        
    # update to the postion of the pistol every round to position it right in front of the player
    def update(self):
      
        player_weapon.rect.x = player.rect.x + 60
        player_weapon.rect.y = player.rect.y + 50
       
   # destroys the pistol object
    def destroy(self):
        self.kill()






# initializes pygame and creates screen dimesions, creates title
pygame.init()

size = [SCREEN_WIDTH,SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Elves Attack!")

done = False

# initializes variables
score = 0  
enemy_wave_num = 0

# initializes all the sprite lists to be used to draw and update created sprites
all_sprites = pygame.sprite.Group()
all_bullets = pygame.sprite.Group()
all_enemies = pygame.sprite.Group()
player_actions = pygame.sprite.Group()
platform_list = pygame.sprite.Group()

# background

# used to instantiate the background class
main_background = Background()

# creates star positions 
star_locations = main_background.create_stars(20)

# creates all snow positions
stored_snow = main_background.create_snow(70)

# creates all platforms 
platform = Platform(250, 460 ,100,10)
platform2 = Platform(650,460,100,10)

# adds all platforms to its specific sprite group also adds them to the list of all sprites in teh game
platform_list.add(platform)
platform_list.add(platform2)
all_sprites.add(platform)
all_sprites.add(platform2)

# instantiates santa class through player and [pistol class as player's weapon. Note that player object is not added to all sprite groups because it requires platforms as parameters
player = Santa()
player.rect.x = 200
player.rect.y = 400
player_actions.add(player)

player_weapon = Pistol()
all_sprites.add(player_weapon)

# creates initial enemy spawn of three enemies and adds it to its appropriate sprite groups
for i in range (3):
    enemy = Elf()
    enemy.rect.x = 400
    enemy.rect.x = random.randint(700,900)
    enemy.rect.y = 500
    all_enemies.add(enemy)
    all_sprites.add(enemy)


# creates and renders font for score
score_writing = pygame.font.SysFont('Calibri', 16, False, False)
score_text = score_writing.render("Score: "+str(score),True,WHITE)

# creates and renders font for player's hitpoints
santa_hitpoint_writing = pygame.font.SysFont('Calibri',16,False,False)
hitpoints_text = santa_hitpoint_writing.render("Health: " + str(round(player.hitpoints,-1)), True,WHITE)

# creates and renders font for waves of enemies
player_waves = pygame.font.SysFont('Calibri',16,False,False)
player_waves_text = player_waves.render('Wave: ' + str(enemy_wave_num), True, WHITE)


clock = pygame.time.Clock()


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
         
        elif event.type == pygame.KEYDOWN:

            # allows user to control player while character is not dead
            if player.is_dead() == False:

                # creates bullets and adds it to its appropriate sprite group
                  if event.key == pygame.K_p:
                      bullet = Bullet()
                      bullet.rect.x = player_weapon.rect.x
                      bullet.rect.y = player_weapon.rect.y
                      all_bullets.add(bullet)
                      all_sprites.add(bullet)

            # if d is pressed movement vector of x is increased so they move right
            if event.key == pygame.K_d:
                  player.move_right()
                  
            # if a is pressed movement vector of x is decreased so they move left    
            elif event.key == pygame.K_a:
                  player.move_left()
            # if k is pressed allows player to jump
            elif event.key == pygame.K_k:
                  player.jump(platform_list)

        # resets movement vector of player if no assigned movement key is being pressed
        elif event.type == pygame.KEYUP:
            if event.key == pygame. K_d or event.key == pygame.K_a:
                  player.reset_movement()
          
                   
                

    # game logic

    # updates all sprites and player 
    all_sprites.update()
    player_actions.update(platform_list)

    # uses selection to determine if the length of enemy sprite list is 0, if it is the wave number is incremented by one and new enemies are spawned
    if len(all_enemies) == 0:
        enemy_wave_num += 1
        player_waves_text = player_waves.render('Wave: ' + str(enemy_wave_num), True, WHITE)
        wave = Wave(enemy_wave_num,all_enemies, all_sprites)

    # iterates through each bullet in its associated group
    for bullets in all_bullets:
        
        # detects collison and adds it to the variable player hit list
        enemy_hit_list = pygame.sprite.spritecollide(bullet, all_enemies, False)

        # iterates through ech enemy hit in the list of hits, removes bullets from all sprites, bullets list, reduces enemy's hitpoints
        for enemy in enemy_hit_list:
            all_bullets.remove(bullet)
            all_sprites.remove(bullet)
            bullet_dmg = bullet.get_damage()
            enemy.reduce_hitpoints(bullet_dmg)

           # because unit testing could not be done using the unittest module, testing was done manually
           #print(enemy.hitpoints)
            
            # if enemy is dead destroys the enemy object and removes it from the lists it is in, also adds points to score
            if enemy.is_dead() == True:
                enemy.destroy()
                all_enemies.remove(enemy)
                all_sprites.remove(enemy)
                score += 10
                score_text = score_writing.render("Score: "+ str(score),False,WHITE)

    # iterates through each enemy in its group           
    for enemies in all_enemies:

       # if player's rectangle intersects with that of the enemy, player takes damage
       if( pygame.sprite.collide_rect(player,enemy) == True) or (pygame.sprite.collide_rect(enemy,player) == True):
           enemy_damage = enemy.get_damage()
           player.reduce_hitpoints(enemy_damage)

           # because unit testing could not be done using the unittest module, testing was done manually
           #print(player.hitpoints)
           
           # uses selection to heck if player is dead, if returned boolean is true destroys the player, destroys the player's weapon.
           if player.is_dead() == True:
               player.hitpoints = 0
               player.destroy()
               player_weapon.destroy()

               # removes player and their weapons from their associated sprite group
               all_sprites.remove(player_weapon)
               player_actions.remove(player)

       # displays player's health 
       hitpoints_text = santa_hitpoint_writing.render("Health: " + str(player.hitpoints), True,WHITE)
    
    
    # clear screen

    screen.fill(WHITE)

    # draw here

    # draws the background, snow and stars
    main_background.draw_background()
    main_background.draw_stars(star_locations[0],star_locations[1],star_locations[2])
    main_background.draw_and_animate_snow(stored_snow[0],stored_snow[1])

    # draws all sprites and the player
    all_sprites.draw(screen)
    player_actions.draw(screen)

    # Displays all the text on the screen including player stats, wave and hitpoints
    screen.blit(score_text, [0, 20])
    screen.blit(hitpoints_text,[0,0])
    screen.blit(player_waves_text,[0,40])
    
    pygame.display.flip()




    # clock speed set to 120 for fast game play
    clock.tick(120)

pygame.quit()
    
