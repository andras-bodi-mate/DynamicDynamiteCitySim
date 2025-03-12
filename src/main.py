import pygame as pg
from app import App

def main():
    pg.init()
    window = App()
    window.mainLoop()

main()