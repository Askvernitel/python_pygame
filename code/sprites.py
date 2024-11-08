
from settings import *
from helper import ImageLoader

class Background(pygame.sprite.Sprite):
    def __init__(self, groups):
        #load stuff 
        super().__init__(groups)
        self.imageLoader = ImageLoader()
        self.loadLayers()
        self.scaleLayers()
        
        self.groundLayer = self.layers[4]
        
        #self.loadRectangles() for now don't need 
        
        
        
    def loadLayers(self):
        #transform
        self.layers = self.imageLoader.loadImagesIntoArrayByPath(join("sprites", "background", "background_layers"))
        
        #load layers from directory
        """for filePath, folders, files in walk():
            for file in sorted(files, key = lambda name:name[0]): 
                fullPath = join(filePath, file)
                self.layers.append(pygame.image.load(fullPath).convert_alpha())
           """     
        
        
    def loadRectangles(self):
        self.rectangles = []
        for layer in self.layers:
            self.rectangles.append(layer.get_rect(bottomleft = (0, SCREEN_HEIGHT)))
    def scaleLayers(self):
        self.layers = [pygame.transform.scale(layer, (SCREEN_WIDTH, SCREEN_HEIGHT)) for layer in self.layers]
        
    def update(self):
        pass
    
    

class HeartHUD(pygame.sprite.Sprite):
    def __init__(self,frames, position, heartIndex, groups):
        super().__init__(groups)
        #general
        self.heartIndex = heartIndex
        self.frames = frames
        self.loseHeartAnimationIndex = 0
        self.loseHeartAnimationSpeed = 10
        self.loadImages()
        self.rect = self.image.get_rect(topleft = position)
        
        #booleans
        self.isLosingHeart = False
    def startLoseHeartAnimation(self):
        self.isLosingHeart = True
    def loseHeartAnimation(self, delta): 
        if self.isLosingHeart and self.loseHeartAnimationIndex < len(self.frames):
            self.image = self.frames[int(self.loseHeartAnimationIndex)]
            self.loseHeartAnimationIndex += self.loseHeartAnimationSpeed * delta
    def loadImages(self):
        self.image = self.frames[0]
    def update(self, delta):
        self.loseHeartAnimation(delta)

class ScoreHUD(pygame.sprite.Sprite):
    def __init__(self,position,fontSize, groups):
        super().__init__(groups)
        self.font = pygame.font.Font(join("fonts", "font2.ttf"), fontSize)
        self.score = 0
        self.color = "black"
        self.image = self.font.render(str(self.score), False, self.color)
        self.rect = self.image.get_rect(center = position)    
    def increaseScoreByValue(self, value):
        self.score+=value 
        self.image = self.font.render(str(self.score),False, self.color)
    def update(self, delta):
        pass

class HUD():
    def __init__(self, groups):
        self.groups = groups
        self.heartHUDScalefactor = 5
        self.imageLoader = ImageLoader()
        self.heartsHUD = []
        self.loadImages()
        
    def placeHearts(self, amount, position):
        margin = pygame.Vector2(10,10)
        self.heartAmount = amount
        for element in range(amount):
            heart = HeartHUD(self.heartFrames, position + margin, element, self.groups)
            position = heart.rect.topleft
            self.heartsHUD.append(heart)
        self.heartsHUD.sort(key = lambda heart: heart.heartIndex)
    def placeScore(self, position):
        self.score = ScoreHUD(position, 50, self.groups)
    def increaseHUDScoreByValue(self,value):
        self.score.increaseScoreByValue(value)
    def loseHeart(self, delta):
        lastHeartIndex = self.heartAmount - 1
        self.heartAmount -= 1
        if self.heartAmount >= 0:
            self.heartsHUD[lastHeartIndex].startLoseHeartAnimation()
            
    def loadImages(self):
        self.heartFrames = self.imageLoader.loadScaledByImagesIntoArrayByPath(join("sprites", "hud", "hearts_hp"), self.heartHUDScalefactor)
    def update(self, delta):
        pass 
    
    
