__author__ = 'DUDE'

import os
from GNSFile import GNSFile


class MapFileTree:
    """ Takes a map file and produces an interface consisting of
    -a list of contexts, each itself consisting of
        -the associated texture(s)
        -a list of textured triangles and their texture coordinates, normals, palettes, and visibility info
        -a list of textured quads    "                                                                    "
        -a list of untextured triangles and their visibility info
        -a list of untextured quads     "                       "
    -the actual terrain info
    -the background gradient
    -all ambient and directional lighting
    -animation instructions
"""
    def __init__(self, map_file):
        map_dir, rel_name = os.path.split(map_file)
        map_name = os.path.splitext(rel_name)[0]
        self.gns_file = GNSFile(map_file)
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
    import sys
    from PyQt4 import QtGui
    app = QtGui.QApplication(sys.argv)
    map_file = QtGui.QFileDialog.getOpenFileName(caption='QGanesha',
                                                 filter='FFT Map Files (*.GNS)')
    current_map = MapFileTree(map_file)
    print(current_map.items)
    print(current_map.get_files((34, 0, 128, 5889)))