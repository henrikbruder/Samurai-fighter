import pygame   
import random
import math
import time
from pygame import mixer
from threading import Thread
from pygame.constants import K_LEFT
import Spritesheet
import numpy as np
from threading import Thread
from pygame import mixer



class Game:
    def __init__(self):

        # General settings
        pygame.init()
        self.scren_width = 1280
        self.scren_height = 720
        self.screen = pygame.display.set_mode((self.scren_width, self.scren_height))
        pygame.display.set_caption("Samurai fighter")
        self.running = True
        self.clock = pygame.time.Clock()
        self.BG = (50, 50, 50)
        self.BLACK = (0, 0 , 0)

        # Classes
        #self.Attack = Attack.Attack(self)
        
        # Background images
        self.background_img = pygame.image.load("Zombie shooter\Game_Background_1.png")
        self.platform_img = pygame.image.load("Zombie shooter\Platform_1_gelb.PNG").convert_alpha()
        self.platform_img = pygame.transform.scale(self.platform_img, (130, 90))
        # Hero images
        self.sprite_sheet_image_run = pygame.image.load("Zombie shooter\Run_2.png").convert_alpha()
        self.sprite_sheet_image_stand = pygame.image.load("Zombie shooter\Stand_2.png").convert_alpha()
        self.sprite_sheet_image_attack_1 = pygame.image.load("Zombie shooter\Attack1.2.png").convert_alpha()
        self.sprite_sheet_image_jump = pygame.image.load("Zombie shooter\Jump.png").convert_alpha()
        self.sprite_sheet_image_fall = pygame.image.load("Zombie shooter\Fall.png").convert_alpha()
        # Enemy images
        self.enemy_image_stand = pygame.image.load("Zombie shooter\Enemy_stand.png").convert_alpha()
        self.enemy_image_run = pygame.image.load("Zombie shooter\Enemy_Run.png").convert_alpha()
        self.enemy_image_attack_1 = pygame.image.load("Zombie shooter\Enemy_Attack1.png").convert_alpha()
        self.enemy_image_death = pygame.image.load("Zombie shooter\Enemy_Death.png").convert_alpha()
        self.enemy_image_take_hit = pygame.image.load("Zombie shooter\Take hit_enemy.png").convert_alpha()
        # Transforming into Hero Sprite
        self.sprite_sheet_run = Spritesheet.Spritesheet(self.sprite_sheet_image_run)
        self.sprite_sheet_stand = Spritesheet.Spritesheet(self.sprite_sheet_image_stand)
        self.sprite_sheet_attack_1 = Spritesheet.Spritesheet(self.sprite_sheet_image_attack_1)
        self.sprite_sheet_jump = Spritesheet.Spritesheet(self.sprite_sheet_image_jump)
        self.sprite_sheet_fall = Spritesheet.Spritesheet(self.sprite_sheet_image_fall)
        # Transforming into enemy Sprites
        self.enemy_sprite_stand = Spritesheet.Spritesheet(self.enemy_image_stand)
        self.enemy_sprite_run = Spritesheet.Spritesheet(self.enemy_image_run)
        self.enemy_sprite_attack_1 = Spritesheet.Spritesheet(self.enemy_image_attack_1)
        self.enemy_sprite_death = Spritesheet.Spritesheet(self.enemy_image_death)
        self.enemy_sprite_take_hit = Spritesheet.Spritesheet(self.enemy_image_take_hit)

        # Create animation list's (Hero)
        self.animation_list_run = []
        self.animation_list_stand = []
        self.animation_list_attack_1 = []
        self.animation_list_jump = []
        self.animation_list_fall = []
        # Create animation list's (Enemy)
        self.animation_list_enemy_run = []
        self.animation_list_enemy_stand = []
        self.animation_list_enemy_attack_1 = []
        self.animation_list_enemy_death = []
        self.animation_list_enemy_take_hit = []

        # Amount of Sprites (Hero)
        self.animation_steps_run = 8
        self.animation_steps_stand = 4
        self.animation_steps_attack_1 = 4                     
        self.animation_steps_jump = 2
        self.animation_steps_fall = 2
        # Amount of Sprites (Enemy)
        self.animation_steps_enemy_run = 8
        self.animation_steps_enemy_stand = 8
        self.animation_steps_enemy_attack_1 = 6                     
        self.animation_steps_enemy_death = 6
        self.animation_steps_enemy_take_hit = 4

        # Amount of Frames (Hero)
        self.frame_run = 0 
        self.frame_stand = 0 
        self.frame_attack_1 = 0 
        self.frame_jump = 0 
        self.frame_fall = 0
        # Amount of Frames (Enemy)
        self.frame_enemy_run = 0 
        self.frame_enemy_stand = 0 
        self.frame_enemy_attack_1 = 0 
        self.frame_enemy_death = 0 
        self.frame_enemy_take_hit = 0 

        # Time settings for sprite cooldown
        self.last_update =  pygame.time.get_ticks()
        self.last_update_2 =  pygame.time.get_ticks()
        self.animation_cooldown = 100
        self.die_animation_cooldown = 10
        self.attack_1_cooldown = 3000

        # Text and Soundeffects/Music
        self.font = pygame.font.SysFont("comicsans", 100)
        self.start_sound = mixer.Sound("Zombie shooter\start sound.mp3")
        self.music_1 = mixer.Sound("Zombie shooter\music_1.mp3")
        self.fight_sound = mixer.Sound("Zombie shooter\Fight short.mp3")
        self.sword_sound = mixer.Sound("Zombie shooter\Sword Hit Soundeffect.mp3")
        self.walk_sound = mixer.Sound("Zombie shooter\Footsteps_Naruto_Soundeffect.wav")
        self.death_sound = mixer.Sound("Zombie shooter\Death Soundeffect.mp3")
        self.gras_landing_sound = mixer.Sound("Zombie shooter\Gras on platform Soundeffect.mp3 ")
        self.landing_sound = mixer.Sound("Zombie shooter\landing Soundeffect short.mp3")
        self.jump_sound = mixer.Sound("Zombie shooter\Jump Soundeffect.mp3")
        

        # Other declarations
        self.x = -180
        self.y = 327
        self.enemy_x = 900
        self.enemy_y = 327
        self.attacks = False
        self.attacks_fliped = False
        self.is_jumping = False
        self.jump_span = 4
        self.jump_dy = self.jump_span
        self.x_platform = 700
        self.y_platform = 400
        self.platform_move_right = False
        self.hitbox_platform = (self.x_platform, self.y_platform, 64, 64)
        self.on_platform = False
        self.not_on_platform = False
        self.start_game = False
        self.falling_left = False
        self.attack_hit = False
        self.enemy_dies = False
        self.death_list_full = False
        self.red_health_bar_enemy_x = 275
        self.red_health_bar_enemy_width = 0
        self.enemy_lives = 13
        self.is_attacking = False
        self.sound_has_played = False
        self.future_hero_pos = 0
        self.flipped_stand = False
        self.delay = 120
        self.delay_bool = False
        self.hero_attack_hitbox_x = 250
        self.counter = 99
        self.stand = False
        


        # Sprite lists Hero
        for x in range(self.animation_steps_run):
            self.animation_list_run.append(self.sprite_sheet_run.get_image(x, 200, 200 , 2.3, self.BLACK))

        for x in range(self.animation_steps_stand):
            self.animation_list_stand.append(self.sprite_sheet_stand.get_image(x, 200, 200 , 2.3, self.BLACK))

        for x in range(self.animation_steps_attack_1):
            self.animation_list_attack_1.append(self.sprite_sheet_attack_1.get_image(x, 200, 200 , 2.3, self.BLACK))

        for x in range(self.animation_steps_jump):
            self.animation_list_jump.append(self.sprite_sheet_jump.get_image(x, 200, 200 , 2.3, self.BLACK))

        for x in range(self.animation_steps_fall):
            self.animation_list_fall.append(self.sprite_sheet_fall.get_image(x, 200, 200 , 2.3, self.BLACK))

        # Sprite lists Enemy 
        for x in range(self.animation_steps_enemy_stand):
            self.animation_list_enemy_stand.append(self.enemy_sprite_stand.get_image(x, 200, 200 , 2.4, self.BLACK))

        for x in range(self.animation_steps_enemy_run):
            self.animation_list_enemy_run.append(self.enemy_sprite_run.get_image(x, 200, 200 , 2.4, self.BLACK))

        for x in range(self.animation_steps_enemy_attack_1):
            self.animation_list_enemy_attack_1.append(self.enemy_sprite_attack_1.get_image(x, 200, 200 , 2.4, self.BLACK))

        for x in range(self.animation_steps_enemy_death):
            self.animation_list_enemy_death.append(self.enemy_sprite_death.get_image(x, 200, 200 , 2.4, self.BLACK))

        for x in range(self.animation_steps_enemy_take_hit):
            self.animation_list_enemy_take_hit.append(self.enemy_sprite_take_hit.get_image(x, 200, 200 , 2.4, self.BLACK))

        
        self.start_sound.play(0)
        self.music_1.play(0)
        self.fight_sound.play(0)

        # Game-Loop:
        while self.running:
            self.clock.tick(130)
            self.screen.fill(self.BG)   # update background
            self.screen.blit(self.background_img, (0, 0))
            self.screen.blit(self.platform_img, (self.x_platform, self.y_platform))
            self.pressed = pygame.key.get_pressed()


            # Text
            self.starting_label = self.font.render(f'Press "Enter"',1, (255, 255, 255))
            self.starting_label_2 = self.font.render(f'to run the game',1, (255, 255, 255))
            
            
            # Platformen bewegen
            if self.x_platform == 0:
                self.platform_move_right = True
            
            elif self.x_platform == self.scren_width-130:
                self.platform_move_right = False

            if self.platform_move_right == True:
                self.x_platform += 1

            else:
                self.x_platform -= 1


            #update frame animation
            self.current_time = pygame.time.get_ticks()
            if self.current_time - self.last_update >= self.animation_cooldown:
                # Hero
                self.frame_run += 1
                self.frame_stand += 1
                self.frame_attack_1 += 1
                self.frame_jump += 1
                self.frame_fall += 1
                
                
                # Setting back the frames if the lists are full (Hero)
                self.last_update = self.current_time
                if self.frame_run >= len(self.animation_list_run):
                    self.frame_run = 0
                
                if self.frame_stand >= len(self.animation_list_stand):
                    self.frame_stand = 0

                if self.frame_attack_1 >= len(self.animation_list_attack_1):
                    self.frame_attack_1 = 0

                if self.frame_jump >= len(self.animation_list_jump):
                    self.frame_jump = 0
                
                if self.frame_fall >= len(self.animation_list_fall):
                    self.frame_fall = 0

                # Enemy
            if self.current_time - self.last_update >= self.animation_cooldown-8:
                self.frame_enemy_run += 1
                self.frame_enemy_stand += 1
                self.frame_enemy_attack_1 += 1
                self.frame_enemy_death += 1
                self.frame_enemy_take_hit += 1
                
                # Setting back the frames if the lists are full (Enemy)
                if self.frame_enemy_run >= len(self.animation_list_enemy_run):
                    self.frame_enemy_run = 0
                
                if self.frame_enemy_stand >= len(self.animation_list_enemy_stand):
                    self.frame_enemy_stand = 0

                if self.frame_enemy_attack_1 >= len(self.animation_list_enemy_attack_1):
                    self.frame_enemy_attack_1 = 0

                if self.frame_enemy_death >= len(self.animation_list_enemy_death):
                    self.frame_enemy_death = 0
                
                if self.frame_enemy_take_hit >= len(self.animation_list_enemy_take_hit):
                    self.frame_enemy_take_hit = 0


           





            

            #self.screen.blit(self.starting_label, (338, 180))
            #self.screen.blit(self.starting_label_2, (275, 300))

            # Looks for Quitting the game
            for event in pygame.event.get():   
                if event.type == pygame.QUIT:   
                    self.running = False  
            
            
    # HITBOXES:a
            # HERO:
            self.hero_hitbox = pygame.Rect(self.x+205, self.y+180, 70, 120)
            #pygame.draw.rect(self.screen,(255,0,0),self.hero_hitbox,3)
            if self.flipped_stand:
                self.hero_attack_hitbox = pygame.Rect(self.x+60, self.y+155, 140, 140)
            else:
                self.hero_attack_hitbox = pygame.Rect(self.x+250, self.y+155, 140, 140)
            pygame.draw.rect(self.screen,(0,255,0),self.hero_attack_hitbox,3)


            # ENEMY:
            self.enemy_hitbox = pygame.Rect(self.enemy_x+205, self.enemy_y+180, 70, 120)
            #pygame.draw.rect(self.screen,(0,0,0),self.enemy_hitbox,3)


    # HEALTH BARS:
            self.enemy_health_bar_green = pygame.Rect(self.enemy_x+205, self.enemy_y+160, 70, 8)
            pygame.draw.rect(self.screen,(0,255,0),self.enemy_health_bar_green,100)
            self.enemy_health_bar_red = pygame.Rect(self.enemy_x+self.red_health_bar_enemy_x, self.enemy_y+160, self.red_health_bar_enemy_width, 8)
            pygame.draw.rect(self.screen,(255,0,0),self.enemy_health_bar_red,100)


    # ENEMY CONTROLS:
   
             # Collision
            if self.hero_attack_hitbox.colliderect(self.enemy_hitbox) and self.attacks or self.hero_attack_hitbox.colliderect(self.enemy_hitbox) and self.attacks_fliped == True:
                self.attack_hit = True

            elif self.attack_hit == True:
                #if self.current_time_2 - self.last_update_2 >= self.die_animation_cooldown:
                    self.flip_image_take_hit = pygame.transform.flip(self.animation_list_enemy_take_hit[self.frame_enemy_take_hit], True, False)
                    self.flip_image_take_hit.set_colorkey(self.BLACK)
                    self.screen.blit(self.flip_image_take_hit, (self.enemy_x, self.enemy_y))
                    if self.frame_enemy_take_hit == 3:
                        if self.enemy_lives > 0:
                            self.enemy_lives -= 1
                            self.red_health_bar_enemy_x -= 5
                            self.red_health_bar_enemy_width += 5
                            self.sword_sound.play(0)
                            self.attack_hit = False
                            print("self.enemy_lives: ")
                            print(self.enemy_lives)
                       
                        else:
                            self.red_health_bar_enemy_x -= 5
                            self.red_health_bar_enemy_width += 5
                            self.enemy_dies = True
                            self.attack_hit = False
   

            elif self.enemy_dies:
                self.screen.blit(self.animation_list_enemy_death[self.frame_enemy_death], (self.enemy_x, self.enemy_y))
                if self.frame_enemy_death == 5:
                    self.screen.blit(self.animation_list_enemy_death[5], (self.enemy_x, self.enemy_y)) 
                    self.last_update_2 = self.current_time_2
                    self.attack_hit = False
                    print("du hs")
                    if self.sound_has_played == False:
                        self.death_sound.play(0)
                        self.sound_has_played = True

                    self.clock.tick(30)
                        

            elif self.enemy_x > self.x + 150 and self.enemy_dies == False and self.attack_hit == False:
                self.enemy_x -= 1
                self.flip_enemy_image = pygame.transform.flip(self.animation_list_enemy_run[self.frame_enemy_run], True, False)
                self.flip_enemy_image.set_colorkey(self.BLACK)
                self.screen.blit(self.flip_enemy_image, (self.enemy_x, self.enemy_y))

            elif self.enemy_x < self.x - 150 and self.enemy_dies == False and self.attack_hit == False:
                self.enemy_x += 1
                self.screen.blit(self.animation_list_enemy_run[self.frame_enemy_run], (self.enemy_x, self.enemy_y))

            else:
                self.current_time_2 = pygame.time.get_ticks()
                
                if self.current_time_2 - self.last_update_2 >= self.attack_1_cooldown and self.enemy_dies == False and self.attack_hit == False:
                    self.last_update_2 = self.current_time_2
                    if self.enemy_x < self.x:
                        self.screen.blit(self.animation_list_enemy_attack_1[self.frame_enemy_attack_1], (self.enemy_x, self.enemy_y))
                        self.attack_1_cooldown += 3000
                        
                    else:
                        if self.enemy_dies == False and self.attack_hit == False:
                            self.flip_enemy_image_attack_1 = pygame.transform.flip(self.animation_list_enemy_attack_1[self.frame_enemy_attack_1], True, False)
                            self.flip_enemy_image_attack_1.set_colorkey(self.BLACK)
                            self.screen.blit(self.flip_enemy_image_attack_1, (self.enemy_x, self.enemy_y))
                
                else:
                    if self.enemy_dies == False and self.attack_hit == False:
                        self.flip_enemy_image_stand = pygame.transform.flip(self.animation_list_enemy_stand[self.frame_enemy_stand], True, False)
                        self.flip_enemy_image_stand.set_colorkey(self.BLACK)
                        self.screen.blit(self.flip_enemy_image_stand, (self.enemy_x, self.enemy_y))
                    
                                       

    # HERO CONTROLLS:

            # Attack
            if self.attacks:
                self.screen.blit(self.animation_list_attack_1[self.frame_attack_1], (self.x, self.y))
                if self.frame_attack_1 == 3:
                    self.attacks = False

            # Jump
            elif self.is_jumping:
                if self.y < self.y_platform-280 and self.y > self.y_platform-285 and self.x+200 > self.x_platform-40 and self.x+200 < self.x_platform+85:
                    self.y = 116
                    self.on_platform = True
                    self.is_jumping = False
                    self.gras_landing_sound.play(0)

                elif self.jump_dy >= -self.jump_span:
                    self.jump_img = self.animation_list_jump[self.frame_jump]
                    self.fall_img = self.animation_list_fall[self.frame_fall]

                    if self.pressed[pygame.K_d]: 
                        if event.type == pygame.MOUSEBUTTONDOWN: 
                            self.attack() 
                        elif self.x > self.scren_width-200:  
                            self.x = -200
                        self.x += 4
                    elif self.pressed[pygame.K_a]:
                        if event.type == pygame.MOUSEBUTTONDOWN: 
                            self.fliped_attack() 
                        elif self.x < -250:
                            self.x = self.scren_width-200
                        self.x -= 4
                        self.jump_img = pygame.transform.flip(self.jump_img, True, False)
                        self.jump_img.set_colorkey(self.BLACK)

                    if self.jump_dy > 0:
                        self.screen.blit(self.jump_img, (self.x, self.y))
                        self.y -= self.jump_dy ** 2
                        
                    else: 
                        self.y += self.jump_dy ** 2+0.4
                        self.screen.blit(self.fall_img, (self.x, self.y))
                        

                    self.jump_dy -= 0.1
                    if event.type == pygame.MOUSEBUTTONDOWN: 
                        self.attack()
                    
                
                else:
                    self.landing_sound.play(0)
                    self.is_jumping = False
                    self.jump_dy = self.jump_span
                    self.screen.blit(self.animation_list_stand[self.frame_stand], (self.x, self.y))

            # On the platform           
            elif self.on_platform == True:
                self.x = self.x_platform - 165
                self.screen.blit(self.animation_list_stand[self.frame_stand], (self.x, self.y))

                if self.pressed[pygame.K_SPACE] or event.type == pygame.MOUSEBUTTONDOWN: 
                    self.not_on_platform = True
                    self.on_platform = False


            # Not on the platformd    
            elif self.not_on_platform == True:
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    self.attacks = True
                elif self.attacks:
                    self.screen.blit(self.animation_list_attack_1[self.frame_attack_1], (self.x, self.y))
                    if self.frame_attack_1 == 3:
                        self.attacks = False
                
                elif self.y < 327:    
                    self.jump_img = self.animation_list_jump[self.frame_jump]
                    self.fall_img = self.animation_list_fall[self.frame_fall]
                    if self.jump_dy >= -self.jump_span:

                        if self.pressed[pygame.K_d]:
                            if event.type == pygame.MOUSEBUTTONDOWN: 
                                self.attack() 
                            if self.x > self.scren_width-200:  
                                self.x = -200
                            self.x += 4
                        elif self.pressed[pygame.K_a]: 
                            if self.x < -250:
                                self.x = self.scren_width-200
                            self.x -= 4
                            self.jump_img = pygame.transform.flip(self.jump_img, True, False)
                            self.jump_img.set_colorkey(self.BLACK)
        
                        if self.jump_dy > 0:
                            self.screen.blit(self.jump_img, (self.x, self.y))
                            self.y -= self.jump_dy ** 1
                        else: 
                            self.y += self.jump_dy ** 2
                            self.screen.blit(self.fall_img, (self.x, self.y))

                        self.jump_dy -= 0.1
                        

                    else:
                        self.y = 327
                        self.jump_dy = self.jump_span
                        self.not_on_platform = False
                        self.landing_sound.play(0)

            # Jump
            elif self.pressed[pygame.K_SPACE]:
                self.is_jumping = True
                self.screen.blit(self.animation_list_stand[self.frame_stand], (self.x, self.y))
                self.jump_sound.play(0)
                self.stand = True 
                self.walk_sound.stop()
                self.counter = 99
        
            # Attack
            elif self.attacks:
                self.attack() 
            
            # Walk right
            elif self.pressed[pygame.K_d]:
                self.flipped_stand = False
                if event.type == pygame.MOUSEBUTTONDOWN: 
                   self.attack()
                   
                elif self.x > self.scren_width-200:  
                    self.x = -200
                    self.screen.blit(self.animation_list_run[self.frame_run], (self.x, self.y))
                    
                else:
                    self.stand = False 
                    self.x += 6
                    self.screen.blit(self.animation_list_run[self.frame_run], (self.x, self.y))
                    self.counter +=1
                    if self.counter % 100 == 0 and self.stand == False:
                        self.walk_sound.stop()
                        self.walk_sound.play(0)
                        
                        

              
                   
            # Walk left
            elif self.pressed[pygame.K_a]:
                self.flipped_stand = True
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    self.fliped_attack()
                elif self.x < -250:
                    self.x = self.scren_width-200
                    self.flip_image = pygame.transform.flip(self.animation_list_run[self.frame_run], True, False)
                    self.flip_image.set_colorkey(self.BLACK)
                    self.screen.blit(self.flip_image, (self.x, self.y))
                else:
                    self.stand = False 
                    self.x -= 6
                    self.flip_image = pygame.transform.flip(self.animation_list_run[self.frame_run], True, False)
                    self.flip_image.set_colorkey(self.BLACK)
                    self.screen.blit(self.flip_image, (self.x, self.y))
                    self.counter +=1
                    if self.counter % 100 == 0 and self.stand == False:
                        self.walk_sound.stop()
                        self.walk_sound.play(0)

            # Attack 1
            elif event.type == pygame.MOUSEBUTTONDOWN or self.is_attacking == True: 
                if self.flipped_stand == True:
                    self.fliped_attack()
                else:
                    self.attack()

            # Stand still
            else:
                self.stand = True 
                self.walk_sound.stop()
                self.counter = 99
                if self.flipped_stand == True:
                    self.flip_image_stand = pygame.transform.flip(self.animation_list_stand[self.frame_stand], True, False)
                    self.flip_image_stand.set_colorkey(self.BLACK)
                    self.screen.blit(self.flip_image_stand, (self.x, self.y))

                else:
                    self.screen.blit(self.animation_list_stand[self.frame_stand], (self.x, self.y))
                    


            # Update Display
            pygame.display.update()
                

    def attack(self):
        self.current_time_2 = pygame.time.get_ticks()
        self.attacks = True
        #print("self.frame_attack_1:")
        #print(self.frame_attack_1)
        self.is_attacking = True
        if self.attacks:
            #print(self.frame_attack_1)
            self.screen.blit(self.animation_list_attack_1[self.frame_attack_1], (self.x, self.y))
            if self.frame_attack_1 == 3:
                self.attacks = False
                self.is_attacking = False
                #print("huefhwufhwi")
                
                

    def fliped_attack(self):
        flip_image_attack = pygame.transform.flip(self.animation_list_attack_1[self.frame_attack_1], True, False)
        flip_image_attack.set_colorkey(self.BLACK)
        self.current_time_2 = pygame.time.get_ticks()
        print("self.attacks_fliped")
        print(self.attacks_fliped)
        self.attacks_fliped = True
        self.is_attacking = True
        if self.attacks_fliped:
            self.screen.blit(flip_image_attack, (self.x, self.y))
            if self.frame_attack_1 == 3:
                self.attacks_fliped = False
                self.is_attacking = False
                


def scale_image(img, scale):
    width = int(img.get_rect().width/scale)
    height = int(img.get_rect().height/scale)
    new_img = pygame.transform.scale(img, (width, height))
    return new_img
        
                

# Startet Spiel
if __name__ == "__main__":
    game = Game()


    #thread_1 = Thread(target = Game)
    #thread_2 = Thread(target = Spaceship)
    #thread_1.start()
    #thread_2.start()