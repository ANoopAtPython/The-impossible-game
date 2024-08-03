import pygame
import math
from random import randint as rand
pygame.init()

Width , Height = 800 , 600
screen = pygame.display.set_mode((Width , Height))

BLACK = (0,0,0)#boss
WHITE = (255,255,255)#screen
RED = (255,0,0)#player bullet
YELLOW = (255,255,0)#boss bullet
SKY_BLUE = (135, 206, 235)#player
GREEN = (0 , 128 , 0)#sth move from top to bottom to cause havoc


#player and bullet
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player , self).__init__()
        self.surf = pygame.Surface((20 , 20))
        self.surf.fill(SKY_BLUE)
        self.rect = self.surf.get_rect(center = (600 , 300))
        self.health = 1000
    def Movement(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_a]:
            self.rect.move_ip(-3 , 0)
        if pressed_keys[pygame.K_d]:
            self.rect.move_ip(3 , 0)
        if pressed_keys[pygame.K_w]:
            self.rect.move_ip(0 , -3)
        if pressed_keys[pygame.K_s]:
            self.rect.move_ip(0 , 3)

        self.rect.top = max(self.rect.top , 0)
        self.rect.bottom = min(self.rect.bottom , Height)
        self.rect.left = max(self.rect.left , 200)
        self.rect.right = min(self.rect.right , Width)
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
player_group = pygame.sprite.Group()
player = Player()
player_group.add(player)

class Bulletin(pygame.sprite.Sprite):
    def __init__(self , x , y , cach):
        super().__init__()
        self.surf = pygame.Surface((10 , 5))
        self.surf.fill(RED)
        self.x = x
        self.y = y
        self.cach = cach
        self.rect = self.surf.get_rect(center = (self.x, self.y +  + self.cach))
    def Movement(self):
        self.rect.move_ip(-5 , 0)
        if self.rect.left < 0:
            self.kill()
Bulletin_Group = pygame.sprite.Group()
Add_Bullet = pygame.USEREVENT + 1
pygame.time.set_timer(Add_Bullet , 200)

#Boss (move up and down)
class Boss(pygame.sprite.Sprite):
    def __init__(self , x , y , move , speed):
        super(Boss , self).__init__()
        self.surf = pygame.Surface((80 , 80))
        self.x = x
        self.y = y
        self.surf.fill(BLACK)
        self.rect = self.surf.get_rect(center = (self.x , self.y))
        self.move = move #0 = down , 1 = up
        self.speed = speed
        self.health = 10e9
    def Movement(self):
        self.rect.move_ip(0 , self.speed)
        if self.move == 0:
            if self.rect.bottom >= 550:
                self.speed = -self.speed
                self.move = 1
        if self.move == 1:
            if self.rect.top <= 50:
                self.speed = -self.speed
                self.move = 0
    def IsAlive(self):
        if self.health > 0:
            screen.blit(self.surf , self.rect)

boss_group = pygame.sprite.Group()
boss_group_2 = pygame.sprite.Group()
boss = Boss(150 , 100 , 0 , 3)
boss2 = Boss(50 , 500 , 1 , -3)
boss_group.add(boss)
boss_group_2.add(boss2)

#spreadsh*t
class spreadshot(pygame.sprite.Sprite):
    def __init__(self , x , y , Up_Or_Down):
        super(spreadshot , self).__init__()
        self.x = x
        self.y = y
        self.Up_Or_Down = Up_Or_Down
        self.surf = pygame.Surface((10 , 10))
        self.surf.fill(YELLOW)
        self.rect = self.surf.get_rect(center = (self.x + 40 , self.y + 40))
        self.angle = 0
    def Movement(self):
        if self.Up_Or_Down == 0:
            self.rect.move_ip(5 , 0)
        elif self.Up_Or_Down == 1:
            self.angle = math.radians(20)
            self.rect.move_ip(5, 5 * math.sin(self.angle))
        elif self.Up_Or_Down == 2:
            self.angle = math.radians(40)
            self.rect.move_ip(5 , 5 * math.sin(self.angle))
        elif self.Up_Or_Down == -1:
            self.angle = math.radians(20)
            self.rect.move_ip(5 ,  -5 * math.sin(self.angle))
        elif self.Up_Or_Down == -2:
            self.angle = math.radians(40)
            self.rect.move_ip(5 , -5 * math.sin(self.angle))

#Make some sus bullet
spreadshot_group = pygame.sprite.Group()
Add_Spread = pygame.USEREVENT + 1
pygame.time.set_timer(Add_Spread , 300)

