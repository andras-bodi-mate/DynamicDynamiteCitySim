import glm
import numpy as np
from pynput.keyboard import Key

from inputHandler import InputHandler

class Camera:
    def __init__(self, window, FOV, nearClip = 0.5, farClip = 1000.0):
        self.window = window
        self.position = glm.vec3(0.0, 3.0, 10.0)  # Start position
        self.front = glm.vec3(0.0, 0.0, -1.0)  # Looking towards -Z
        self.up = glm.vec3(0.0, 1.0, 0.0)  # Y-axis is up
        self.yaw, self.pitch = -90.0, 0.0  # Camera rotation
        self.sensitivity = 0.06
        self.speed = 7
        self.fov = FOV

        self.projection = glm.perspective(glm.radians(FOV), window.size.x / window.size.y, nearClip, farClip)
        self.processRotationInput(glm.vec2(0.0, 0.0))
    
    def processMovementInput(self, inpuHandler: InputHandler, deltaTime):
        if inpuHandler.isPressed('w'):  # Move forward
            self.position += self.speed * glm.normalize(glm.vec3(self.front.x, 0, self.front.z)) * deltaTime
        if inpuHandler.isPressed('s'):  # Move backward
            self.position -= self.speed * glm.normalize(glm.vec3(self.front.x, 0, self.front.z)) * deltaTime
        if inpuHandler.isPressed('a'):  # Move left
            self.position -= glm.normalize(glm.cross(self.front, self.up)) * self.speed * deltaTime
        if inpuHandler.isPressed('d'):  # Move right
            self.position += glm.normalize(glm.cross(self.front, self.up)) * self.speed * deltaTime
        if inpuHandler.isPressed(Key.space):
            self.position += self.speed * self.up * deltaTime
        if inpuHandler.isPressed(Key.shift_l):
            self.position -= self.speed * self.up * deltaTime
    
    def processRotationInput(self, deltaPos):
        self.yaw += deltaPos.x * self.sensitivity
        self.pitch -= deltaPos.y * self.sensitivity  # Invert Y-axis

        # Clamp pitch to avoid flipping
        self.pitch = max(-89.0, min(89.0, self.pitch))

        # Calculate new camera direction
        direction = glm.vec3(
            np.cos(glm.radians(self.yaw)) * np.cos(glm.radians(self.pitch)),
            np.sin(glm.radians(self.pitch)),
            np.sin(glm.radians(self.yaw)) * np.cos(glm.radians(self.pitch))
        )
        self.front = glm.normalize(direction)

    def calculateViewMatrix(self):
        self.view = glm.lookAt(self.position, self.position + self.front, (0.0, 1.0, 0.0))

    def updateUniforms(self, shaderProgram, writeProjection = True, writeView = True):
        if writeProjection:
            shaderProgram["u_projection"].write(self.projection)

        if writeView:
            shaderProgram["u_view"].write(self.view)