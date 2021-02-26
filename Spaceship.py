
import os
import pygame, sys
import time
import random

pygame.mixer.pre_init(44100, -16, 1, 512)

pygame.init()

win = pygame.display.set_mode((600, 650))

pygame.display.set_caption("Космический корабль")

igrok = pygame.image.load('images/Player_Ship.png')
vrag = pygame.image.load('images/enemy1.png')
bg = pygame.image.load('images/bg.png')
start_menu = pygame.image.load('images/menu.jpg')
victory_im = pygame.image.load('images/victory.png')
defeat_im = pygame.image.load('images/defeat.png')

font = pygame.font.SysFont('Comicsans', 25, True)
menu_font = pygame.font.SysFont('Comicsans', 45, True)

player_loop = 0
enemy_loop = 0

player_shoot_sound = pygame.mixer.Sound('Sounds/player_shot.ogg')
enemy_shoot_sound = pygame.mixer.Sound('Sounds/enemy_shot.ogg')
explosion_sound = pygame.mixer.Sound('Sounds/explosion.ogg')

pygame.mixer.music.load('Sounds/awesomeness.ogg')

class Main_menu:   

    highlighted = False

    def __init__(self, text, pos): # Конструктор класса главного меню
        self.text = text
        self.pos = pos
        self.set_rect()
        self.draw()
        
        
    def draw(self): # Метод класса Main_menu, выполняющий рисование
        self.set_rend()
        win.blit(self.rend, self.rect)

    def set_rend(self): # метод класса Main_menu, определящий метод,с шрифтом и цветом
        self.rend = menu_font.render(self.text, True, self.get_color())

    def get_color(self): # метод класса Main_menu, устанавливающий цвет пункта меню в зависимости от выделения
        if self.highlighted:
            return (255, 255, 0)
        else:
            return (255, 255, 255)
        
    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos

        

class player(object):
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.hitbox = (self.x, self.y, 95, 88)
        self.lives = 5
        self.loop = 0
        self.visible = True

    def draw(self, win):
        win.blit(igrok, (self.x, self.y))
        self.hitbox = (self.x, self.y, 95, 88)

class snaryad():
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class enemy (object):
    def __init__(self, x, y, speed, end):
        self.x = x
        self.y = y
        self.speed = speed
        self.end = end
        self.path = [self.x, self.end]
        self.hitbox = (self.x, self.y, 95, 88)
        self.health = 10
        self.visible = True
        self.loop = 0

    def draw(self, win):
        if self.visible:
            win.blit(vrag, (self.x, self.y))
            self.hitbox = (self.x, self.y, 95, 88)

            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 90, 10))
            pygame.draw.rect(win, (0,255,0), (self.hitbox[0], self.hitbox[1] - 20, 9*self.health, 10))
        
    def move(self, win):
        if self.speed > 0:
            if self.x < self.path[1]:
                self.x += self.speed
            else:
                self.speed = self.speed * -1
        else:
            if self.x > self.path[0]:
                self.x += self.speed
            else:
                self.speed = self.speed * -1
    
    def hit(self):
        if self.health > 0:
            self.health -= 1
        elif self.health == 0:
            explosion_sound.play()
            run = False
            win.blit(victory_im, (140, 250))
            pygame.display.update()
            time.sleep(2)
            menu()
            
                        
                   
            
run = True        
enemy = enemy(6, 76, 1, 502)
player = player(300, 550, 6)
player_bullets = []
enemy_bullets = []

def drawWindow():
    player.x = 300
    player.y = 550
    player.lives = 5
    enemy.visible = True
    enemy.x = 6
    enemy.y = 76
    enemy.health = 10
    pygame.display.update()
   
    
    while True:
        win.blit(bg, (0,0))
        text = font.render('Жизни: ' + str(player.lives), 1, (255,255,255))
        win.blit(text, (500, 10))
        player.draw(win)
        enemy.draw(win)
        enemy.move(win)
    
        for bullet in player_bullets:
            bullet.draw(win)

        for bullet in enemy_bullets:
            bullet.draw(win)
      
                     
        enemy.loop = enemy.loop+1
    
        if enemy.loop >=100 and enemy.visible:
            enemy_shoot_sound.play()
            facing = -1
            enemy_bullets.append(snaryad(round(enemy.x + 99//2), round(enemy.y + 75//2), 5, (0, 0 ,255), facing))
            enemy.loop = 0
            
        player.loop = player.loop+1 #задержка снарядов
        
        for event in pygame.event.get(): #цикл перебора всех событий
            if event.type == pygame.QUIT:
                run = False

        for bullet in player_bullets:
            if bullet.y - bullet.radius < enemy.hitbox[1] + enemy.hitbox[3] and bullet.y + bullet.radius > enemy.hitbox[1]:
                if bullet.x + bullet.radius > enemy.hitbox[0] and bullet.x - bullet.radius < enemy.hitbox[0] + enemy.hitbox[2]:
                    enemy.hit()
                if enemy.health>0:
                    player_bullets.pop(player_bullets.index(bullet))
               
            if bullet.y < 600 and bullet.y > 0:
                bullet.y += bullet.vel
            
            else:
                player_bullets.pop(player_bullets.index(bullet))

        for bullet in enemy_bullets:
            if bullet.y - bullet.radius < player.hitbox[1] + player.hitbox[3] and bullet.y + bullet.radius > player.hitbox[1]:
                if bullet.x + bullet.radius > player.hitbox[0] and bullet.x - bullet.radius < player.hitbox[0] + player.hitbox[2]:
                    enemy_bullets.pop(enemy_bullets.index(bullet))
                    player.lives -= 1
                if player.lives == 0:
                    explosion_sound.play()
                    player.visible = False
                    run = False
                    win.blit(defeat_im, (140, 250))
                    pygame.display.update()
                    time.sleep(2)
                    menu()
               
            if bullet.y > 0 and bullet.y < 600:
                bullet.y -= bullet.vel
            
            else:
                enemy_bullets.pop(enemy_bullets.index(bullet))
        pygame.display.update()
   
              
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            if player.loop >=100:
                player_shoot_sound.play()
                facing = -1
                player_bullets.append(snaryad(round(player.x + 99//2), round(player.y + 75//2), 5, (255, 0 ,0), facing))
                player.loop = 0
                
            
        if keys[pygame.K_LEFT] and player.x > 5:
            player.x -= player.speed
    
        elif keys[pygame.K_RIGHT] and player.x < 600 - 99 - 5:
            player.x += player.speed

       
           
        
def starting():
    drawWindow()
    
    
menu_points = [Main_menu("Новая игра", (210, 423)), Main_menu("Выход", (210, 463))]

                     
def menu():
    pygame.mixer.music.play()
    start = True
    while start:
            
        win.blit(start_menu, (0, 0))
             
        for point in menu_points:
            if point.rect.collidepoint(pygame.mouse.get_pos()):
                 point.highlighted = True
            else:
                point.highlighted = False
            point.draw()

        pygame.display.update()
        
        
        for event in pygame.event.get(): #цикл перебора всех событий
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_points[0].rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.mixer.music.pause()
                    starting()
                if menu_points[1].rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()
            
menu()


    

