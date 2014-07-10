__author__ = 'DUDE'

import os
import numpy
from GNSFile import GNSFile

class MapFileTree:

    def __init__(self, map_dir, map_name):
        try:
            self.gns_file = GNSFile(map_dir + map_name + '.GNS')
        except FileNotFoundError:
            self.gns_file = GNSFile(map_dir + map_name + '.gns')

        #find all mesh/texture files(files with the same base name but a different extension)
        self.resources = [res for res in os.listdir(map_dir)
                          if os.path.splitext(res)[0] == map_name and
                          os.path.splitext(res)[1].lower() != '.gns']
        #sort the extensions by numeric order instead of lexicographic(remember to remove the dot)
        self.resources.sort(key=lambda s: int(os.path.splitext(s)[1].strip('.')))
        #note to self:  numpy and dictionaries don't play nicely together
        self.items = dict(zip(self.gns_file.situations.astype(tuple).tolist(), self.resources))

    def get_files(self, situation):
        #return all values of self.items for which some or all of the key matches, if the rest(except type) are zero
        #some default indices are always returned
        return ([self.items[sit] for sit in self.items if (((sit[0] == situation[0]) &
                                                            (sit[1] == situation[1]) &
                                                            (sit[2] == situation[2]) &
                                                            (sit[3] == situation[3])) |
                                                           ((sit[0] == situation[0]) &
                                                            (sit[1] == situation[1]) &
                                                            (sit[2] == 0) &
                                                            (sit[3] == situation[3])) |
                                                           ((sit[0] == situation[0]) &
                                                            (sit[1] == 0) &
                                                            (sit[2] == 0) &
                                                            (sit[3] == situation[3])) |
                                                           ((sit[0] == 0) &
                                                            (sit[1] == 0) &
                                                            (sit[2] == 0) &
                                                            (sit[3] == situation[3])) |
                                                          ((sit[0] == 34) &
                                                            (sit[1] == 0) &
                                                            (sit[2] == 0) &
                                                            (sit[3] == situation[3])) |
                                                           ((sit[0] == 48) &
                                                            (sit[1] == 0) &
                                                            (sit[2] == 0) &
                                                            (sit[3] == situation[3])) |
                                                           ((sit[0] == 112) &
                                                            (sit[1] == 0) &
                                                            (sit[2] == 0) &
                                                            (sit[3] == situation[3])))])

if __name__ == "__main__":
    import random
    current_map = MapFileTree('C:\\Users\DUDE\\PycharmProjects\\Ganesha-0.60\\FINALFANTASYTACTICS\\MAP\\',
                              'MAP{:03}'.format(random.randint(1, 119)))
    print(current_map.items)
    print(current_map.get_files((34, 0, 128, 5889)))