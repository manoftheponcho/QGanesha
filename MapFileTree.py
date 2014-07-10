__author__ = 'DUDE'

import os
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
        self.items = dict(zip(self.gns_file.situations, self.resources))

    def get_files(self, situation):
        #return all values of self.items for which some or all parts of the key match, if the rest are zero
        return [self.items[sit] for sit in self.items]
#                if (sit == situation or
#                    (sit[0], sit[1], 0)
if __name__ == "__main__":
    import random
    current_map = MapFileTree('C:\\Users\DUDE\\PycharmProjects\\Ganesha-0.60\\FINALFANTASYTACTICS\\MAP\\',
                              'MAP{:03}'.format(random.randint(1, 119)))
    print(current_map.items)
