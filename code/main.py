from settings import *


from player import *
from groups import *
from sprites import *
from weapons import *
from helper import *
from enemies import *


class Game():
    def __init__(self):
        # general stuff
        pygame.init()
        self.displaySurface = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("The Game")
        self.clock = pygame.time.Clock()
        self.gameIsRunning = True
        self.menuIsRunning = True
        # fonts
        self.font = pygame.font.Font(join("fonts", "font2.ttf"), 50)

        # helpers
        self.imageLoader = ImageLoader()

        # important variables
        # aka collision with ground by y coordinate
        self.groundYCoordinate = GROUND_Y_COORDINATE

        # Sprite Groups
        self.allSprites = pygame.sprite.Group()
        self.backgroundGroupSingle = BackgroundGroupSingle(self.displaySurface)
        self.HUDGroup = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.bulletsGroup = pygame.sprite.Group()
        self.enemiesGroup = pygame.sprite.Group()
        self.MainMenuUIGroup = pygame.sprite.Group()

        # menu
        self.button = StartButton((SCREEN_WIDTH/2, SCREEN_HEIGHT/2), self.font, "Play", (0, 0, 0),
                                  (self.MainMenuUIGroup), (SCREEN_WIDTH/4, SCREEN_HEIGHT/4), (0, 0), (0, -20))
        self.button = QuitButton((SCREEN_WIDTH/2, SCREEN_HEIGHT/2), self.font, "Exit", (0, 0, 0),
                                 (self.MainMenuUIGroup), (SCREEN_WIDTH/4, SCREEN_HEIGHT/4), (0, 200), (0, -20))
        self.title = Title("The Game", (SCREEN_WIDTH/2, SCREEN_HEIGHT/4),
                           50, (0, 0, 0), (self.MainMenuUIGroup))
        # self.button = Button((SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 300), self.font, "Play", (0,0,0),  (self.MainMenuUIGroup), 400, 200)
        self.text = self.font.render(
            "Hello World!", False, "Black").convert_alpha()
        self.menuBackgroundColor = (232, 229, 155)

        # Temporary
        # self.loadObjects()
        # misc
        self.isMenuStartButtonClicked = False

    def draw(self, delta):
        for layer in self.background.layers:
            if layer == self.background.groundLayer:
                self.drawAllSpritesGroup(delta)
            self.backgroundGroupSingle.draw(layer)
        self.drawHUD(delta)

    def drawAllSpritesGroup(self, delta):

        self.allSprites.draw(self.displaySurface)
        self.allSprites.update(delta)

    def drawHUD(self, delta):
        self.HUDGroup.draw(self.displaySurface)
        self.HUDGroup.update(delta)
        # self.HUD.loseHeart(delta)

    def assignUpdatedGroupToObjects(self):
        self.player.enemiesGroup = self.enemiesGroup

    def changeRunningStates(self, state):
        if state == "menu":
            self.menuIsRunning = not self.menuIsRunning
            self.isMenuStartButtonClicked = True
        if state == "game":
            self.gameIsRunning = not self.gameIsRunning

    def loadObjects(self):
        self.HUD = HUD((self.HUDGroup))
        self.player = Player((SCREEN_WIDTH/2, SCREEN_HEIGHT/2),
                             self.groundYCoordinate, self.HUD, self.allSprites)
        self.gun = Gun(self.imageLoader.importScaledByImage(join("sprites", "guns", "ak47.png"), 5),
                       self.player, self.enemiesGroup, self.bulletsGroup, 10, 5, (self.allSprites))
        # self.enemy= Enemy(pygame.image.load(join("sprites", "enemies", "tree_enemy", "1.png")), self.player, (0,self.groundYCoordinate), (self.allSprites, self.enemiesGroup))
        self.enemySpawner = EnemySpawner(self.groundYCoordinate, [pygame.image.load(join(
            "sprites", "enemies", "tree_enemy", "1.png"))], 2000, 8, self.player,  (self.allSprites, self.enemiesGroup))

        self.background = Background(self.backgroundGroupSingle)
        self.HUD.placeHearts(self.player.heartsAmount, (0, 0))
        self.HUD.placeScore((SCREEN_WIDTH/2, 100))

    def runMainMenu(self, delta):
        self.displaySurface.fill(self.menuBackgroundColor)
        # self.displaySurface.blit(self.button, (40,40))
        self.MainMenuUIGroup.update(self.changeRunningStates, delta)
        self.MainMenuUIGroup.draw(self.displaySurface)
        pygame.display.update()

    def checkMenuButtonClick(self):
        if self.isMenuStartButtonClicked:
            self.loadObjects()
            self.isMenuStartButtonClicked = False

    def run(self):
        while self.gameIsRunning:
            delta = self.clock.tick(MAX_FRAMERATE)/1000  # seconds

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.changeRunningStates('game')
            self.checkMenuButtonClick()
            # loading continue stuff
            if self.menuIsRunning:
                self.runMainMenu(delta)
                continue

            # print(self.clock.get_fps())
            # Temporary
            self.enemySpawner.update()
            # Display
            # self.backgroundGroupSingle.update()
            # self.backgroundGroupSingle.draw()
            self.assignUpdatedGroupToObjects()
            self.draw(delta)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
