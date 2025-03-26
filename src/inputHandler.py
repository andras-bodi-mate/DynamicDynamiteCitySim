import pynput
import glm

class InputHandler:
    def __init__(self, mouseCenter):
        self.mouse = pynput.mouse.Controller()
        self.pressedKeys = {}

        self.mouseCenter = mouseCenter

        self.keyboardListener = pynput.keyboard.Listener(on_press = self.keyPressed, on_release = self.keyReleased)
        self.keyboardListener.start()

    def convertKeyCode(self, key):
        if type(key) == pynput.keyboard.KeyCode:
            return pynput.keyboard.KeyCode.from_char(key.char.lower())
        return key

    def keyPressed(self, key: pynput.keyboard.Key):
        self.pressedKeys[self.convertKeyCode(key)] = True

    def keyReleased(self, key: pynput.keyboard.Key):
        self.pressedKeys[self.convertKeyCode(key)] = False

    def isPressed(self, key):
        if type(key) == str:
            key = pynput.keyboard.KeyCode.from_char(key)
        key = self.convertKeyCode(key)

        if key in self.pressedKeys:
            return self.pressedKeys[key]
        else:
            return False

    def getMouseDelta(self):
        mouseDelta = glm.ivec2(self.mouse.position) - self.mouseCenter
        self.mouse.position = (self.mouseCenter.x, self.mouseCenter.y)
        return mouseDelta
