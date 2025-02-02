from pygame import *

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

img_back = "galaxy.jpg"
img_hero="rocket.png"

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
        pass

win_width = 700
win_heigth = 500

display.set_caption("Shooter")
window=display.set_mode((win_width, win_heigth))
background = transform.scale(image.load(img_back), (win_width, win_heigth))

ship = Player(img_hero, 5, win_heigth - 100, 80, 100, 10)
finish = False
run = True

while run:
    for e in event.get():
        if e.type==QUIT:
            run= False
