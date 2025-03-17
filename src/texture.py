import moderngl as gl
from PIL import Image as im

class Texture:
    def __init__(self, path):
        glContext = gl.get_context()

        image = im.open(path).convert("RGB")
        self.texture = glContext.texture(image.size, 3, image.tobytes())
        self.sampler = glContext.sampler(texture = self.texture)

    def use(self):
        self.sampler.use()