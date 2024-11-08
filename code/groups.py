from settings import *

class BackgroundGroupSingle(pygame.sprite.GroupSingle):
    def __init__(self, displaySurface):
        super().__init__()
        self.displaySurface = displaySurface
    def draw(self, layer):
        self.displaySurface.blit(layer,(0,0))