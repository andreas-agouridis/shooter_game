from pygame import *
from random import randint
import time

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font2 = font.Font(None, 36)

img_back = "galaxy.jpg" 
img_hero = "rocket.png" 
img_enemy = "ufo.png" 
img_bullet = "bullet.png" 

score = 0 
lost = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):        
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
   def update(self):
       self.rect.y += self.speed
       if self.rect.y < 0:
           self.kill()
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
bullets = sprite.Group()

finish = False
player_lives = 3 

run = True
rip = time.time()

while run:
    current_time = time.time()
    
    if current_time - rip > 20:
        rip = current_time
        score = 0
        lost = 0
        player_lives = 3
        finish = False
        ship.rect.x = 5
        ship.rect.y = win_height - 100
        monsters.empty()
        bullets.empty()
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
    
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
                fire_sound.play()

    if not finish:
        window.blit(background,(0,0))

        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        hits = sprite.groupcollide(monsters, bullets, True, True)
        for hit in hits:
            score += 1
            if score >= 10: 
                finish = True
                win_text = font2.render("YOU WIN!", 1, (255, 255, 0))
                window.blit(win_text, (win_width//2 - 70, win_height//2 - 20))
            else:
                enemy = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(2, 4))
                monsters.add(enemy)

        if sprite.spritecollide(ship, monsters, True):
            player_lives -= 1
            if player_lives <= 0:
                finish = True
                lose_text = font2.render("YOU LOST!", 1, (255, 0, 0))
                window.blit(lose_text, (win_width//2 - 80, win_height//2 - 20))

        if lost >= 3:  
            finish = True
            lose_text = font2.render("YOU LOST!", 1, (255, 0, 0))
            window.blit(lose_text, (win_width//2 - 80, win_height//2 - 20))

        ship.update()
        monsters.update()
        bullets.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        display.update()
    time.sleep(0.05)