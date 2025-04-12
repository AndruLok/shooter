#Создай собственный Шутер!
from pygame import *
from random import *
window = display.set_mode((700, 500))
display.set_caption('Космос')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
clock = time.Clock()
FPS = 60
game = True
finish = False
mixer.init()
mixer.music.load('space.ogg')
fire_sound = mixer.Sound('fire.ogg')
mixer.music.play()
# money = mixer.Sound('money.ogg')
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_xsize, player_ysize):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_xsize, player_ysize))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.player_xsize = player_xsize
        self.player_ysize = player_ysize
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
bullets = sprite.Group()
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_d] and self.rect.x < 595:
            self.rect.x += self.speed
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)
hero = Player('rocket.png', 250, 400, 7, 150, 75)
lost = 0
win = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(30, 670)
            self.rect.y = 0
            lost = lost + 1
monsters = sprite.Group()
for i in range(5):
    en = Enemy('ufo.png', randint(30, 620), 0, randint(1,3), randint(45, 120), randint(20, 60))
    monsters.add(en)
font.init()
font1 = font.SysFont('Arial', 36)
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed  
        if self.rect.y < 0:
            self.kill()
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.x = randint(30, 670)
            self.rect.y = 0
asteroids1 = sprite.Group()
for i in range(8):
    ast = Asteroid('asteroid.png', randint(30, 620), 0, randint(1,2), randint(30, 60), randint(50, 70))
    asteroids1.add(ast)
asteroids2 = sprite.Group()
for i in range(8):
    ast2 = Asteroid('kometa.png', randint(30, 620), 0, randint(1,2), randint(40, 70), randint(70, 90))
    asteroids2.add(ast2)
asteroids3 = sprite.Group()
for i in range(8):
    ast3 = Asteroid('zvezda.png', randint(30, 620), 0, randint(1,2), randint(20, 50), randint(30, 60))
    asteroids3.add(ast3)
text_victory = font1.render('YOU WIN!', True, (255, 255, 0))
text_l = font1.render('YOU LOOSE!', True, (255, 0, 0))
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                hero.fire()
            elif e.key == K_r:
                if finish == True:
                    finish = False
                    win = 0
                    lost = 0
                    for em in monsters:
                        em.kill()
                    for aster in asteroids1:
                        aster.kill()
                    for a in asteroids2:
                        a.kill()
                    for z in asteroids3:
                        z.kill()
                    for i in range(8):
                        ast = Asteroid('asteroid.png', randint(30, 620), 0, randint(1,2), randint(30, 60), randint(50, 70))
                        asteroids1.add(ast)
                    for i in range(8):
                        ast2 = Asteroid('kometa.png', randint(30, 620), 0, randint(1,2), randint(40, 70), randint(70, 90))
                        asteroids2.add(ast2)
                    for i in range(8):
                        ast3 = Asteroid('zvezda.png', randint(30, 620), 0, randint(1,2), randint(20, 50), randint(30, 60))
                        asteroids3.add(ast3)
                    for i in range(5):
                        en = Enemy('ufo.png', randint(30, 620), 0, randint(1,3), randint(45, 120), randint(20, 60))
                        monsters.add(en)
    if finish != True:
        window.blit(background,(0,0))
        hero.update()
        hero.reset()
        bullets.draw(window)
        bullets.update()
        monsters.update()
        monsters.draw(window)
        asteroids1.draw(window)
        asteroids1.update()
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        for i in sprites_list:
            win += 1
            en = Enemy('ufo.png', randint(30, 620), 0, randint(1,3), randint(45, 120), randint(20, 60))
            monsters.add(en)
        if win >= 25:
            finish = True
            window.blit(text_victory, (250, 250))
        if sprite.spritecollide(hero, monsters, False):
            finish = True
            window.blit(text_l, (250, 250))
        if lost >= 10:
            finish = True
            window.blit(text_l, (250, 250))
        if win >= 15:
            asteroids2.update()
            asteroids2.draw(window)
        if win >= 10:
            asteroids3.update()
            asteroids3.draw(window)    
        aster_list = sprite.groupcollide(asteroids1, bullets, True, True)
        aster_list2 = sprite.groupcollide(asteroids2, bullets, True, True)
        aster_list3 = sprite.groupcollide(asteroids3, bullets, True, True)
        text_lose = font1.render('Пропущено: ' + str(lost), 1, (255, 0, 0))
        text_win = font1.render('Сбито: ' + str(win), 1, (0, 255, 0))  
        window.blit(text_lose, (23, 50))
        window.blit(text_win, (23, 20))
    display.update()
    clock.tick(FPS)