__author__ = 'DUDE'

import os
import numpy
from GNSFile import GNSFile
from MeshFile import MeshFile
from PyQt4.QtGui import QVector2D, QVector3D

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
    class TexPoint(QVector3D):
        def __init__(self, pos=(0,0,0), uv=(0,0)):
            super().__init__(*pos)
            self.tex_uvs = QVector2D(uv)
        def __repr__(self):
            return '(x,y,z)={}, (u, v)={}'.format((self.x, self.y, self.z), self.tex_uvs)

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

        current_textures = self.get_files((34, 0, 0, 5889))
        current_meshes = (self.get_files((34, 0, 0, 11777)) +
                          self.get_files((34, 0, 0, 12033)) +
                          self.get_files((34, 0, 0, 12289)))
        mesh = MeshFile(map_dir + '\\' + current_meshes[0])
        points = numpy.concatenate((mesh.textris['A'],
                                    mesh.textris['B'],
                                    mesh.textris['C']))
        uvs = ((mesh.textriuvs[['A.u', 'A.v']].tolist() +
               mesh.textriuvs[['B.u', 'B.v']].tolist() +
               mesh.textriuvs[['C.u', 'C.v']].tolist()))
        self.textris = list(zip(points.tolist(), uvs))

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
#    map_file = QtGui.QFileDialog.getOpenFileName(caption='QGanesha',
#                                                 filter='FFT Map Files (*.GNS)')
    map_file = 'C:\\Users\\DUDE\\PycharmProjects\\Ganesha-0.60\\FINALFANTASYTACTICS\\MAP\\MAP001.GNS'
    current_map = MapFileTree(map_file)