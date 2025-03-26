import pynput
import glm

class InputHandler:
    def __init__(self, mouseCenter):
        self.mouseController = pynput.mouse.Controller()
        self.pressedKeys = {}

        self.lastMousePos = None
        self.currentMousePos = glm.ivec2()
        self.mouseCenter = mouseCenter

        self.keyboardListener = pynput.keyboard.Listener(on_press = self.keyPressed, on_release = self.keyReleased)
        self.mouseListener = pynput.mouse.Listener(on_move = self.mouseMoved)
        self.keyboardListener.start()
        self.mouseListener.start()

    def convertKeyCode(self, key):
        if type(key) == pynput.keyboard.KeyCode:
            return pynput.keyboard.KeyCode.from_char(key.char.lower())
        return key

    def mouseMoved(self, newX, newY):
        self.currentMousePos.x = newX
        self.currentMousePos.y = newY

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
        if self.currentMousePos.x == 0 and self.currentMousePos.y == 0:
            return
        
        mouseDelta = self.currentMousePos - self.mouseCenter
        self.mouseController.position = (self.mouseCenter.x, self.mouseCenter.y)
        return mouseDelta
