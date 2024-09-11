#создай игру "Лабиринт"!
from pygame import *

from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, speed, wildth, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (wildth, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    bullet_delay = 20
    lives = 3
    def update(self):
        live_count = size.render(str(self.lives), True, (255, 255, 255))
        window.blit(live_count, (1300, 0))
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT]:
            if self.rect.x > 0:
                self.rect.x -= self.speed
        if keys_pressed[K_RIGHT]:
            if self.rect.x < 1235:
                self.rect.x += self.speed
        if keys_pressed[K_SPACE]:
            if self.bullet_delay < 0:
                self.fire()
                self.bullet_delay = 20
        self.bullet_delay -= 1
        



    def fire(self):
        bullets.add(Bullet('bullet.png', self.rect.centerx-10, self.rect.top-40, 15, 20, 40))

    def live_count(self):
        self.lives -= 1
    





class Enemy(GameSprite):
    def update(self):
        if self.rect.y < 1400:
            self.rect.y += self.speed
        global lost
        if self.rect.y > 1000:
            self.rect.y = -100
            self.rect.x = randint(0, 1250)
            lost += 1
    
    def start_pos(self):
        global kills
        self.rect.y = -100
        self.rect.x = randint(0, 1250)
        kills += 1
            
class Bullet(GameSprite):
    def update(self):
        if self.rect.y < -40:
            self.kill()
        self.rect.y -= self.speed
     
class Asteroid(GameSprite):
    def update(self):
        if self.rect.y > 1000:
            self.rect.y = -100
            self.rect.x = randint(0, 1250)
        self.rect.y += self.speed    
    def start(self):
        self.speed = randint(3, 9)
        self.rect.y = -100
        self.rect.x = randint(0, 1250)    
    
    
hero_height = 150
enemy_height = 100
bullet_height = 40   
asteroid_height = 80 
hero_wildth = 150
enemy_wildth = 150
bullet_wildth = 20  
asteroid_wildth = 160   
        


window = display.set_mode((1400, 1000))
display.set_caption('Шутер')

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

hero = Player('rocket.png', 0, 850, 15, hero_wildth, hero_height)
bullet = Bullet('bullet.png', 500, 800, 15, bullet_wildth, bullet_height)


asteroids = sprite.Group()
monsters = sprite.Group()
bullets = sprite.Group()
for i in range(5):
    b = randint(0, 1250)
    enemy_speed = randint(1, 5)
    monsters.add(Enemy('ufo.png', b, 0, enemy_speed, enemy_wildth, enemy_height))

for i in range(2):
    asteroids.add(Asteroid('asteroid.png', randint(0, 1250), 0, randint(3, 9), asteroid_wildth, asteroid_height))


lost = 0
kills = 0

font.init()
size = font.SysFont('Arial', 50)
text = font.SysFont('Arial', 200)

lose = text.render('YOU LOSE', True, (255, 0, 0))
win = text.render('YOU WIN', True, (0, 100, 255))

clock = time.Clock()
bullet_delay = 0
FPS = 200

background = transform.scale(image.load('galaxy.jpg'), (1400, 1000))
game = True
finish = False
while game:
    
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        window.blit(background, (0, 0))

        bullets.draw(window)
        bullets.update()

        asteroids.draw(window)
        asteroids.update()

        monsters.draw(window)
        monsters.update()

        hero.reset()
        if hero.lives <= 0:
            
            window.blit(lose, (350, 450))
            finish = True
        hero.update()
    

        miss = size.render('Пропущено:'+str(lost), True, (255, 255, 255))
        strike = size.render('Счет:'+str(kills), True, (255, 255, 255))

        window.blit(miss, (5, 60))
        window.blit(strike, (5, 20))
        

        sprite_list = sprite.spritecollide(hero, monsters, False)
        strike_list = sprite.spritecollide(hero, asteroids, False)
        

        

        if lost > 2:
            window.blit(lose, (350, 450))
            finish = True

        if kills > 19:
            window.blit(win, (350, 450))
            finish = True

        monster_list = sprite.groupcollide(monsters, bullets, False, True)
        for monster in monster_list:
            monster.start_pos()

        for enemy in sprite_list:
            hero.live_count()
            if hero.lives >= 1:
                enemy.start_pos()

        for asteroid in strike_list:
            hero.live_count()
            if hero.lives >= 1:
                asteroid.start()
            
            

    



    clock.tick(FPS)
    display.update()
