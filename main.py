import pygame as pg
import backend as be
import interface as gui
import config as cf
import time


if __name__ == '__main__':

    player = be.Backend()

    while True:
        gui.root.fill(cf.SCREEN_FILL)

        player.update()
        player.draw()

        time.sleep(0.04)

        pg.display.flip()
