import glm
import pygame as pg
import numpy as np
from pygame import Vector3 as Vec3

class Camera:
    def __init__(self, window, FOV, nearClip = 0.1, farClip = 1000):
        self.window = window
        self.position = glm.vec3(0.0, 0.0, 5.0)  # Start position
        self.front = glm.vec3(0.0, 0.0, -1.0)  # Looking towards -Z
        self.up = glm.vec3(0.0, 1.0, 0.0)  # Y-axis is up
        self.yaw, self.pitch = -90.0, 0.0  # Camera rotation
        self.sensitivity = 0.06
        self.speed = 7

        self.projection = glm.perspective(glm.radians(FOV), window.size[0] / window.size[1], nearClip, farClip)
        self.processRotationInput((0.0, 0.0))

    def processMovementInput(self, keys, deltaTime):
        if keys[pg.K_w]:  # Move forward
            self.position += self.speed * glm.normalize(glm.vec3(self.front.x, 0, self.front.z)) * deltaTime
        if keys[pg.K_s]:  # Move backward
            self.position -= self.speed * glm.normalize(glm.vec3(self.front.x, 0, self.front.z)) * deltaTime
        if keys[pg.K_a]:  # Move left
            self.position -= glm.normalize(glm.cross(self.front, self.up)) * self.speed * deltaTime
        if keys[pg.K_d]:  # Move right
            self.position += glm.normalize(glm.cross(self.front, self.up)) * self.speed * deltaTime
        if keys[pg.K_SPACE]:
            self.position += self.speed * self.up * deltaTime
        if keys[pg.K_LSHIFT]:
            self.position -= self.speed * self.up * deltaTime

    
    def processRotationInput(self, relPos):
        self.yaw += relPos[0] * self.sensitivity
        self.pitch -= relPos[1] * self.sensitivity  # Invert Y-axis

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
        self.look = glm.lookAt(self.position, self.position + self.front, (0.0, 1.0, 0.0))

    def updateUniforms(self, shaderProgram):
        shaderProgram["camera"].write(self.projection * self.look)