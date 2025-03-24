import moderngl as gl
from PIL import Image as im

from pathHandler import getPath

class Texture:
    def __init__(self, path):
        glContext = gl.get_context()

        image = im.open(getPath(path)).convert("RGB")
        self.texture = glContext.texture(image.size, 3, image.tobytes())
        self.texture.build_mipmaps()
        #self.sampler = glContext.sampler(texture = self.texture)

    def use(self):
        self.texture.use()
        #self.sampler.use()