#enemy up to down like meteorite
class meteorite_up(pygame.sprite.Sprite):
    def __init__(self):
        super(meteorite_up , self).__init__()
        self.surf = pygame.Surface((10 , 10))
        self.surf.fill(GREEN)
        self.rect = self.surf.get_rect(
            center = (
                rand(200 , Width) ,
                -20
            )
        )
        self.speed = 7
    def Movement(self):
        self.rect.move_ip(0 , self.speed)
        if self.rect.bottom > Height:
            self.kill()
meteorite_group_up = pygame.sprite.Group()
Add_Meteorite_Up = pygame.USEREVENT + 2
pygame.time.set_timer(Add_Meteorite_Up , 600)

class meteorite_down(pygame.sprite.Sprite):
    def __init__(self):
        super(meteorite_down , self).__init__()
        self.surf = pygame.Surface((10 , 10))
        self.surf.fill(GREEN)
        self.rect = self.surf.get_rect(
            center = (
                rand(200 , Width) ,
                Height + 20
            )
        )
        self.speed = 7
    def Movement(self):
        self.rect.move_ip(0 , -self.speed)
        if self.rect.top < 0:
            self.kill()
meteorite_group_down = pygame.sprite.Group()
Add_Meteorite_Down = pygame.USEREVENT + 3
pygame.time.set_timer(Add_Meteorite_Down , 600)

clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.QUIT:
            running = False
        elif event.type == Add_Bullet:
            i,j = player.rect[:2]
            Bullet2 = Bulletin(i , j , 7)
            Bulletin_Group.add(Bullet2)
        if event.type == Add_Spread:
            if boss.health > 0:
                i,j = boss.rect[:2]
                n1 , n2 , n3 , n4 , n5 = spreadshot(i , j , 2) , spreadshot(i , j , 1) , spreadshot(i , j , 0) , spreadshot(i , j , -1) , spreadshot(i , j , -2)
                spreadshot_group.add(n1)
                spreadshot_group.add(n2)
                spreadshot_group.add(n3)
                spreadshot_group.add(n4)
                spreadshot_group.add(n5)

            if boss2.health > 0:
                i,j = boss2.rect[:2]
                n1 , n2 , n3 , n4 , n5 = spreadshot(i , j , 2) , spreadshot(i , j , 1) , spreadshot(i , j , 0) , spreadshot(i , j , -1) , spreadshot(i , j , -2)
                spreadshot_group.add(n1)
                spreadshot_group.add(n2)
                spreadshot_group.add(n3)
                spreadshot_group.add(n4)
                spreadshot_group.add(n5)
        if event.type == Add_Meteorite_Up:
            New_Meteorite = meteorite_up()
            meteorite_group_up.add(New_Meteorite)
        if event.type == Add_Meteorite_Down:
            New_Meteorite = meteorite_down()
            meteorite_group_down.add(New_Meteorite)

    player.Movement()
    boss.Movement()
    boss2.Movement()
    screen.fill(WHITE)
    screen.blit(player.surf , player.rect)
    boss.IsAlive()
    boss2.IsAlive()

    if boss.health <= 0 and boss2.health <= 0:
        running = False

    for bl1 in Bulletin_Group:
        bl1.Movement()
        screen.blit(bl1.surf , bl1.rect)
        if pygame.sprite.spritecollideany(bl1 , boss_group):
            boss.health -= 1
            bl1.kill()
            if boss.health == 0:
                boss.kill()
        if pygame.sprite.spritecollideany(bl1 , boss_group_2):
            boss2.health -= 1
            bl1.kill()
            if boss2.health == 0:
                boss2.kill()

    for spsh in spreadshot_group:
        spsh.Movement()
        screen.blit(spsh.surf , spsh.rect)
        if pygame.sprite.spritecollideany(spsh , player_group):
            player.health -= 5
            spsh.kill()
            if player.health == 0:
                player.kill()
                running = False

    for mtr in meteorite_group_up:
        mtr.Movement()
        screen.blit(mtr.surf , mtr.rect)
        if pygame.sprite.spritecollideany(mtr , player_group):
            player.health -= 1
            mtr.kill()
            if player.health == 0:
                player.kill()
                running = False

    for mtr in meteorite_group_down:
        mtr.Movement()
        screen.blit(mtr.surf , mtr.rect)
        if pygame.sprite.spritecollideany(mtr , player_group):
            player.health -= 1
            mtr.kill()
            if player.health == 0:
                player.kill()
                running = False

    pygame.display.flip()
pygame.quit()
if player.health > 0:
    print("You win")
elif player.health == 0 and boss1.health == 0 and boss2.health == 0:
    print("Draw")
else:
    print("you lose")
