__author__ = 'DUDE'

import os
from GNSFile import GNSFile

class MapFileTree:

    def __init__(self, map_dir, map_name):
        try:
            self.gns_file = GNSFile(map_dir + map_name + '.GNS')
        except FileNotFoundError:
            self.gns_file = GNSFile(map_dir + map_name + '.gns')

        #find all mesh files(files with the same base name but a different extension)
        self.resources = [res for res in os.listdir(map_dir)
                          if os.path.splitext(res)[0] == map_name and
                          os.path.splitext(res)[1].lower() != '.gns']
        #sort the extensions by numeric order instead of lexicographic(remember to remove the dot)
        self.resources.sort(key=lambda s: int(os.path.splitext(s)[1].strip('.')))

if __name__ == "__main__":
    import random
    current_map = MapFileTree('C:\\Users\DUDE\\PycharmProjects\\Ganesha-0.60\\FINALFANTASYTACTICS\\MAP\\',
                              'MAP{:03}'.format(random.randint(1, 119)))
    print('gns_file = {}, mesh_files = {}'.format(current_map.gns_file, current_map.resources))