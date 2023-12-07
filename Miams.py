from Drawable import *
from Miam import *

class Miams(Drawable):
    
    def __init__(self, surface, camera, nb_miams):
        super().__init__(surface, camera)
        self.nb_miams = nb_miams
        self.list = []
        for i in range(self.nb_miams):
            self.list.append(Miam(self.surface, self.camera))
            
    def draw(self):
        for miam in self.list: 
            miam.draw()