from settings import *


class EnemySpawner():

    def __init__(self, groundYCoordinate, enemySurfaces, timeBetweenSpawn, maxAmountOfEnemies, player, groups):
        self.enemySurfaces = enemySurfaces
        self.maxAmountOfEnemies = maxAmountOfEnemies
        self.groups = groups
        self.timeBetweenSpawn = timeBetweenSpawn
        self.player = player
        self.lastSpawnedTime = 0

        self.groundYCoordinate = groundYCoordinate
        # self.enemiesCount = 0

    def getCurrentTime(self):
        self.currentTime = pygame.time.get_ticks()

    def generateRandomPosition(self):
        position = None
        if randint(0, 1):
            position = (SCREEN_WIDTH + randint(100, 300),
                        self.groundYCoordinate)
        else:
            position = (0 - randint(100, 300), self.groundYCoordinate)
        return position

    def generateRandomEnemyIndex(self, enemySurfaces):
        return randint(0, len(enemySurfaces) - 1)

    def spawnEnemy(self):
        if self.currentTime - self.lastSpawnedTime >= self.timeBetweenSpawn and Enemy.enemyObjectCount <= self.maxAmountOfEnemies:
            enemyIndex = self.generateRandomEnemyIndex(self.enemySurfaces)
            pos = self.generateRandomPosition()
            enemy = Enemy(
                self.enemySurfaces[enemyIndex], self.player, pos, self.groups)
            self.lastSpawnedTime = self.currentTime
            # enemy.enemyObjectCount+=1

    def update(self):

        self.getCurrentTime()
        self.spawnEnemy()


class Enemy(pygame.sprite.Sprite):
    # static variables
    enemyObjectCount = 0

    def __init__(self, surf, player, position, groups):
        super().__init__(groups)
        Enemy.enemyObjectCount += 1
        # general
        self.scaleFactor = 5
        self.player = player
        # stats
        self.healthPoints = randint(10, 20)
        self.speed = randint(100, 300)
        self.isFlipped = False
        self.directionX = 1
        self.marginBetweenPlayer = 20
        # animation
        self.angleSpeed = 0.4

        # self.rotationAnimationSpeed=1
        self.rotationDirection = 1
        self.rotationCurrentFrame = 0
        self.rotationFrames = 20
        # load images and rects masks
        self.loadImages(surf)
        self.rect = self.image.get_rect(midbottom=position)

        self.mask = pygame.mask.from_surface(self.orginalImage)
        self.maskSurface = self.mask.to_surface(
            setcolor=(255, 255, 255, 200), unsetcolor=(0, 0, 0, 0))
        self.flippedMaskSurface = pygame.transform.flip(
            self.maskSurface, True, False)
        self.notflippedMaskSurface = self.maskSurface
        self.hitbox = self.rect.inflate(-70, -70)

    def loadImages(self, surf):
        self.orginalImage = pygame.transform.scale_by(surf, self.scaleFactor)
        self.flippedImageX = pygame.transform.flip(
            self.orginalImage, True, False)
        self.notFlippedImageX = self.orginalImage
        self.rotatedImage = pygame.transform.rotate(
            surf, self.angleSpeed * self.rotationFrames//2)
        self.rotatedImageReverse = pygame.transform.rotate(
            surf, -self.angleSpeed * self.rotationFrames)
        self.image = pygame.transform.scale_by(
            self.rotatedImage, self.scaleFactor)

    def movingRotatingAnimation(self, delta):
        self.angle = self.angleSpeed * (self.rotationFrames//2)
        if self.rotationDirection <= 0:
            self.rotate(self.angle * self.rotationDirection)
            self.angle -= self.angleSpeed * delta
        elif self.rotationDirection >= 0:
            self.rotate(self.angle * self.rotationDirection)
            self.angle += self.angleSpeed * delta

        self.rotationCurrentFrame += 1

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.orginalImage, angle)
        if self.rotationCurrentFrame == self.rotationFrames//2:
            self.rotationCurrentFrame %= (self.rotationFrames//2)
            self.rotationDirection *= -1

    def takeDamage(self):
        # self.image=self.orginalImage
        self.image = self.maskSurface
        self.player.HUD.increaseHUDScoreByValue(1)
        self.healthPoints -= 1

    def checkIfDead(self):
        if self.healthPoints <= 0:
            Enemy.enemyObjectCount -= 1
            self.kill()

    def flipOriginalImage(self):
        if self.isFlipped:
            self.orginalImage = self.flippedImageX
            self.maskSurface = self.flippedMaskSurface
        else:
            self.orginalImage = self.notFlippedImageX
            self.maskSurface = self.notflippedMaskSurface
        # self.orginalImage = self.flippedImageX if self.isFlipped else self.notFlippedImageX

    def moveTowardsPlayer(self, delta):
        if self.rect.centerx - self.player.rect.centerx >= self.marginBetweenPlayer:
            self.directionX = -1
            self.rect.centerx += self.directionX * self.speed * delta
            self.isFlipped = True
        elif self.rect.centerx - self.player.rect.centerx <= -self.marginBetweenPlayer:
            self.directionX = 1
            self.rect.centerx += self.directionX * self.speed * delta
            self.isFlipped = False

    def changeHitboxPosition(self):
        self.hitbox.center = self.rect.center
        # self.rect.centerx += -self.speed * delta if self.rect.centerx - self.player.rect.centerx > 0 else self.speed * delta

    def update(self, delta):
        self.movingRotatingAnimation(delta)
        self.moveTowardsPlayer(delta)
        self.changeHitboxPosition()
        self.flipOriginalImage()
        self.checkIfDead()


class TreeEnemy(Enemy):
    pass
