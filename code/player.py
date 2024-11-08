from settings import * 
from helper import ImageLoader


class Player(pygame.sprite.Sprite):
    def __init__(self, position, groundYCoordinate, HUD, groups):
        #general
        super().__init__(groups)
        self.imageLoader = ImageLoader()
        self.scaleFactor = 5
        self.loadImages()
        self.rect = self.image.get_rect(center = position)
        
        #stats 
        self.position = position
        self.gravityConstant =1000
        self.gravitySpeed = 0
        self.canJump = False
        self.isOnGround = False 
        self.direction = pygame.math.Vector2(0,0)
        self.jumpSpeed = 700
        self.speed = 400
        self.heartsAmount = 5
        self.maxHeartsAmount = 10
        self.knockSpeed = 700
        #important variables
        self.groundYCoordinate = groundYCoordinate
        
        #animations 
        self.runAnimtionSpeed = 10
        self.idleAnimationSpeed = 5
        self.isFlippedToLeft = False #False == right
        
        self.runFrameIndex = 0 
        self.idleFrameIndex = 0 
        
        self.invincibilityAnimationIndex = 0
        self.invincibilityAnimationSpeed = 10
        self.invincibilityAnimationFrames = [self.image, self.maskSuface]
        #booleans
        self.isHit = False 
        self.isKnocked = False
        self.canMove = True
        #groups 
        self.enemiesGroup = []
        
        #objects
        self.HUD = HUD
        self.enemy = None
        
        #timer
        self.lastTimeHit = 0

        self.invincibilityTime = 1000
        self.knockDuration = 100 
        
        #mask
    def getCurrentTime(self):
        self.currentTime = pygame.time.get_ticks()
        
    def animateJump(self):
        pass 
    def animateIdle(self, delta):
        if self.direction.x == 0 and self.isOnGround:
            self.idleFrameIndex += self.idleAnimationSpeed * delta
            self.idleFrameIndex %= len(self.idleFrames)
            
            self.image = pygame.transform.flip(self.idleFrames[int(self.idleFrameIndex)], self.isFlippedToLeft, False)
            #update rect
            self.rect = self.image.get_rect(center = self.rect.center)
            
    def animateRun(self, delta):
        if self.direction.x > 0:
            #right 
            self.isFlippedToLeft = False
        elif self.direction.x < 0:
            #left
            self.isFlippedToLeft = True

        if self.direction.x:
            self.runFrameIndex += self.runAnimtionSpeed * delta
            self.runFrameIndex %= len(self.runFrames)
            
            
            self.image = pygame.transform.flip(self.runFrames[int(self.runFrameIndex)], self.isFlippedToLeft, False)
            self.rect = self.image.get_rect(center = self.rect.center)
            
    def getInput(self):
        self.input = pygame.key.get_pressed()
        
    def applyGravity(self,delta):
        
        
        if not self.isOnGround:
            self.gravitySpeed+=self.gravityConstant*delta
        else:
            self.gravitySpeed = 0
        self.rect.y +=self.gravitySpeed * delta
    
    def jump(self):
        if self.canJump and self.input[pygame.K_SPACE]: 
            self.gravitySpeed -= self.jumpSpeed
            self.canJump = False 
            self.isOnGround = False
        
    def movementX(self, delta):
        self.direction.x = int(self.input[pygame.K_d]) - int(self.input[pygame.K_a]) 
        
        self.rect.x += self.direction.x * self.speed * delta
        
    def checkIsOnGround(self, delta):
        if self.rect.bottom + self.gravitySpeed * delta>= self.groundYCoordinate: 
            self.rect.bottom = self.groundYCoordinate
            self.canJump = True
            self.isOnGround = True
    """def findAndSetCurrentInvicibilityAnimationMask(self):
        if self.isHit:
            for img, mask in self.allMasks:
                if self.image == img:
                    print("EE")
                    self.invincibilityAnimationFrames[1] = mask 
                    self.invincibilityAnimationFrames[0] = img
                    return
    """
    """def createMaskSurfacesForFrames(self, frames):
        masks = [pygame.mask.from_surface(frame) for frame in frames]
        masks = [mask.to_surface( setcolor=(255,255,255,100), unsetcolor=(0,0,0,0)) for mask in masks]
    
        for index, frame in enumerate(frames):
            self.allMasks.append((frame, masks[index]))    
        return masks"""
    
    def loadImages(self):
        #normalSizeImage = pygame.image.load(join("sprites", "player", "idle", "idle1.png")).convert_alpha()
        self.runFrames = self.imageLoader.loadScaledByImagesIntoArrayByPath(join("sprites", "player", "run"), self.scaleFactor)
        self.idleFrames = self.imageLoader.loadScaledByImagesIntoArrayByPath(join("sprites", "player", "idle"), self.scaleFactor)
        
        self.image = self.idleFrames[0]
        #self.image = pygame.transform.scale_by(normalSizeImage, self.scaleFactor)
        
       #self.allMasks = []
        self.mask = pygame.mask.from_surface(self.image)
        self.maskSuface = self.mask.to_surface( setcolor=(255,255,255,150), unsetcolor=(0,0,0,0))
        
        #self.runFramesMaskSurfaces = self.createMaskSurfacesForFrames(self.runFrames)
        #self.idleFramesMaskSurfaces = self.createMaskSurfacesForFrames(self.idleFrames)
        
    def hitKnockback(self, delta):
        if self.isKnocked and self.enemy:
            
            self.rect.x +=  self.enemy.directionX * self.knockSpeed * delta
            
    def checkIfKnocked(self):
        if self.currentTime - self.lastTimeHit >= self.knockDuration:
            self.isKnocked = False
            self.canMove = True
            
    def invincibilityAnimation(self,delta):
        self.invincibilityAnimationIndex += self.invincibilityAnimationSpeed * delta
        if self.isHit:
            #set current image
            if self.image != self.maskSuface:
                self.invincibilityAnimationFrames[0] = self.image 
                       
            self.image = self.invincibilityAnimationFrames[int(self.invincibilityAnimationIndex%len(self.invincibilityAnimationFrames))]
    def checkIfHit(self):
        if self.isHit and self.currentTime - self.lastTimeHit >= self.invincibilityTime:
            self.isHit = False
    
    
    def collision(self,delta):
        for enemy in self.enemiesGroup:
            if self.rect.colliderect(enemy.hitbox) and not self.isHit:
                self.isHit = True
                self.isKnocked = True
                self.canMove = False
                self.enemy = enemy
                self.heartsAmount -= 1
                self.lastTimeHit = self.currentTime
                self.HUD.loseHeart(delta)
                
    def movement(self, delta): 
        if self.canMove:

            self.movementX(delta)
            self.jump()
            
    def update(self, delta):
        #print(self.gravitySpeed)
        self.getCurrentTime()
        self.animateRun(delta)
        self.animateIdle(delta)
        
        self.getInput()
        self.checkIsOnGround(delta)
        self.movement(delta)
        self.applyGravity(delta)
        
        
        #collisions
        
        #self.findAndSetCurrentInvicibilityAnimationMask()
        self.hitKnockback(delta)
        self.checkIfKnocked()
        self.checkIfHit()
        self.collision(delta)
        self.invincibilityAnimation(delta)
        #------------
        
