from PIL import Image
import moderngl as gl

from texture import Texture

class Material:
    def __init__(self, baseColorPath):
        self.baseColorTexture = Texture(baseColorPath)

    def use(self):
        self.baseColorTexture.use()