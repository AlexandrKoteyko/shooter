from pygame import *
from random import randint

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
font.init()
font2= font.Font(None,36)              
font1=font.Font(None, 80)
win=font1.render('YOU WIN!', True, (255,255,255))
lose=font1.render("YOU LOSE!", True, (180,0,0))
score=0
lost=0
goal=10
max_lost=3
img_back = "galaxy.jpg"
img_hero="rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
        super().__init__()
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
        bullet=Bullet(img_bullet,self.rect.centerx, self.rect.top, 15, randint(1,400),randint(1,400))
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_heigth:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y-=self.speed
        if self.rect.y<0:
            self.kill()

win_width = 700
win_heigth = 500

display.set_caption("Shooter")
window=display.set_mode((win_width, win_heigth))
background = transform.scale(image.load(img_back), (win_width, win_heigth))

ship = Player(img_hero, 5, win_heigth - 100, 40, 100, 100)
bullets=sprite.Group()
monsters = sprite.Group()
for i in range(1,6):
    # def __init__(self, player_image, player_x,                    player_y, player_speed,      size_x,     size_y):
    monster = Enemy(      img_enemy,   randint(80, win_width - 80), -40,          randint(1,5),    50,   50)
    monsters.add(monster)


finish = False
run = True

while run:
    for e in event.get():
        if e.type==QUIT:
            run= False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()
    if not finish:
        window.blit(background, (0, 0))

        
        text = font2.render("Рахунок: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено:"+ str(lost), 1, (255,255,255))
        window.blit(text_lose, (10, 50))

        ship.update()
        monsters.update()
        bullets.update()
        monsters.draw(window)   

        ship.reset()
        bullets.draw(window)

        collides=sprite.groupcollide(monsters,bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, randint(1,5), 50, 50)
            monsters.add(monster)

        if sprite.spritecollide(ship,monsters, False) or lost>=max_lost:
            finish=True
            window.blit(lose, (200,200))

        if score>= goal:
            finish=True
            window.blit(win, (200,200))



        display.update()

    time.delay(50)