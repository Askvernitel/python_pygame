from settings import *
from helper import ImageLoader


class Gun(pygame.sprite.Sprite):
    def __init__(self, surf, player, enemyGroup, bulletGroup, bulletsPerSecond, recoilKnockback, groups):
        super().__init__(groups)
        # general
        self.imageLoader = ImageLoader()
        self.originalImage = surf
        self.image = surf
        self.rect = self.image.get_rect(center=player.position)

        self.player = player
        self.bulletsPerSecond = bulletsPerSecond
        self.recoilKnockback = recoilKnockback
        self.direction = pygame.Vector2(1, 0)

        self.offset = 100

        # stats
        self.shootCooldown = 500 // bulletsPerSecond  # 1000 miliseconds
        # recoilAnimationSpeed // shootCooldown -> will be used
        self.recoilAnimationSpeed = 500
        # bullets
        self.bulletScaleFactor = 4
        self.bulletSurface = self.imageLoader.importScaledByImage(
            join("sprites", "bullets", "type1", "1.png"), self.bulletScaleFactor)

        # booleans
        self.canShoot = False

        # time
        self.lastShootTime = pygame.time.get_ticks()
        # groups
        self.bulletGroup = bulletGroup
        self.gunGroups = groups
        self.enemyGroup = enemyGroup

    def moveTowardsMouse(self):
        mousePosition = pygame.Vector2(
            pygame.mouse.get_pos())-self.player.rect.center

        mouseDirection = mousePosition.normalize()

        self.direction = mouseDirection

    def shoot(self):
        # 0 == left click
        if (self.mouseInput[0] or self.input[pygame.K_LSHIFT]) and self.canShoot:
            DefaultBullet(self.bulletSurface, self.rect.center, self.direction,
                          self.enemyGroup,  (self.gunGroups, self.bulletGroup))
            self.canShoot = False
            # self.recoilAnimation()
            self.getCurrentTime()
            self.lastShootTime = self.currentTime

    def getMouseInput(self):
        self.mouseInput = pygame.mouse.get_pressed()
        self.input = pygame.key.get_pressed()

    def lookAtMouse(self):
        angle = degrees(atan2(self.direction.x, self.direction.y)) - 90

        self.flippedImage = pygame.transform.flip(
            self.originalImage, False, True) if self.direction.x < 0 else self.originalImage
        self.image = pygame.transform.rotate(self.flippedImage, angle)

    def fixPosition(self):
        self.rect.center = self.player.rect.center + self.direction * self.offset

    def recoilAnimation(self, state):
        if state == "going_back":
            self.rect.center -= self.recoilAnimationSpeed//self.shootCooldown * self.direction
        if state == "going_forward":
            self.rect.center += self.recoilAnimationSpeed//self.shootCooldown * self.direction

    def getCurrentTime(self):
        self.currentTime = pygame.time.get_ticks()

    def checkShootCooldown(self):
        self.getCurrentTime()
        if self.currentTime - self.lastShootTime >= self.shootCooldown:
            self.canShoot = True
        elif self.currentTime - self.lastShootTime <= self.shootCooldown//2:
            self.recoilAnimation('going_back')
        else:
            self.recoilAnimation('going_forward')

    def update(self, delta):
        self.moveTowardsMouse()
        self.lookAtMouse()
        self.fixPosition()
        self.getMouseInput()
        self.checkShootCooldown()
        self.shoot()


class DefaultBullet(pygame.sprite.Sprite):
    def __init__(self, surf, position, direction, enemyGroup, groups):
        super().__init__(groups)
       # print(groups)
        # general
        self.image = surf
        self.direction = direction
        self.offset = 80 * self.direction

        self.rect = self.image.get_rect(center=position + self.offset)
        self.hitbox = self.rect
        self.speed = 800
        self.destroyTime = 4000  # miliseconds

        # Timers
        # self.setDestroyTimer()
        self.spawnTime = pygame.time.get_ticks()
        self.currentTime = self.spawnTime

        # groups
        self.enemyGroup = enemyGroup

    def moveWithDirection(self, delta):
        self.rect.center += self.direction * self.speed * delta

    def getCurrentTime(self):
        self.currentTime = pygame.time.get_ticks()

    def destroy(self):
        if self.currentTime - self.spawnTime >= self.destroyTime:
            self.kill()

    def collisions(self):
        for enemy in self.enemyGroup:
            if self.rect.colliderect(enemy.hitbox):
                enemy.takeDamage()
                self.kill()

        # print(self.rect.midbottom)
        if self.rect.bottom >= GROUND_Y_COORDINATE:
            self.kill()

    def changeHitboxPosition(self):
        self.hitbox.positon = self.rect.position

    def update(self, delta):
        self.getCurrentTime()
        self.moveWithDirection(delta)
        self.destroy()
        self.collisions()
