import os
from config import RESOURCES, STARRAIL, SFONTS
from PIL import Image, ImageDraw, ImageFont

from mihomo.client import MihomoAPI
from mihomo.models.character import Character
from mihomo.models.equipment import LightCone, Relic, RelicSet

FONT = os.path.join(SFONTS, "star-rail.ttf")
PROFILE = os.path.join(STARRAIL, "profile")
BASE =  os.path.join(PROFILE, "base")
MATERIAL = os.path.join(BASE, "materials")
DONE = os.path.join(PROFILE, "done")
BASE_IMAGE = os.path.join(BASE, "profile.png")

LIST_OF_PATHS = [
    FONT, PROFILE, BASE, MATERIAL, DONE, BASE_IMAGE
]


def file_path_check():
    for i in LIST_OF_PATHS:
        print(os.path.exists(i))



class ImageDrawing:
    def __init__(self, characters:list[Character] | Character, client):
        self.character = characters[0] if isinstance(characters, list) else characters
        self.client:MihomoAPI = client

        self.file_save()

    
    def file_save(self):
        target_files = [
            self.character.preview,
            #self.character.light_cone.preview,
            
            self.character.icon
        ].extend([i.icon for i in self.character.relics])
        #print(self.character.relics[0].)
        print((self.character.relics[0]))
        
        [print(self.client.get_icon_url(i)) for i in target_files]