class Button(pygame.sprite.Sprite):
    def __init__(self, position, font, text, textColor,  groups, scaleWidthHeight, offsetXY, textOffsetXY):
        super().__init__(groups)
        #general
        self.imageLoader = ImageLoader()
        self.scaleWidthHeight = scaleWidthHeight
        self.loadImages()
        self.offsetXY = pygame.Vector2(offsetXY)
        self.textOffsetXY = pygame.Vector2(textOffsetXY)
        self.position = position
        self.rect = self.image.get_rect(center=position+self.offsetXY)
        
        
        #text
        self.text = font.render(text, False, textColor).convert_alpha()
        self.textRect = self.text.get_rect(center = (self.image.get_width()/2, self.image.get_height()/2) + self.textOffsetXY)
        self.image.blit(self.text, self.textRect)
        self.originalImage.blit(self.text, self.textRect)
        #mask
        self.image.blit(self.maskSurface, (0,0))

        #stuff 
        #mouse input 
        self.prevMouseInput = None
        self.mouseInput = None
    def loadImages(self):
        
        self.originalFrames = self.imageLoader.loadScaledImagesIntoArrayByPath(join("sprites", "UI", "Button"), self.scaleWidthHeight)
        self.frames = self.imageLoader.loadScaledImagesIntoArrayByPath(join("sprites", "UI", "Button"), self.scaleWidthHeight)
        self.originalImage = self.originalFrames[0]
        self.image = self.frames[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.maskSurface = self.mask.to_surface( setcolor=(255,255,255,100), unsetcolor=(0,0,0,0))
    def getMouseInput(self):
        self.prevMouseInput = self.mouseInput
        self.mouseInput = pygame.mouse.get_pressed()
        self.mousePosition = pygame.mouse.get_pos()
    def buttonPressAnimation(self):
        pass

    def buttonHoverEffect(self):
        if self.rect.collidepoint(self.mousePosition):
            self.image = self.originalImage
        else:
            self.image = self.frames[0]
    def buttonIsClicked(self):
        return self.rect.collidepoint(self.mousePosition) and self.mouseInput[0] and (self.prevMouseInput and self.mouseInput[0] != self.prevMouseInput[0])
    def update(self, changeStateMethod, delta):
        self.getMouseInput()
        self.buttonHoverEffect()


class StartButton(Button):
    def __init__(self, position, font, text, textColor,  groups, scaleWidthHeight, offsetXY, textOffsetXY):
        super().__init__(position, font, text, textColor,  groups, scaleWidthHeight, offsetXY, textOffsetXY)
        
        
    def checkButton(self, changeStateMethod):
        
        if super().buttonIsClicked():
            changeStateMethod('menu')
    
    
    def update(self, changeGameStateMethod, delta):
        super().update(changeGameStateMethod, delta)
        self.checkButton(changeGameStateMethod)

class QuitButton(Button):
    
    def __init__(self, position, font, text, textColor,  groups, scaleWidthHeight, offsetXY, textOffsetXY):
        super().__init__(position, font, text, textColor,  groups, scaleWidthHeight, offsetXY, textOffsetXY)
        
    def checkButton(self, changeStateMethod):
        if super().buttonIsClicked():
            changeStateMethod('game')
            
    def update(self, changeGameStateMethod, delta):
        super().update(changeGameStateMethod,delta)
        self.checkButton(changeGameStateMethod)
        
class Title(pygame.sprite.Sprite):
    def __init__(self, title ,position, fontSize, color, groups):
        super().__init__(groups)
        #general
        self.font = pygame.font.Font(join("fonts", "font2.ttf"), fontSize)
        self.originalFontSurface = self.font.render(title, False, color)
        self.image = self.font.render(title, False, color)
        self.rect = self.image.get_rect(center = position)
        self.position =position

        #animation
        self.scaleAnimationFactor = 1
        self.maxScaleFactor = 2
        self.minScaleFactor = 1.5
        self.scaleSpeed = 0.7
        self.isExpanding = True 
    def animateText(self, delta):
        if self.scaleAnimationFactor >= self.maxScaleFactor: 
            
            self.isExpanding = False 
        if self.scaleAnimationFactor <= self.minScaleFactor:
            self.isExpanding = True
            
        self.image = pygame.transform.scale_by(self.originalFontSurface, self.scaleAnimationFactor)
        self.scaleAnimationFactor += self.scaleSpeed *delta if self.isExpanding else -self.scaleSpeed *delta
        
        self.rect = self.image.get_rect(center=self.position)
            
    def update(self, _, delta):
        self.animateText(delta)
        
        
    