__author__ = 'DUDE'

import numpy


class TextureFile:

    def __init__(self, file_name):
        self._data = numpy.fromfile(file_name, dtype='B')
        #separate the data into left and right nibbles
        self._lefts = self._data >> 4 & 15
        self._rights = self._data & 15
        #then interleave them into the full array
        self.full = numpy.dstack((self._lefts, self._rights)).flatten()
        self.full.resize((256, 1024))

if __name__ == "__main__":
    import pygame
    import random
    import os
    #find all texture files in the MAP directory and pick one at random
    os.chdir('C:\\Users\\DUDE\\PycharmProjects\\Ganesha-0.60\\FINALFANTASYTACTICS\\MAP\\')
    all_files = os.listdir()
    texture_files = [tex for tex in all_files if os.stat(tex).st_size == 131072]
    random_tex_file = random.choice(texture_files)
    texture_file = TextureFile(random_tex_file)
    #display it in greyscale
    pygame.init()
    screen = pygame.display.set_mode(texture_file.full.shape[:2])
    #scale the palette index to 24-bit color (8 a piece)
    scaled = texture_file.full.astype(numpy.uint32) * 16
    #then copy that value to each of the red, green, and blue values
    grey_scaled = scaled.reshape((texture_file.full.shape + (1,))).repeat(3, 2)
    pygame.surfarray.blit_array(screen, grey_scaled)
    pygame.display.flip()
    done = False
    while not done:
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN or e.type == pygame.QUIT:
                done = True
    pygame.quit()