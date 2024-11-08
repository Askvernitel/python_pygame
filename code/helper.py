from settings import * 
class ImageLoader():
    def __init__(self):
        pass
    
    def loadImagesIntoArrayByPath(self, path):
        result = []
        
        for filePath, folders, files in walk(path):
            for file in sorted(files, key = lambda name: name.split(".")[0]): 
                fullPath = join(filePath, file)
                result.append(pygame.image.load(fullPath).convert_alpha())
                
        return result 
    
    
    def loadScaledByImagesIntoArrayByPath(self, path, scale):
        result = []
        
        for filePath, folders, files in walk(path):
            for file in sorted(files, key = lambda name: name.split(".")[0]): 
                fullPath = join(filePath, file)
                result.append(pygame.transform.scale_by(pygame.image.load(fullPath).convert_alpha(), scale))
                
        return result 
    
    def loadScaledImagesIntoArrayByPath(self, path, scale):
        result = []
        
        for filePath, folders, files in walk(path):
            for file in sorted(files, key = lambda name: name.split(".")[0]): 
                fullPath = join(filePath, file)
                result.append(pygame.transform.scale(pygame.image.load(fullPath).convert_alpha(), scale))
                
        return result 
    def importScaledByImage(self, path, scale):
        
        return pygame.transform.scale_by(pygame.image.load(path).convert_alpha(), scale)
        
    """def loadScaledByImagesIntoArrayByPath(self, path, scale, flippedX, flippedY):
        result = []
        
        for filePath, folders, files in walk(path):
            for file in sorted(files, key = lambda name: name.split(".")[0]): 
                fullPath = join(filePath, file)
                scaledImage = pygame.transform.scale_by(pygame.image.load(fullPath).convert_alpha(), scale)
                result.append(pygame.transform.flip(scaledImage, flippedX, flippedY))
                
        return result """